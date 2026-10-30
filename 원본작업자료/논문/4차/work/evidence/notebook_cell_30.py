# ── Experiment settings ─────────────────────────────────────────
FILTER_MODE = "train_per_filter"    # "inference_only" | "train_per_filter"
# [changed] was "inference_only": a YOLO trained on normal images sees inverted / binarised / blurred inputs it has never
# seen, so it predicts (almost) nothing and every image collapses to NG (or OK) -> the accuracy just equals the class share.
FILTER_EPOCHS = 30                  # epochs per filter in train_per_filter mode (the Original model uses EPOCHS)

# ── [added] Stratified K-fold cross-validation (train_per_filter mode) ──────────────────────────
# Why: with the fixed 400/100 split there is no test set, the 100 scored images also picked the checkpoint (best.pt),
# and even 100/100 correct only gives a 95% CI of 96.3 - 100. In CV every one of the 500 images is judged exactly
# once by a detector that never trained on it (80% of the images, minus an inner 10% val used for early stopping),
# so N = 500. Original and every filter use the SAME training recipe (FILTER_EPOCHS, AUG, oversampling) -> fair.
USE_CV = True
CV_FOLDS = 5
CV_RUN_FOLDS = None        # None: "quick" -> [0] only, otherwise every fold; or e.g. [0, 1]
CV_VAL_FRAC = 0.10         # inner validation share of the non-test images (early stopping / best.pt only)

# ── [added] Optional stress conditions (default: all off). A harder detector task is where filters can differ. ──
STRESS_TRAIN_FRAC = 1.0    # e.g. 0.25 -> train on 25% of the training images only (low-data regime)
STRESS_IMGSZ = None        # e.g. 640  -> train / predict at a lower resolution than IMGSZ
STRESS_NOISE_STD = 0.0     # e.g. 15   -> Gaussian noise (gray levels, fixed per image) added BEFORE the filter
CV_IMGSZ = STRESS_IMGSZ or IMGSZ
_STRESS_TAG = (f"_n{STRESS_NOISE_STD:g}" if STRESS_NOISE_STD else "")

if USE_CV and FILTER_MODE != "train_per_filter":
    print("NOTE: USE_CV needs FILTER_MODE = 'train_per_filter' (otherwise one detector is scored on its own training images) -> CV switched off.")
    USE_CV = False


def _noisy(gray, key):
    if not STRESS_NOISE_STD:
        return gray
    rng = np.random.default_rng(int(hashlib.md5(key.encode("utf-8")).hexdigest()[:8], 16))
    return np.clip(gray.astype(np.float32) + rng.normal(0.0, STRESS_NOISE_STD, gray.shape), 0, 255).astype(np.uint8)

# RUN_PRESET: "quick"  -> smoke test : 30 random images per filter, every split
#             "final"  -> paper run  : the whole test split, every filter (nothing skipped)
#             "custom" -> use the three CUSTOM_* values below
RUN_PRESET = "final"    # [changed] was "quick": 30 images -> accuracy can only be k/30 (53.33 = 16/30, 100 = 30/30)
CUSTOM_EVAL_SPLITS = list(SPLITS)   # e.g. ["test"] to score only the test split
CUSTOM_QUICK_TEST_N = None          # e.g. 30 -> N random images per filter
CUSTOM_SKIP_FILTERS = set()         # e.g. {"Invert"} to leave a filter out

if RUN_PRESET == "quick":
    EVAL_SPLITS, QUICK_TEST_N, SKIP_FILTERS = list(SPLITS), 30, set()
elif RUN_PRESET == "final":
    # [fixed] this dataset may have no test split (by_split comes from Section 1): fall back test -> val -> everything available
    _fallback = next(([sp] for sp in ("test", "val") if by_split.get(sp)), [sp for sp in SPLITS if by_split.get(sp)])
    if _fallback != ["test"] and not USE_CV:
        print(f"WARNING: no test split found (images per split: {dict(by_split)}) -> scoring {_fallback} instead. "
              "Numbers on a split the detector trained on are optimistic; keep that in mind for the paper.")
    EVAL_SPLITS, QUICK_TEST_N, SKIP_FILTERS = _fallback, None, set()
elif RUN_PRESET == "custom":
    EVAL_SPLITS, QUICK_TEST_N, SKIP_FILTERS = list(CUSTOM_EVAL_SPLITS), CUSTOM_QUICK_TEST_N, set(CUSTOM_SKIP_FILTERS)
else:
    raise ValueError(f"Unknown RUN_PRESET: {RUN_PRESET!r} (use 'quick', 'final' or 'custom')")

eval_items = [it for it in dataset if it["split"] in EVAL_SPLITS and it["key"] in gt_by_key]

# ── [added] CV folds: every image gets one fold id (stratified by the label-based OK/NG judgement) ──
CV_ITEMS = [it for it in dataset if it["key"] in gt_by_key]


GROUP_FOLDS = globals().get("GROUP_FOLDS", False)       # [added v5] set / decided in Section 4b
DUP_GROUP_OF = globals().get("DUP_GROUP_OF", {})


