# ── 25a. Helpers (verification + hard mode). Nothing here trains a detector: fold detectors come from the weights cache. ──
VERIFY_SEED = SEED + 7
_MODELS = {}


def cached_fold_model(name, fn, fold):
    """The fold detector Sections 14-17 trained for (name, fold), loaded from the weights cache; None if it is not there."""
    if not os.path.isfile(FILTER_WEIGHTS_JSON):
        return None
    with open(FILTER_WEIGHTS_JSON, encoding="utf-8") as f:
        cache = json.load(f)
    root = filtered_root_for(name, fn)
    key = (f"{os.path.basename(os.path.normpath(root))}_cv{CV_FOLDS}f{fold}{FOLD_TAG}_os{OVERSAMPLE_MAX_FACTOR if OVERSAMPLE else 0}"
           f"_e{FILTER_EPOCHS}_tf{STRESS_TRAIN_FRAC:g}_sz{CV_IMGSZ}_v{CV_VAL_FRAC:g}")
    w = cache.get(key)
    return YOLO(w) if (w and os.path.isfile(w)) else None


def get_model(name, fn, fold):
    if (name, fold) not in _MODELS:
        _MODELS[(name, fold)] = cached_fold_model(name, fn, fold)
    return _MODELS[(name, fold)]


def predict_gray(model, gray, imgsz=None):
    return yolo_predict_full(model, cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR), imgsz or CV_IMGSZ)


def erase_boxes(gray, boxes, pad=0.3):
    """Paint the given balls (cx, cy, w, h in px) over with the surrounding background (local cv2.inpaint, so it stays fast)."""
    out = gray.copy()
    H, W = gray.shape
    for cx, cy, bw, bh in boxes:
        r = int(max(bw, bh) / 2 * (1 + pad)) + 1
        x0, x1 = max(0, int(cx) - 3 * r), min(W, int(cx) + 3 * r + 1)
        y0, y1 = max(0, int(cy) - 3 * r), min(H, int(cy) + 3 * r + 1)
        crop = np.ascontiguousarray(out[y0:y1, x0:x1])
        m = np.zeros(crop.shape, np.uint8)
        cv2.circle(m, (int(cx) - x0, int(cy) - y0), r, 255, -1)
        out[y0:y1, x0:x1] = cv2.inpaint(crop, m, 5, cv2.INPAINT_TELEA)
    return out


def paste_ball(gray, box, target_xy, feather=0.3):
    """Copy the ball `box` (with a little surrounding) to target_xy with a soft edge. None if the patch leaves the image."""
    cx, cy, bw, bh = box
    r = int(max(bw, bh) / 2 * 1.4) + 1
    H, W = gray.shape
    sx0, sy0, sx1, sy1 = int(cx) - r, int(cy) - r, int(cx) + r + 1, int(cy) + r + 1
    tx, ty = int(target_xy[0]), int(target_xy[1])
    dx0, dy0, dx1, dy1 = tx - r, ty - r, tx + r + 1, ty + r + 1
    if min(sx0, sy0, dx0, dy0) < 0 or max(sx1, dx1) > W or max(sy1, dy1) > H:
        return None
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
    alpha = np.clip((1.0 - np.sqrt(xx ** 2 + yy ** 2) / r) / max(feather, 1e-3), 0, 1)
    out = gray.copy()
    mixed = alpha * gray[sy0:sy1, sx0:sx1].astype(np.float32) + (1 - alpha) * gray[dy0:dy1, dx0:dx1].astype(np.float32)
    out[dy0:dy1, dx0:dx1] = np.clip(mixed, 0, 255).astype(np.uint8)
    return out


def pick_insert_xy(part, boxes, rng, size, tries=400):
    """A random free spot well inside the rectangle (>= 2 ball sizes from its edge, >= 2.5 sizes from every ball)."""
    poly = part["poly"].reshape(-1, 1, 2).astype(np.float32)
    x0, y0, w0, h0 = cv2.boundingRect(poly)
    for _ in range(tries):
        x, y = rng.uniform(x0, x0 + w0), rng.uniform(y0, y0 + h0)
        if cv2.pointPolygonTest(poly, (float(x), float(y)), True) < 2 * size:
            continue
        if all(math.hypot(x - b[0], y - b[1]) > 2.5 * max(b[2], b[3]) for b in boxes):
            return float(x), float(y)
    return None


