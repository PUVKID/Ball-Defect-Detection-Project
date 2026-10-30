# ── 28a. Where do the 'ghost' boxes of the remove-one test come from? ─────────────────────────────────
import re
RUN_DIAG = True
DIAG_MAX_IMAGES = None                          # None = every clean OK image; e.g. 120 for a quick look
GHOST_ERASE_METHODS = ["none", "telea", "ns", "ring"]
DIAG_SEED = VERIFY_SEED + 1


def erase_boxes_m(gray, boxes, method="telea", pad=0.3, seed=0):
    """Like erase_boxes, but the way a ball is painted over can be chosen:
    none = untouched image, telea / ns = two OpenCV inpainting algorithms, ring = noise with the mean / std of the ring around the ball."""
    if method == "none":
        return gray.copy()
    if method == "telea":
        return erase_boxes(gray, boxes, pad)
    out = gray.copy()
    H, W = gray.shape
    rng = np.random.default_rng(seed)
    for cx, cy, bw, bh in boxes:
        r = int(max(bw, bh) / 2 * (1 + pad)) + 1
        x0, x1 = max(0, int(cx) - 3 * r), min(W, int(cx) + 3 * r + 1)
        y0, y1 = max(0, int(cy) - 3 * r), min(H, int(cy) + 3 * r + 1)
        crop = np.ascontiguousarray(out[y0:y1, x0:x1])
        c = (int(cx) - x0, int(cy) - y0)
        m = np.zeros(crop.shape, np.uint8)
        cv2.circle(m, c, r, 255, -1)
        if method == "ns":
            out[y0:y1, x0:x1] = cv2.inpaint(crop, m, 5, cv2.INPAINT_NS)
        elif method == "ring":
            ring = np.zeros(crop.shape, np.uint8)
            cv2.circle(ring, c, int(r * 1.6) + 1, 255, -1)
            ring[m > 0] = 0
            vals = crop[ring > 0].astype(np.float32)
            if vals.size < 10:
                continue
            fill = rng.normal(float(vals.mean()), float(vals.std()), crop.shape)
            new = crop.copy()
            new[m > 0] = np.clip(fill[m > 0], 0, 255).astype(np.uint8)
            out[y0:y1, x0:x1] = new
        else:
            raise ValueError(method)
    return out


def run_ghost_diagnosis(items, methods=GHOST_ERASE_METHODS, seed=DIAG_SEED):
    """One ball per clean OK image is erased (site 'ball'); the same patch size is erased at a free spot (site 'free', control).
    found = a detection within 0.5 x ball size of the site."""
    rng = np.random.default_rng(seed)
    rows = []
    for it in tqdm(items, desc="ghost diagnosis", unit="img"):
        g = gt_by_key[it["key"]]
        if g["part"] is None or g["gt_pred"] != "OK":
            continue
        model = get_model("Original", identity_filter, FOLD_OF[it["key"]])
        if model is None:
            continue
        boxes = [tuple(b) for b in g["gt_boxes"]]
        inside = judge_boxes([(b[0], b[1]) for b in boxes], g["part"], (g["W"], g["H"]))["inside"]
        in_idx = [i for i, ins in enumerate(inside) if ins]
        if not in_idx:
            continue
        tb = boxes[int(rng.choice(in_idx))]
        size = max(tb[2], tb[3])
        free = pick_insert_xy(g["part"], boxes, rng, size)
        gray = cv2.imread(it["img"], cv2.IMREAD_GRAYSCALE)
        sites = [("ball", (tb[0], tb[1]))] + ([("free", free)] if free is not None else [])
        for meth in methods:
            for site, (sx, sy) in sites:
                img = erase_boxes_m(gray, [(sx, sy, tb[2], tb[3])], meth, seed=int(rng.integers(1 << 30)))
                xywh, conf = predict_gray(model, img)
                near = [float(c) for (x, y, _, _), c in zip(xywh, conf) if math.hypot(x - sx, y - sy) <= 0.5 * size]
                rows.append(dict(key=it["key"], method=meth, site=site, found=bool(near),
                                 conf=max(near) if near else 0.0, n_det=len(xywh)))
    return rows


def ghost_summary(rows):
    """(table of found-% per method x site, n per cell, verdict text)."""
    gdf = pd.DataFrame(rows)
    piv = 100.0 * gdf.pivot_table(index="method", columns="site", values="found", aggfunc="mean")
    n = gdf.groupby(["method", "site"]).size().unstack()
    piv = piv.reindex([m for m in GHOST_ERASE_METHODS if m in piv.index])
    er = [m for m in ("telea", "ns", "ring") if m in piv.index]
    ball = piv.loc[er, "ball"] if "ball" in piv else None
    free = piv.loc[er, "free"] if "free" in piv else None
    if ball is None or free is None or not er:
        return piv, n, "not enough data for a verdict"
    spread, gap = float(ball.max() - ball.min()), float((ball - free).min())
    if float(ball.max()) <= 2.0:
        v = "After erasing, a box at the erased spot is (almost) never found -> no ghost: the detector does not keep predicting balls where they were removed."
    elif gap <= 2.0:
        v = ("The boxes appear at free spots as often as at the erased ball -> they are generic false positives of the erased/inpainted look, "
             "not a memory of ball positions.")
    elif spread >= 5.0:
        v = ("The rate depends strongly on how the ball was erased (spread %.1f pp) -> the ghost is a residue of the ball / the inpainting, "
             "not a memory of positions." % spread)
    else:
        v = ("The rate is similar for every erase method (spread %.1f pp) and higher than at free spots (>= %.1f pp) -> a position prior is possible; "
             "do not claim the detector is purely appearance-based, report the number instead." % (spread, gap))
    return piv, n, v


GHOST_ROWS = []
if RUN_DIAG and not USE_CV:
    print("The diagnostics use the CV fold detectors (USE_CV = True) -> skipped.")
elif RUN_DIAG:
    _it = [it for it in eval_items if gt_by_key[it["key"]]["gt_pred"] == "OK" and gt_by_key[it["key"]]["part"] is not None]
    if DIAG_MAX_IMAGES and len(_it) > DIAG_MAX_IMAGES:
        _it = random.Random(DIAG_SEED).sample(_it, DIAG_MAX_IMAGES)
    GHOST_ROWS = run_ghost_diagnosis(_it)
    if GHOST_ROWS:
        _piv, _n, _verdict = ghost_summary(GHOST_ROWS)
        print("\n(28a) Detection within 0.5 x ball size of the erased site (%):")
        display(_piv.round(1))
        print("images per cell:")
        display(_n)
        _gdf = pd.DataFrame(GHOST_ROWS)
        print("mean confidence of those detections:", _gdf[_gdf.found].groupby(["method", "site"]).conf.mean().round(2).to_dict())
        print("\nVerdict:", _verdict)
        print("Reading guide: 'none'/'ball' is the untouched image (should be ~100 %: the ball itself); 'none'/'free' is the natural false-positive rate of the detector (should be ~0 %).")
        _gdf.to_csv(os.path.join(FILTER_FIG_DIR, "diag_ghost_rows.csv"), index=False, encoding="utf-8-sig")
        _piv.round(2).to_csv(os.path.join(FILTER_FIG_DIR, "diag_ghost_table.csv"), encoding="utf-8-sig")
    else:
        print("No usable images (no cached Original fold detectors?).")