def assign_folds(items, k, seed):
    rng = random.Random(seed)
    fold_of = {}
    if not (GROUP_FOLDS and DUP_GROUP_OF):          # plain stratified split (unchanged behaviour, old caches stay valid)
        for cls in ("OK", "NG"):
            keys = sorted(it["key"] for it in items if gt_by_key[it["key"]]["gt_pred"] == cls)
            rng.shuffle(keys)
            for i, key in enumerate(keys):
                fold_of[key] = i % k
        return fold_of
    # [added v5] near-duplicate images stay together: whole groups are dealt to the emptiest fold (per class, biggest first)
    groups = defaultdict(list)
    for it in items:
        groups[DUP_GROUP_OF[it["key"]]].append(it["key"])
    by_cls = {"OK": [], "NG": []}
    for g in groups.values():
        n_ok = sum(gt_by_key[x]["gt_pred"] == "OK" for x in g)
        by_cls["OK" if n_ok * 2 > len(g) else "NG"].append(sorted(g))
    for cls in ("OK", "NG"):
        units = sorted(by_cls[cls])
        rng.shuffle(units)
        units.sort(key=len, reverse=True)            # stable: big groups first, ties keep the shuffled order
        sizes = [0] * k
        for g in units:
            f = min(range(k), key=lambda x: (sizes[x], x))
            for key in g:
                fold_of[key] = f
            sizes[f] += len(g)
    return fold_of


FOLD_OF = assign_folds(CV_ITEMS, CV_FOLDS, SEED) if USE_CV else {}
FOLD_TAG = "_grp" if (USE_CV and GROUP_FOLDS and DUP_GROUP_OF) else ""     # part of every weights / result cache key
if USE_CV:
    print("Fold sizes: " + ", ".join(f"fold {f}: {sum(v == f for v in FOLD_OF.values())}" for f in range(CV_FOLDS))
          + ("  (near-duplicate groups kept together)" if FOLD_TAG else ""))


def fold_split(k):
    """(train, val, test) item lists of fold k. test = fold k; val = CV_VAL_FRAC of the rest (stratified)."""
    test = [it for it in CV_ITEMS if FOLD_OF[it["key"]] == k]
    rest = [it for it in CV_ITEMS if FOLD_OF[it["key"]] != k]
    rng = random.Random(SEED + 100 + k)
    train, val = [], []
    for cls in ("OK", "NG"):
        grp = [it for it in rest if gt_by_key[it["key"]]["gt_pred"] == cls]
        rng.shuffle(grp)
        nv = max(1, round(len(grp) * CV_VAL_FRAC)) if grp else 0
        val += grp[:nv]
        tr = grp[nv:]
        train += tr[:max(1, round(len(tr) * STRESS_TRAIN_FRAC))] if tr else []
    return train, val, test


_run_folds = []
if USE_CV:
    _run_folds = list(CV_RUN_FOLDS) if CV_RUN_FOLDS is not None else ([0] if RUN_PRESET == "quick" else list(range(CV_FOLDS)))
    eval_items = [it for it in CV_ITEMS if FOLD_OF[it["key"]] in _run_folds]
    EVAL_SPLITS = [f"{CV_FOLDS}-fold CV, folds {_run_folds}"]
    QUICK_TEST_N = None
    print(f"Cross-validation: {CV_FOLDS} folds, running {_run_folds}  (train frac {STRESS_TRAIN_FRAC:g}, imgsz {CV_IMGSZ}, noise {STRESS_NOISE_STD:g})")
    for _f in _run_folds:
        _tr, _va, _te = fold_split(_f)
        _g = lambda xs, c: sum(gt_by_key[x["key"]]["gt_pred"] == c for x in xs)
        print(f"  fold {_f}: train {len(_tr)} (OK {_g(_tr, 'OK')}/NG {_g(_tr, 'NG')}) | val {len(_va)} | test {len(_te)} (OK {_g(_te, 'OK')}/NG {_g(_te, 'NG')})")
if QUICK_TEST_N is not None and len(eval_items) > QUICK_TEST_N:
    # [changed] stratified: half OK, half NG (a plain random sample of 30 can contain almost one class only)
    _rng = random.Random(SEED)
    _ok_items = [it for it in eval_items if gt_by_key[it["key"]]["gt_pred"] == "OK"]
    _ng_items = [it for it in eval_items if gt_by_key[it["key"]]["gt_pred"] == "NG"]
    _h = QUICK_TEST_N // 2
    eval_items = (_rng.sample(_ok_items, min(_h, len(_ok_items))) + _rng.sample(_ng_items, min(QUICK_TEST_N - _h, len(_ng_items))))
if not eval_items:
    raise RuntimeError(f"No images to score for EVAL_SPLITS={EVAL_SPLITS}.")

_n_gt_ok = sum(gt_by_key[it["key"]]["gt_pred"] == "OK" for it in eval_items)
_n_gt_ng = len(eval_items) - _n_gt_ok
print(f"RUN_PRESET = {RUN_PRESET}  (EVAL_SPLITS = {EVAL_SPLITS}, QUICK_TEST_N = {QUICK_TEST_N}, SKIP_FILTERS = {sorted(SKIP_FILTERS)})")
if RUN_PRESET == "quick":
    print("NOTE: the 'quick' preset is a smoke test, not a final result. Set RUN_PRESET = \"final\" for the paper run.")