def run_counterfactuals(kind, items, seed=VERIFY_SEED):
    """kind = 'remove_one' | 'insert_one' | 'erase_all'. Starts from clean OK images, scored by the detector that never saw them."""
    rng = np.random.default_rng(seed)
    rows = []
    for it in tqdm(items, desc=kind, unit="img"):
        g = gt_by_key[it["key"]]
        if g["part"] is None or g["gt_pred"] != "OK":
            continue
        model = get_model("Original", identity_filter, FOLD_OF[it["key"]])
        if model is None:
            continue
        gray = cv2.imread(it["img"], cv2.IMREAD_GRAYSCALE)
        boxes = [tuple(b) for b in g["gt_boxes"]]
        wh = (g["W"], g["H"])
        inside = judge_boxes([(b[0], b[1]) for b in boxes], g["part"], wh)["inside"]
        in_idx = [i for i, ins in enumerate(inside) if ins]
        if not in_idx:
            continue
        target_xy = tsize = None
        if kind == "remove_one":
            i = int(rng.choice(in_idx))
            tb = boxes[i]
            new_gray, new_boxes = erase_boxes(gray, [tb]), [b for j, b in enumerate(boxes) if j != i]
            target_xy, tsize = (tb[0], tb[1]), max(tb[2], tb[3])
        elif kind == "insert_one":
            src = boxes[int(rng.choice(in_idx))]
            xy = pick_insert_xy(g["part"], boxes, rng, max(src[2], src[3]))
            new_gray = paste_ball(gray, src, xy) if xy is not None else None
            if new_gray is None:
                continue
            new_boxes = boxes + [(xy[0], xy[1], src[2], src[3])]
            target_xy, tsize = xy, max(src[2], src[3])
        elif kind == "erase_all":
            new_gray, new_boxes = erase_boxes(gray, boxes), []
        else:
            raise ValueError(kind)
        xywh, conf = predict_gray(model, new_gray)
        pts = [(float(x), float(y)) for x, y, _, _ in xywh]
        j_new = judge_boxes(pts, g["part"], wh)
        j_exp = judge_boxes([(b[0], b[1]) for b in new_boxes], g["part"], wh)
        st = ball_match_stats(new_boxes, xywh, conf) if new_boxes else dict(miss=0, extra=len(pts))
        near = target_xy is not None and any(math.hypot(x - target_xy[0], y - target_xy[1]) <= 0.5 * tsize for x, y in pts)
        rows.append(dict(key=it["key"], kind=kind, n_det=len(pts), near_target=bool(near), pred=j_new["pred"],
                         exp_pred=j_exp["pred"], counts_equal=bool(j_new["counts"] == j_exp["counts"]),
                         miss=st["miss"], extra=st["extra"]))
    return rows


def permutation_test(rows, n_perm=10000, seed=VERIFY_SEED):
    """Accuracy of the real predictions vs the accuracy they would get against shuffled ground truth."""
    gt = np.array([r["gt_pred"] == "NG" for r in rows])
    pr = np.array([r["pred"] == "NG" for r in rows])
    acc = float((gt == pr).mean())
    rng = np.random.default_rng(seed)
    null = np.array([(rng.permutation(gt) == pr).mean() for _ in range(n_perm)])
    return acc, null, float((1 + (null >= acc).sum()) / (n_perm + 1))


def global_shortcut_baseline(items, size=32):
    """Image-level classifiers without any localisation, scored on the SAME folds as the detector.
    Returns {name: (accuracy %, balanced accuracy %)} or None if scikit-learn is missing."""
    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler
    except ImportError:
        print("scikit-learn is not installed (pip install scikit-learn) -> check 5 skipped")
        return None
    thumbs, stats, y, fold = [], [], [], []
    for it in items:
        g = cv2.imread(it["img"], cv2.IMREAD_GRAYSCALE)
        thumbs.append(cv2.resize(g, (size, size), interpolation=cv2.INTER_AREA).astype(np.float32).ravel())
        stats.append(np.percentile(g, [1, 5, 10, 25, 50, 75, 90, 95, 99]).tolist() + [float(g.mean()), float(g.std())])
        y.append(gt_by_key[it["key"]]["gt_pred"] == "NG")
        fold.append(FOLD_OF[it["key"]])
    y, fold = np.array(y), np.array(fold)
    out = {}
    for name, X in (("32x32 thumbnail", np.array(thumbs)), ("global gray statistics", np.array(stats))):
        pred = np.zeros(len(y), bool)
        for f in sorted(set(fold)):
            tr, te = fold != f, fold == f
            if len(set(y[tr])) < 2:                  # degenerate fold (cannot happen with stratified folds)
                pred[te] = bool(y[tr][0])
                continue
            clf = make_pipeline(StandardScaler(), LogisticRegression(C=0.05, max_iter=3000, class_weight="balanced"))
            clf.fit(X[tr], y[tr])
            pred[te] = clf.predict(X[te])
        rec_ng = (pred & y).sum() / max(y.sum(), 1)
        rec_ok = (~pred & ~y).sum() / max((~y).sum(), 1)
        out[name] = (100.0 * (pred == y).mean(), 50.0 * (rec_ng + rec_ok))
    return out


# ── difficulty strata (from the number of labelled balls; an OK image has exactly 13) ──
STRAT_ORDER = ["OK (13 balls)", "NG same count (wrong regions)", "NG +-1 ball", "NG >=2 balls off"]


def difficulty_of(key):
    g = gt_by_key[key]
    n = len(g["gt_boxes"])
    if g["gt_pred"] == "OK":
        return STRAT_ORDER[0]
    if n == 13:
        return STRAT_ORDER[1]
    return STRAT_ORDER[2] if abs(n - 13) == 1 else STRAT_ORDER[3]


