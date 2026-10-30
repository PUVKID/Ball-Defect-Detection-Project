# ── 28b. Shortcut diagnosis: balls or global shooting condition? ───────────────────────────────────────
def thumb_cv(items, loader, size=32, C=0.05):
    """Image-level classifier (logistic regression on a size x size thumbnail, no localisation) scored on the SAME folds as the detector.
    Returns (pred NG bool array, y NG bool array) or None when scikit-learn is missing."""
    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler
    except ImportError:
        print("scikit-learn is not installed (pip install scikit-learn) -> skipped")
        return None
    X = np.array([cv2.resize(loader(it), (size, size), interpolation=cv2.INTER_AREA).astype(np.float32).ravel() for it in items])
    y = np.array([gt_by_key[it["key"]]["gt_pred"] == "NG" for it in items])
    fold = np.array([FOLD_OF[it["key"]] for it in items])
    pred = np.zeros(len(y), bool)
    for f in sorted(set(fold)):
        tr, te = fold != f, fold == f
        if len(set(y[tr])) < 2:
            pred[te] = bool(y[tr][0])
            continue
        clf = make_pipeline(StandardScaler(), LogisticRegression(C=C, max_iter=3000, class_weight="balanced"))
        clf.fit(X[tr], y[tr])
        pred[te] = clf.predict(X[te])
    return pred, y


def _acc_bal(pred, y):
    rec_ng = (pred & y).sum() / max(y.sum(), 1)
    rec_ok = (~pred & ~y).sum() / max((~y).sum(), 1)
    return 100.0 * (pred == y).mean(), 50.0 * (rec_ng + rec_ok)


def stratum_acc(items, pred, y):
    """Accuracy (%) of an image-level classifier per difficulty stratum + n."""
    out = {}
    strata = np.array([difficulty_of(it["key"]) for it in items])
    for d in STRAT_ORDER:
        sel = strata == d
        out[d] = (100.0 * (pred[sel] == y[sel]).mean() if sel.any() else float("nan"), int(sel.sum()))
    return out


def load_raw(it):
    return cv2.imread(it["img"], cv2.IMREAD_GRAYSCALE)


def load_erased(it):
    g = gt_by_key[it["key"]]
    return erase_boxes(load_raw(it), [tuple(b) for b in g["gt_boxes"]])


def _rank_auc_perm(x, y, n_perm=2000, seed=0):
    """AUC of feature x for the label y (True = NG) from ranks, and a two-sided permutation p-value. NaNs are dropped."""
    x, y = np.asarray(x, float), np.asarray(y, bool)
    ok = ~np.isnan(x)
    x, y = x[ok], y[ok]
    n1, n0 = int(y.sum()), int((~y).sum())
    if n1 == 0 or n0 == 0 or len(x) < 10:
        return float("nan"), float("nan"), len(x)
    r = pd.Series(x).rank(method="average").to_numpy()
    base = n1 * (n1 + 1) / 2.0
    auc = (r[y].sum() - base) / (n1 * n0)
    rng = np.random.default_rng(seed)
    cnt = 0
    for _ in range(n_perm):
        a = (r[rng.permutation(y)].sum() - base) / (n1 * n0)
        cnt += abs(a - 0.5) >= abs(auc - 0.5) - 1e-12
    return float(auc), float((cnt + 1) / (n_perm + 1)), len(x)


def global_features(items):
    """Features that say nothing about single balls: file number, file time, global brightness, size / position of the part."""
    feats = {k: [] for k in ("file number", "file time", "mean gray", "gray std", "part area share", "part centre x", "part centre y")}
    for it in items:
        g = gt_by_key[it["key"]]
        num = re.findall(r"\d+", it["stem"])
        feats["file number"].append(float(num[0]) if num else float("nan"))
        try:
            feats["file time"].append(float(os.path.getmtime(it["img"])))
        except OSError:
            feats["file time"].append(float("nan"))
        gray = load_raw(it)
        feats["mean gray"].append(float(gray.mean()))
        feats["gray std"].append(float(gray.std()))
        part = g["part"]
        feats["part area share"].append(float("nan") if part is None else float(part["area_frac"]))
        feats["part centre x"].append(float("nan") if part is None else float(part["cx"]) / g["W"])
        feats["part centre y"].append(float("nan") if part is None else float(part["cy"]) / g["H"])
    return {k: np.array(v, float) for k, v in feats.items()}