print(f"FILTER_MODE = {FILTER_MODE}")
print(f"Images scored per filter: {len(eval_items)}  (GT OK {_n_gt_ok} / GT NG {_n_gt_ng}),  splits = {EVAL_SPLITS}")
if len(eval_items) < 100:
    print(f"WARNING: only {len(eval_items)} images are scored -> accuracy moves in steps of {100 / len(eval_items):.2f} pp and the 95% CI is wide. "
          "Use the whole test split (RUN_PRESET = 'final') or add val to CUSTOM_EVAL_SPLITS.")
if _n_gt_ok == 0 or _n_gt_ng == 0:
    print("WARNING: the ground truth contains only one class -> recall / precision / F1 of the missing class will be 0.0.")


def safe_filename(name):
    return "".join(c if c.isalnum() else "_" for c in name).strip("_").lower()


def apply_filter_gray(gray, filter_fn):
    """Apply a filter to a uint8 gray image. Returns (filtered uint8 gray image, filter time in seconds)."""
    t = to_gpu_tensor(gray)
    _sync()
    t0 = time.perf_counter()
    with torch.no_grad():
        out = filter_fn(t)
    _sync()
    dt = time.perf_counter() - t0
    return to_gray_np(out), dt


def save_filter_example(name, gray, filtered, scale=0.25, overwrite=True):
    """Save one 'Original | filtered' side-by-side example image per filter (overwrite=False keeps an existing file)."""
    out_path = os.path.join(FILTER_SAMPLE_DIR, f"{safe_filename(name)}_example.png")
    if not overwrite and os.path.isfile(out_path):
        return
    def _prep(img, label):
        vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        vis = cv2.resize(vis, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        cv2.putText(vis, label, (15, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 5, cv2.LINE_AA)
        cv2.putText(vis, label, (15, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv2.LINE_AA)
        return vis
    side = cv2.hconcat([_prep(gray, "Original"), _prep(filtered, name)])
    cv2.imwrite(out_path, side)


def yolo_centers(model, source):
    """Run YOLO on an image path or a BGR ndarray and return the detection-box centres."""
    pred = model.predict(source, imgsz=IMGSZ, conf=CONF_THRES, iou=IOU_THRES, verbose=False)[0]
    xywh = pred.boxes.xywh.cpu().numpy() if len(pred.boxes) else np.zeros((0, 4))
    return [(float(x), float(y)) for x, y, _, _ in xywh]


PER_IMAGE = {}   # method name -> one dict per image (saved to per_image_predictions.csv, used for the McNemar test)


def mcnemar_exact(b, c):
    """Exact two-sided McNemar test (binomial, p = 0.5) on the discordant pairs.
    b = images the reference judged right and the tested method wrong, c = the opposite."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1))
    return min(1.0, 2 * tail / 2 ** n)      # int / int stays exact for very large n (no float overflow)


def mcnemar_between(ref_name, test_name):
    """Paired comparison of two methods on the same images. 'right' = judgement equals the label-based GT.
    Returns (newly_wrong, newly_correct, p) of test_name relative to ref_name, or (None, None, None)."""
    ref = {r["key"]: r["match"] for r in PER_IMAGE.get(ref_name, [])}
    tst = {r["key"]: r["match"] for r in PER_IMAGE.get(test_name, [])}
    keys = ref.keys() & tst.keys()
    if not keys:
        return None, None, None
    b = sum(ref[k] == 1 and tst[k] == 0 for k in keys)
    c = sum(ref[k] == 0 and tst[k] == 1 for k in keys)
    return b, c, mcnemar_exact(b, c)


def summarize(name, rows, filter_ms, yolo_ms):
    """rows: one dict per image with gt_pred / pred / gt_counts / counts. NG is the positive class."""
    n = len(rows)
    tp = sum(r["gt_pred"] == "NG" and r["pred"] == "NG" for r in rows)
    fn = sum(r["gt_pred"] == "NG" and r["pred"] == "OK" for r in rows)
    fp = sum(r["gt_pred"] == "OK" and r["pred"] == "NG" for r in rows)
    tn = sum(r["gt_pred"] == "OK" and r["pred"] == "OK" for r in rows)
    ng_recall, ok_recall = _pct(tp, tp + fn), _pct(tn, tn + fp)
    precision = _pct(tp, tp + fp)
    f1 = 2 * precision * ng_recall / (precision + ng_recall) if (precision + ng_recall) else 0.0
    reg = {k: _pct(sum(r["counts"][k] == r["gt_counts"][k] for r in rows), n) for k in REGION_RULE}
    PER_IMAGE[name] = [dict(method=name, key=r["key"], split=r["split"], gt_pred=r["gt_pred"], pred=r["pred"],
                            match=int(r["pred"] == r["gt_pred"]),
                            **{f"count_{k}": r["counts"][k] for k in REGION_RULE},
                            **{k: r[k] for k in ("fold", "n_gt", "miss", "extra", "loc_err_px", "min_conf", "ref_label") if k in r}) for r in rows]
    # [added] continuous detection-quality metrics (they do not saturate at 100% like the OK/NG accuracy)
    _vals = lambda k: [r[k] for r in rows if r.get(k) is not None]
    n_gt = sum(r.get("n_gt", 0) for r in rows)
    nan = float("nan")
    ball_recall = 100.0 * (1 - sum(r.get("miss", 0) for r in rows) / n_gt) if n_gt else nan
    extra_per_img = float(np.mean(_vals("extra"))) if _vals("extra") else nan
    loc_err_px = float(np.mean(_vals("loc_err_px"))) if _vals("loc_err_px") else nan
    min_conf = 100.0 * float(np.mean(_vals("min_conf"))) if _vals("min_conf") else nan
    # [added v5] numbers that put the plain accuracy in context
    gt_ok_pct = _pct(tn + fp, n)
    _sr = [r for r in rows if r.get("miss") is not None and r.get("extra") is not None]
    strict_acc = _pct(sum(r["miss"] == 0 and r["extra"] == 0 for r in _sr), len(_sr)) if _sr else nan     # every labelled ball found, no extra detection anywhere
    _rr = [r for r in rows if r.get("ref_label") in ("OK", "NG")]
    ref_acc = _pct(sum(r["pred"] == r["ref_label"] for r in _rr), len(_rr)) if _rr else nan                # agreement with the independent OK/NG list
    gt_vs_ref_acc = _pct(sum(r["gt_pred"] == r["ref_label"] for r in _rr), len(_rr)) if _rr else nan       # how well the label rule itself matches that list
    nw = nc = mp = None
    if name != "Original":
        nw, nc, mp = mcnemar_between("Original", name)
    return dict(name=name, n_images=n, accuracy=_pct(tp + tn, n), bal_acc=(ng_recall + ok_recall) / 2,
                gt_ok_pct=gt_ok_pct, majority_acc=max(gt_ok_pct, 100 - gt_ok_pct), strict_acc=strict_acc,
                ref_acc=ref_acc, ref_n=len(_rr), gt_vs_ref_acc=gt_vs_ref_acc,
                pred_ng_pct=_pct(tp + fp, n), ball_recall=ball_recall, extra_per_img=extra_per_img,
                loc_err_px=loc_err_px, min_conf=min_conf,
                top_acc=reg["top"], left_acc=reg["left"], bottom_acc=reg["bottom"], right_acc=reg["right"],
                ok_recall=ok_recall, ng_recall=ng_recall, precision=precision, f1=f1,
                avg_time_ms=filter_ms, yolo_time_ms=yolo_ms, tp=tp, fn=fn, fp=fp, tn=tn,
                newly_wrong=nw, newly_correct=nc, mcnemar_p=mp)


REF_LABEL = {}      # [added v5] independent OK/NG list (OKNG_CSV: name,label), keyed by image stem
if OKNG_CSV and os.path.isfile(OKNG_CSV):
    with open(OKNG_CSV, newline="", encoding="utf-8-sig") as _f:
        for _r in csv.DictReader(_f):
            REF_LABEL[os.path.splitext(_r["name"].strip())[0]] = _r["label"].strip().upper()
    print(f"OKNG_CSV: {len(REF_LABEL)} reference labels loaded")


def _row(it, pts):
    gt = gt_by_key[it["key"]]
    j = judge_boxes(pts, gt["part"], (gt["W"], gt["H"]))
    return dict(key=it["key"], split=it["split"], gt_pred=gt["gt_pred"], pred=j["pred"],
                gt_counts=gt["gt_counts"], counts=j["counts"], ref_label=REF_LABEL.get(it["stem"]))


# ── Mode 1: filter at judgement time, reuse the YOLO trained on the original images ──
class _Progress:
    """Prints a status line at most every `every` seconds (and at the end) with elapsed time and a rough ETA,
    so that a long run does not look like a frozen notebook."""

    def __init__(self, tag, total, every=30):
        self.tag, self.total, self.every = tag, total, every
        self.t0 = self.last = time.time()

    def update(self, done):
        now = time.time()
        if done == self.total or now - self.last >= self.every:
            self.last = now
            el = now - self.t0
            eta = el / done * (self.total - done) if done else 0.0
            print(f"    [{self.tag}] {done}/{self.total} images | {el / 60:.1f} min elapsed | ~{eta / 60:.1f} min left")


def evaluate_inference_only(name, filter_fn, items, model, save_example=True):
    rows, t_filter, t_yolo, example_saved = [], 0.0, 0.0, False
    prog = _Progress(name, len(items))
    for i, it in enumerate(items):
        gray = cv2.imread(it["img"], cv2.IMREAD_GRAYSCALE)
        filtered, dt = apply_filter_gray(gray, filter_fn)
        t_filter += dt
        if save_example and not example_saved and name != "Original":
            save_filter_example(name, gray, filtered, overwrite=False)   # Section 13 already saved the sample
            example_saved = True
        bgr = cv2.cvtColor(filtered, cv2.COLOR_GRAY2BGR)
        t0 = time.perf_counter()
        pts = yolo_centers(model, bgr)
        t_yolo += time.perf_counter() - t0
        rows.append(_row(it, pts))
        prog.update(i + 1)
    return summarize(name, rows, t_filter / len(items) * 1000, t_yolo / len(items) * 1000)


# ── Mode 2: filter the whole dataset, train one YOLO per filter ──
FILTER_WEIGHTS_JSON = os.path.join(RUNS_DIR, "filter_weights.json")


def _filtered_yaml(root):
    try:
        with open(_yaml_path, encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
    except Exception:
        cfg = {}
    cfg.setdefault("names", {0: "ball"})
    cfg["path"] = os.path.abspath(root)
    for k in ("train", "val", "test"):
        cfg.pop(k, None)
    for sp in sorted({it["split"] for it in dataset}):
        cfg[sp] = f"images/{sp}"
    path = os.path.join(root, "data.yaml")
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, allow_unicode=True, sort_keys=False)
    return path


def filtered_root_for(name, filter_fn):
    """Folder of the filtered dataset. A filter object with `root_key` (see SAME in Section 22) shares one folder."""
    key = getattr(filter_fn, "root_key", None) or filter_cache_key(name, filter_fn)
    return os.path.join(FILTERED_ROOT, key + _STRESS_TAG)


def build_filtered_dataset(name, filter_fn):
    """Write the filtered copy of every image (+ its label file) and return (root, avg filter time in ms)."""
    root = filtered_root_for(name, filter_fn)
    meta_path = os.path.join(root, "meta.json")
    all_items = [it for it in dataset if it["key"] in gt_by_key]
    if os.path.isfile(meta_path):
        with open(meta_path, encoding="utf-8") as f:
            meta = json.load(f)
        if meta.get("n_images") == len(all_items):
            print(f"    [{name}] reusing the existing filtered dataset: {root}")
            return root, meta["avg_filter_ms"]

    total, example_saved = 0.0, False
    prog = _Progress(f"{name} filtering", len(all_items))
    for i, it in enumerate(all_items):
        img_out = os.path.join(root, "images", it["split"], it["stem"] + ".png")
        lab_out = os.path.join(root, "labels", it["split"], it["stem"] + ".txt")
        os.makedirs(os.path.dirname(img_out), exist_ok=True)
        os.makedirs(os.path.dirname(lab_out), exist_ok=True)
        shutil.copyfile(it["lab"], lab_out)
        gray = _noisy(cv2.imread(it["img"], cv2.IMREAD_GRAYSCALE), it["key"])
        filtered, dt = apply_filter_gray(gray, filter_fn)
        total += dt
        cv2.imwrite(img_out, filtered, [cv2.IMWRITE_PNG_COMPRESSION, 1])
        if not example_saved:
            save_filter_example(name, gray, filtered, overwrite=False)   # Section 13 already saved the sample
            example_saved = True
        prog.update(i + 1)
    avg_ms = total / len(all_items) * 1000
    _filtered_yaml(root)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(dict(n_images=len(all_items), avg_filter_ms=avg_ms), f)
    return root, avg_ms


def get_filter_weights(name, root):
    """Train a YOLO on the filtered dataset (or reuse weights from an earlier run)."""
    cache = {}
    if os.path.isfile(FILTER_WEIGHTS_JSON):
        with open(FILTER_WEIGHTS_JSON, encoding="utf-8") as f:
            cache = json.load(f)
    key = os.path.basename(os.path.normpath(root))     # filter name + a hash of its parameters
    key += (f"_os{OVERSAMPLE_MAX_FACTOR}" if OVERSAMPLE else "") + f"_e{FILTER_EPOCHS}"   # [added] a changed recipe never reuses old weights
    w = cache.get(key)
    if w and os.path.isfile(w):
        print(f"    [{name}] reusing trained weights: {w}")
        return w
    m = YOLO(MODEL_SIZE)
    data_yaml = _filtered_yaml(root)
    if OVERSAMPLE:     # [added] same oversampling as the Original model, on the filtered train images
        pairs = [(it["key"], os.path.join(root, "images", "train", it["stem"] + ".png"),
                  os.path.join(root, "labels", "train", it["stem"] + ".txt"))
                 for it in dataset if it["split"] == "train" and it["key"] in gt_by_key]
        if pairs:
            _v = os.path.join(os.path.abspath(root), "images", "val")
            if not os.path.isdir(_v):
                _v = os.path.join(os.path.abspath(root), "images", "train")
            data_yaml, _ = build_oversampled_dataset(pairs, os.path.abspath(root) + "_os", _v)
    res = m.train(data=data_yaml, epochs=FILTER_EPOCHS, imgsz=IMGSZ, batch=BATCH,
                  project=RUNS_DIR, name=f"ball_detect_{key}", seed=SEED, patience=15, **AUG)
    w = str(res.save_dir / "weights" / "best.pt")
    cache[key] = w
    os.makedirs(RUNS_DIR, exist_ok=True)
    with open(FILTER_WEIGHTS_JSON, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)
    return w


def evaluate_train_per_filter(name, filter_fn, items):
    root, filter_ms = build_filtered_dataset(name, filter_fn)
    model = YOLO(get_filter_weights(name, root))
    rows, t_yolo = [], 0.0
    for i, it in enumerate(items):
        img_path = os.path.join(root, "images", it["split"], it["stem"] + ".png")
        t0 = time.perf_counter()
        pts = yolo_centers(model, img_path)
        t_yolo += time.perf_counter() - t0
        rows.append(_row(it, pts))
        if (i + 1) % 100 == 0 or (i + 1) == len(items):
            print(f"    [{name}] {i + 1}/{len(items)} images")
    return summarize(name, rows, filter_ms, t_yolo / len(items) * 1000)


# ── [added] Mode 3: stratified K-fold CV (USE_CV) ──────────────────────────────────────────────
def yolo_predict_full(model, source, imgsz):
    pred = model.predict(source, imgsz=imgsz, conf=CONF_THRES, iou=IOU_THRES, verbose=False)[0]
    xywh = pred.boxes.xywh.cpu().numpy() if len(pred.boxes) else np.zeros((0, 4))
    conf = pred.boxes.conf.cpu().numpy() if len(pred.boxes) else np.zeros(0)
    return xywh, conf


def ball_match_stats(gt_boxes, xywh, conf, tol_frac=0.5):
    """Detection quality of one image, independent of the OK/NG rule. A prediction matches a labelled ball when
    its centre is within tol_frac x box size of the label centre (greedy nearest-first, one-to-one).
    miss = labelled balls nobody found, extra = predictions without a ball, loc_err_px = mean centre error of the
    matches, min_conf = lowest confidence among the matches (0 if a ball was missed) = how close the image was to failing."""
    G = np.array([[b[0], b[1]] for b in gt_boxes], dtype=float).reshape(-1, 2)
    gsz = np.array([max(b[2], b[3]) for b in gt_boxes], dtype=float)
    P = np.asarray(xywh, dtype=float).reshape(-1, 4)[:, :2]
    conf = np.asarray(conf, dtype=float)
    if len(G) == 0:
        return dict(n_gt=0, miss=0, extra=len(P), loc_err_px=None, min_conf=None)
    cand = sorted((float(np.hypot(*(G[i] - P[j]))), i, j) for i in range(len(G)) for j in range(len(P)))
    used_g, used_p, errs, confs = set(), set(), [], []
    for d, i, j in cand:
        if i in used_g or j in used_p or d > tol_frac * gsz[i]:
            continue
        used_g.add(i); used_p.add(j); errs.append(d); confs.append(float(conf[j]))
    miss = len(G) - len(used_g)
    return dict(n_gt=len(G), miss=miss, extra=len(P) - len(used_p),
                loc_err_px=float(np.mean(errs)) if errs else None,
                min_conf=0.0 if (miss or not confs) else float(min(confs)))


def build_fold_dataset(root, fold):
    """Symlinks the filtered images of `root` into <root>_cv<K>f<fold>/{train,val,test} (train is oversampled).
    Returns (data.yaml path, info)."""
    train, val, test = fold_split(fold)
    dst = os.path.abspath(root) + f"_cv{CV_FOLDS}f{fold}"

    def _pairs(items):
        return [(it["key"], os.path.join(root, "images", it["split"], it["stem"] + ".png"),
                 os.path.join(root, "labels", it["split"], it["stem"] + ".txt")) for it in items]

    for sub, items in (("val", val), ("test", test)):
        idir, ldir = os.path.join(dst, "images", sub), os.path.join(dst, "labels", sub)
        for d in (idir, ldir):
            shutil.rmtree(d, ignore_errors=True)
            os.makedirs(d, exist_ok=True)
        for _, img, lab in _pairs(items):
            _link_or_copy(img, os.path.join(idir, os.path.basename(img)))
            shutil.copyfile(lab, os.path.join(ldir, os.path.basename(lab)))
    yaml_path, info = build_oversampled_dataset(_pairs(train), dst, os.path.join(dst, "images", "val"),
                                                max_factor=OVERSAMPLE_MAX_FACTOR if OVERSAMPLE else 1)
    with open(yaml_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    cfg["test"] = os.path.join(dst, "images", "test")
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, allow_unicode=True, sort_keys=False)
    return yaml_path, info


def get_fold_weights(name, root, fold):
    """Train (or reuse) the detector of one fold. Returns (weights path, data.yaml path)."""
    data_yaml, info = build_fold_dataset(root, fold)
    cache = {}
    if os.path.isfile(FILTER_WEIGHTS_JSON):
        with open(FILTER_WEIGHTS_JSON, encoding="utf-8") as f:
            cache = json.load(f)
    key = (f"{os.path.basename(os.path.normpath(root))}_cv{CV_FOLDS}f{fold}{FOLD_TAG}_os{OVERSAMPLE_MAX_FACTOR if OVERSAMPLE else 0}"
           f"_e{FILTER_EPOCHS}_tf{STRESS_TRAIN_FRAC:g}_sz{CV_IMGSZ}_v{CV_VAL_FRAC:g}")
    w = cache.get(key)
    if w and os.path.isfile(w):
        print(f"    [{name}] fold {fold}: reusing trained weights")
        return w, data_yaml
    print(f"    [{name}] fold {fold}: training on {info['n_after']} images ...")
    m = YOLO(MODEL_SIZE)
    res = m.train(data=data_yaml, epochs=FILTER_EPOCHS, imgsz=CV_IMGSZ, batch=BATCH, project=RUNS_DIR,
                  name=f"ball_detect_{key}", seed=SEED, patience=15, **AUG)
    w = str(res.save_dir / "weights" / "best.pt")
    cache[key] = w
    os.makedirs(RUNS_DIR, exist_ok=True)
    with open(FILTER_WEIGHTS_JSON, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)
    return w, data_yaml


def fold_map(model, data_yaml):
    """mAP50 / mAP50-95 (%) of a fold's detector on the fold's held-out test images."""
    try:
        v = model.val(data=data_yaml, split="test", imgsz=CV_IMGSZ, batch=BATCH, conf=0.001, iou=0.7,
                      verbose=False, plots=False, project=RUNS_DIR, name="cv_val", exist_ok=True)
        return 100.0 * float(v.box.map50), 100.0 * float(v.box.map)
    except Exception as e:
        print(f"    mAP skipped ({type(e).__name__}: {e})")
        return float("nan"), float("nan")


def read_yolo_history(weights_path):
    """Per-epoch curves of a finished YOLO run (results.csv next to weights/). Returns None when it is missing."""
    csv_path = os.path.join(os.path.dirname(os.path.dirname(str(weights_path))), "results.csv")
    if not os.path.isfile(csv_path):
        return None
    try:
        df = pd.read_csv(csv_path)
    except Exception:
        return None
    df.columns = [c.strip() for c in df.columns]

    def col(name):
        return [float(x) for x in df[name].tolist()] if name in df.columns else []
    return dict(loss=col("train/box_loss"), val_loss=col("val/box_loss"),
                map50=col("metrics/mAP50(B)"), map50_95=col("metrics/mAP50-95(B)"))


def _nanmean(xs):
    xs = [x for x in xs if x is not None and not math.isnan(x)]
    return float(np.mean(xs)) if xs else float("nan")


def evaluate_cv(name, filter_fn, items):
    """Each image is judged by the detector of the fold in which it is the held-out test image."""
    root, filter_ms = build_filtered_dataset(name, filter_fn)
    by_fold = defaultdict(list)
    for it in items:
        by_fold[FOLD_OF[it["key"]]].append(it)
    rows, t_yolo, fold_acc, m50, m5095 = [], 0.0, [], [], []
    histories = {}
    for fold in sorted(by_fold):
        w, data_yaml = get_fold_weights(name, root, fold)
        hist = read_yolo_history(w)
        if hist:
            histories[fold] = hist
        model = YOLO(w)
        a, b = fold_map(model, data_yaml)
        m50.append(a); m5095.append(b)
        fold_rows = []
        for it in by_fold[fold]:
            img_path = os.path.join(root, "images", it["split"], it["stem"] + ".png")
            t0 = time.perf_counter()
            xywh, conf = yolo_predict_full(model, img_path, CV_IMGSZ)
            t_yolo += time.perf_counter() - t0
            row = _row(it, [(float(x), float(y)) for x, y, _, _ in xywh])
            row.update(fold=fold, **ball_match_stats(gt_by_key[it["key"]]["gt_boxes"], xywh, conf))
            fold_rows.append(row)
        fold_acc.append(_pct(sum(r["pred"] == r["gt_pred"] for r in fold_rows), len(fold_rows)))
        print(f"    [{name}] fold {fold}: accuracy {fold_acc[-1]:.2f}% | mAP50-95 {b:.1f}% | {len(fold_rows)} held-out images")
        rows += fold_rows
        del model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    r = summarize(name, rows, filter_ms, t_yolo / len(rows) * 1000)
    r.update(map50=_nanmean(m50), map50_95=_nanmean(m5095), fold_acc=fold_acc, fold_std=float(np.std(fold_acc)),
             histories=histories)
    return r


def _result_line(r):
    s = (f"accuracy {r['accuracy']:.2f}% (majority baseline {r.get('majority_acc', float('nan')):.1f}%) | balanced {r['bal_acc']:.2f}% | NG recall {r['ng_recall']:.2f}% | "
         f"predicted NG {r['pred_ng_pct']:.1f}%")
    if r.get("strict_acc") is not None and not math.isnan(r["strict_acc"]):
        s += f" | strict {r['strict_acc']:.2f}%"
    if r.get("map50_95") is not None and not math.isnan(r["map50_95"]):
        s += f" | mAP50-95 {r['map50_95']:.1f}% | ball recall {r['ball_recall']:.2f}% | center err {r['loc_err_px']:.2f}px"
    return s + f" | filter {r['avg_time_ms']:.2f} ms/img"


# ── Resume support: every finished method is saved and skipped when the notebook is run again ──
RESULT_CACHE_DIR = os.path.join(FILTER_FIG_DIR, "result_cache")
REUSE_RESULTS = True      # False -> evaluate everything again (or delete the result_cache folder)
_EVAL_SIG = hashlib.md5(json.dumps(
    [[it["key"], gt_by_key[it["key"]]["gt_pred"], gt_by_key[it["key"]]["gt_counts"]] for it in eval_items],
    sort_keys=True).encode("utf-8")).hexdigest()


def _weights_id():
    p = getattr(yolo_model, "ckpt_path", None)
    if p and os.path.isfile(str(p)):
        st = os.stat(str(p))
        return f"{p}:{st.st_size}:{int(st.st_mtime)}"
    return str(p or "")


def _result_path_and_sig(name, filter_fn):
    """Cache file + signature of everything that decides a result: images and ground truth, mode, detector,
    thresholds and the filter's parameters. A changed signature means the saved result is ignored."""
    sig = json.dumps(dict(
        v=4, name=name, mode=FILTER_MODE, eval=_EVAL_SIG, weights=("cv" if USE_CV else _weights_id()), conf=CONF_THRES, iou=IOU_THRES,
        imgsz=CV_IMGSZ if USE_CV else IMGSZ,
        cv=dict(folds=CV_FOLDS, val=CV_VAL_FRAC, train_frac=STRESS_TRAIN_FRAC, noise=STRESS_NOISE_STD, **({"fold": FOLD_TAG} if FOLD_TAG else {})) if USE_CV else None,
        filt=filter_fn.signature() if hasattr(filter_fn, "signature") else "",
        train=dict(epochs=FILTER_EPOCHS, batch=BATCH, model=MODEL_SIZE, oversample=OVERSAMPLE, aug=AUG) if FILTER_MODE == "train_per_filter" else None), sort_keys=True)
    tag = hashlib.md5(sig.encode("utf-8")).hexdigest()[:8]
    return os.path.join(RESULT_CACHE_DIR, f"{filter_cache_key(name, filter_fn)}_{tag}.json"), sig


def cached_result(name, filter_fn):
    """The saved result of a method, or None. Also restores its per-image rows for the McNemar test."""
    if not REUSE_RESULTS:
        return None
    path, sig = _result_path_and_sig(name, filter_fn)
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    if d.get("signature") != sig:
        return None
    PER_IMAGE[name] = d["rows"]
    r = d["result"]
    if name != "Original":     # the McNemar numbers refer to the Original rows that are loaded / computed in this run
        r["newly_wrong"], r["newly_correct"], r["mcnemar_p"] = mcnemar_between("Original", name)
    return r


def save_result(name, filter_fn, r):
    path, sig = _result_path_and_sig(name, filter_fn)
    os.makedirs(RESULT_CACHE_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dict(signature=sig, result=r, rows=PER_IMAGE[name]), f, ensure_ascii=False)


def filter_params_str(filter_fn):
    """Human-readable parameters of a filter (shown in the tables)."""
    return filter_fn.describe() if hasattr(filter_fn, "describe") else "-"


def filter_cache_key(name, filter_fn):
    """Folder / weights key: the filter name plus a short hash of its parameters."""
    sig = filter_fn.signature() if hasattr(filter_fn, "signature") else ""
    return safe_filename(name) + (("_" + hashlib.md5(sig.encode("utf-8")).hexdigest()[:8]) if sig else "")


def run_round(round_tag, filters):
    results_round, t_round = [], time.time()
    for name, fn in filters:
        if name in SKIP_FILTERS:
            print(f"\n[{round_tag}] {name}: skipped (SKIP_FILTERS)")
            continue
        r = cached_result(name, fn)
        if r is not None:
            print(f"\n[{round_tag}] {name}: reusing the saved result ({os.path.basename(RESULT_CACHE_DIR)}/, REUSE_RESULTS = True)")
            print("  -> " + _result_line(r))
            results_round.append(r)
            continue
        print(f"\n[{round_tag}] {name} ...")
        t0 = time.time()
        if FILTER_MODE == "inference_only":
            r = evaluate_inference_only(name, fn, eval_items, yolo_model)
        elif FILTER_MODE == "train_per_filter":
            r = evaluate_cv(name, fn, eval_items) if USE_CV else evaluate_train_per_filter(name, fn, eval_items)
        else:
            raise ValueError(f"Unknown FILTER_MODE: {FILTER_MODE!r}")
        r["params"] = filter_params_str(fn)
        save_result(name, fn, r)
        results_round.append(r)
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        print("  -> " + _result_line(r) + f" | {(time.time() - t0) / 60:.1f} min")
        if r["pred_ng_pct"] >= 95 or r["pred_ng_pct"] <= 5:
            print("     WARNING: almost every image got the same judgement -> the detector collapsed (accuracy = class share, not skill)")
    print(f"\n{round_tag} finished in {(time.time() - t_round) / 60:.1f} min")
    return results_round