def stratified_table(names):
    recs = []
    for name in names:
        per = PER_IMAGE.get(name)
        if not per:
            continue
        agg = {d: [0, 0, 0] for d in STRAT_ORDER}
        for r in per:
            a = agg[difficulty_of(r["key"])]
            a[0] += 1
            a[1] += int(r["match"])
            a[2] += int(r.get("miss") == 0 and r.get("extra") == 0)
        rec = {"Method": name}
        for d in STRAT_ORDER:
            n_, ok_, st_ = agg[d]
            rec[f"{d} acc"] = 100.0 * ok_ / n_ if n_ else float("nan")
            rec[f"{d} strict"] = 100.0 * st_ / n_ if n_ else float("nan")
        recs.append(rec)
    return pd.DataFrame(recs)


def strict_mcnemar(ref_name, test_name):
    """Paired exact McNemar on 'strict correct' (every labelled ball found, no extra detection anywhere)."""
    def ok(per):
        return {r["key"]: int(r.get("miss") == 0 and r.get("extra") == 0) for r in per}
    ref, tst = ok(PER_IMAGE[ref_name]), ok(PER_IMAGE[test_name])
    keys = ref.keys() & tst.keys()
    b = sum(ref[k] == 1 and tst[k] == 0 for k in keys)
    c = sum(ref[k] == 0 and tst[k] == 1 for k in keys)
    return b, c, mcnemar_exact(b, c)


# ── photometric shifts for the hard mode (no geometry change, so labels and rectangle stay valid) ──
def corrupt(gray, spec, key):
    kind, v = spec["kind"], spec["v"]
    if kind == "blur":
        return cv2.GaussianBlur(gray, (0, 0), float(v))
    if kind == "down":
        h, w = gray.shape
        small = cv2.resize(gray, (max(1, w // int(v)), max(1, h // int(v))), interpolation=cv2.INTER_AREA)
        return cv2.resize(small, (w, h), interpolation=cv2.INTER_LINEAR)
    f = gray.astype(np.float32)
    if kind == "noise":
        rng = np.random.default_rng(int(hashlib.md5((key + "|shift").encode("utf-8")).hexdigest()[:8], 16))
        f = f + rng.normal(0.0, float(v), f.shape)
    elif kind == "contrast":
        f = 128.0 + float(v) * (f - 128.0)
    elif kind == "bright":
        f = f + float(v)
    else:
        raise ValueError(kind)
    return np.clip(f, 0, 255).astype(np.uint8)


def quick_metrics(rows):
    n = len(rows)
    tp = sum(r["gt_pred"] == "NG" and r["pred"] == "NG" for r in rows)
    fn = sum(r["gt_pred"] == "NG" and r["pred"] == "OK" for r in rows)
    fp = sum(r["gt_pred"] == "OK" and r["pred"] == "NG" for r in rows)
    tn = sum(r["gt_pred"] == "OK" and r["pred"] == "OK" for r in rows)
    n_gt = sum(r["n_gt"] for r in rows)
    return dict(n=n, acc=100.0 * (tp + tn) / n, bal=50.0 * (tp / max(tp + fn, 1) + tn / max(tn + fp, 1)),
                strict=100.0 * sum(r["miss"] == 0 and r["extra"] == 0 for r in rows) / n,
                ball_recall=100.0 * (1 - sum(r["miss"] for r in rows) / n_gt) if n_gt else float("nan"),
                pred_ng=100.0 * (tp + fp) / n)


def run_shift(methods, conds, items, cache_path):
    """Clean-trained detectors (no retraining) judging corrupted held-out images: corrupt -> filter -> detector of the image's fold.
    methods = [(name, filter_fn)], conds = [(label, spec)]. Finished conditions are read from / written to cache_path."""
    res = {}
    if os.path.isfile(cache_path):
        with open(cache_path, encoding="utf-8") as f:
            res = json.load(f)
    for label, spec in conds:
        if label in res and all(m in res[label] for m, _ in methods):
            print(f"[shift] {label}: reusing the saved result")
            continue
        rows = {m: [] for m, _ in methods}
        for it in tqdm(items, desc=f"shift {label}", unit="img"):
            g, fold = gt_by_key[it["key"]], FOLD_OF[it["key"]]
            gray = corrupt(cv2.imread(it["img"], cv2.IMREAD_GRAYSCALE), spec, it["key"])
            for m, fn in methods:
                filtered, _ = apply_filter_gray(gray, fn)
                xywh, conf = predict_gray(get_model(m, fn, fold), filtered)
                row = _row(it, [(float(x), float(y)) for x, y, _, _ in xywh])
                row.update(ball_match_stats(g["gt_boxes"], xywh, conf))
                rows[m].append(row)
        res[label] = {m: quick_metrics(r) for m, r in rows.items()}
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(res, f)
        print(f"[shift] {label}: " + " | ".join(f"{m} {res[label][m]['strict']:.1f}%" for m, _ in methods[:4]) + " ...")
    return res


print("Verification / hard-mode helpers ready")