SHORTCUT_DIAG = {}
if RUN_DIAG and not USE_CV:
    pass
elif RUN_DIAG:
    print("(28b-1) image-level classifier on raw vs ball-erased images (same folds as the detector)")
    _items = CV_ITEMS
    _raw = thumb_cv(_items, load_raw)
    if _raw is not None:
        _t0 = time.time()
        _ers = thumb_cv(_items, load_erased)
        print(f"   erased-image classifier finished ({time.time() - _t0:.0f} s)")
        _y = _raw[1]
        _rows = []
        for nm, (pr, _) in (("raw 32x32 thumbnail", _raw), ("all balls inpainted away", _ers)):
            a, b = _acc_bal(pr, _y)
            sa = stratum_acc(_items, pr, _y)
            _rows.append(dict(Input=nm, **{"Accuracy (%)": a, "Balanced (%)": b}, **{f"{d} (n={sa[d][1]})": sa[d][0] for d in STRAT_ORDER}))
        _sdf = pd.DataFrame(_rows)
        display(_sdf.round(1))
        _sdf.to_csv(os.path.join(FILTER_FIG_DIR, "diag_shortcut_thumbnail.csv"), index=False, encoding="utf-8-sig")
        SHORTCUT_DIAG["thumbnail"] = _rows
        _b_raw, _b_ers = _rows[0]["Balanced (%)"], _rows[1]["Balanced (%)"]
        if _b_ers >= _b_raw - 5:
            print(f"   -> erasing the balls barely changes the score ({_b_raw:.1f}% -> {_b_ers:.1f}%): the classifier does NOT need the balls, "
                  "the label is predictable from the rest of the image (global shooting condition / part appearance).")
        elif _b_ers <= 60:
            print(f"   -> without the balls the classifier falls to ~chance ({_b_ers:.1f}%): the thumbnail classifier of v6 was reading the balls.")
        else:
            print(f"   -> partly: {_b_raw:.1f}% -> {_b_ers:.1f}%; part of the signal is in the balls, part elsewhere.")
        print("   caveat: inpainting leaves a trace per erased ball, so an erased OK image (13 traces) differs slightly from an erased NG image (11-15 traces).")

    print("\n(28b-2) can the label be predicted from global features alone? (AUC 0.5 = no information; permutation p, 2000 shuffles)")
    _feat = global_features(CV_ITEMS)
    _yy = np.array([gt_by_key[it["key"]]["gt_pred"] == "NG" for it in CV_ITEMS])
    _rows = []
    for k, x in _feat.items():
        auc, p, n_ = _rank_auc_perm(x, _yy)
        _rows.append({"Feature": k, "n": n_, "AUC (NG vs OK)": auc, "|AUC-0.5|x2": abs(auc - 0.5) * 2 if not math.isnan(auc) else float("nan"), "perm. p": p})
    _adf = pd.DataFrame(_rows)
    display(_adf.round(3))
    _adf.to_csv(os.path.join(FILTER_FIG_DIR, "diag_global_feature_auc.csv"), index=False, encoding="utf-8-sig")
    SHORTCUT_DIAG["global_auc"] = _rows
    _strong = [r for r in _rows if r["perm. p"] < 0.01 and abs(r["AUC (NG vs OK)"] - 0.5) >= 0.1]
    if _strong:
        print("   -> label-related global features: " + ", ".join(f"{r['Feature']} (AUC {r['AUC (NG vs OK)']:.2f})" for r in _strong)
              + " -> OK and NG images differ in more than the balls (shooting order / lighting / part placement).")
    else:
        print("   -> no global feature separates OK from NG (all |AUC-0.5| < 0.1 or p >= 0.01).")