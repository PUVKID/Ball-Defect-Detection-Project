# ── 26b. Distribution shift without retraining (clean-trained detectors, corrupted held-out images) ──
RUN_HARD_SHIFT = True
HARD_QUICK = False          # True: every second condition only
HARD_SHIFT_FILTERS = None   # None = Original + the 10 Round-1 filters (each with its own cached fold detectors)
HARD_SHIFT_CONDITIONS = [
    ("noise 40", dict(kind="noise", v=40)), ("noise 80", dict(kind="noise", v=80)),
    ("blur 8", dict(kind="blur", v=8)), ("blur 16", dict(kind="blur", v=16)),
    ("contrast x0.4", dict(kind="contrast", v=0.4)), ("contrast x0.2", dict(kind="contrast", v=0.2)),
    ("brightness +60", dict(kind="bright", v=60)), ("brightness -60", dict(kind="bright", v=-60)),
    ("down x4", dict(kind="down", v=4)), ("down x8", dict(kind="down", v=8)),
]

SHIFT_RESULTS = {}
if RUN_HARD_SHIFT and not USE_CV:
    print("The shift test uses the CV fold detectors (USE_CV = True) -> skipped.")
elif RUN_HARD_SHIFT:
    _methods = [("Original", identity_filter)] + [(n, f) for n, f in FILTERS_ROUND1 if HARD_SHIFT_FILTERS is None or n in HARD_SHIFT_FILTERS]
    _missing = [m for m, fn in _methods if any(get_model(m, fn, f) is None for f in sorted(set(FOLD_OF.values())))]
    if _missing:
        print(f"No cached fold detectors for {_missing} -> left out (run Sections 14-17 first).")
        _methods = [(m, fn) for m, fn in _methods if m not in _missing]
    _conds = HARD_SHIFT_CONDITIONS[::2] if HARD_QUICK else HARD_SHIFT_CONDITIONS
    _sig = hashlib.md5(json.dumps([CONF_THRES, IOU_THRES, CV_IMGSZ, FOLD_TAG, [m for m, _ in _methods], _conds], sort_keys=True).encode("utf-8")).hexdigest()[:8]
    print(f"Shift test: {len(_methods)} methods x {len(_conds)} conditions x {len(eval_items)} images (inference only)")
    SHIFT_RESULTS = run_shift(_methods, _conds, eval_items, os.path.join(FILTER_FIG_DIR, f"hard_shift_{_sig}.json"))

    labels = [lb for lb, _ in _conds]
    names_m = [m for m, _ in _methods]
    S = pd.DataFrame({lb: {m: SHIFT_RESULTS[lb][m]["strict"] for m in names_m} for lb in labels})
    A = pd.DataFrame({lb: {m: SHIFT_RESULTS[lb][m]["acc"] for m in names_m} for lb in labels})
    S["mean"], A["mean"] = S.mean(axis=1), A.mean(axis=1)
    S["vs Original"] = S["mean"] - S.loc["Original", "mean"]
    print("\nStrict accuracy (%) per condition (a gap below ~3 pp = 15 images is within noise):")
    display(S.round(1).sort_values("mean", ascending=False))
    print("Plain OK/NG accuracy (%):")
    display(A.round(1).sort_values("mean", ascending=False))
    S.round(2).to_csv(os.path.join(FILTER_FIG_DIR, "table_shift_strict.csv"), encoding="utf-8-sig")
    A.round(2).to_csv(os.path.join(FILTER_FIG_DIR, "table_shift_accuracy.csv"), encoding="utf-8-sig")

    _fig, _ax = plt.subplots(figsize=(1.0 * len(labels) + 5, 0.55 * len(names_m) + 2.5))
    _im = _ax.imshow(S[labels].values, cmap="RdYlGn", vmin=0, vmax=100, aspect="auto")
    _ax.set_xticks(range(len(labels)))
    _ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=12)
    _ax.set_yticks(range(len(names_m)))
    _ax.set_yticklabels(names_m, fontsize=12)
    for i in range(len(names_m)):
        for j in range(len(labels)):
            _ax.text(j, i, f"{S[labels].values[i, j]:.0f}", ha="center", va="center", fontsize=11, fontweight="bold")
    _fig.colorbar(_im, ax=_ax, label="Strict accuracy (%)")
    _fig.tight_layout()
    _p = os.path.join(FILTER_FIG_DIR, "fig_hard_shift_strict_heatmap.png")
    _fig.savefig(_p, dpi=300, bbox_inches="tight", facecolor="white")
    plt.show()
    print(f"Saved: {_p}")
