RUN_FILTER_GRID = True
GRID_NOISE_LEVELS = [40, 80]
GRID_FILTER_NAMES = None          # e.g. ["Gaussian Blur (max)", "CLAHE (max)"]; None = all Round-1 filters

GRID_RESULTS = {}
if RUN_FILTER_GRID and not USE_CV:
    print("The grid needs USE_CV = True -> skipped.")
elif RUN_FILTER_GRID:
    _grid_filters = [(n, f) for n, f in FILTERS_ROUND1 if (GRID_FILTER_NAMES is None or n in GRID_FILTER_NAMES) and n not in SKIP_FILTERS]
    _n_new = len(GRID_NOISE_LEVELS) * len(_grid_filters) * len(_run_folds)
    print(f"Grid: {len(GRID_NOISE_LEVELS)} noise levels x {len(_grid_filters)} filters, {_n_new} trainings (roughly {_n_new * 2 / 60:.1f} h).")
    for nz in GRID_NOISE_LEVELS:
        ref = NOISE_BY_LEVEL.get(nz)
        if ref is None:
            ref = dict(run_condition(f"Noise std={nz:g}", SAME, nz, _BASE_COND["frac"], _BASE_COND["imgsz"]), label=f"noise {nz:g}")
        rs = []
        for fname, fn in _grid_filters:
            nm = f"{fname} | noise {nz:g}"
            print(f"\n[Grid noise {nz:g}] {fname} ...")
            r = run_condition(nm, fn, nz, _BASE_COND["frac"], _BASE_COND["imgsz"])
            r["newly_wrong"], r["newly_correct"], r["mcnemar_p"] = mcnemar_between(ref["name"], nm)
            print("  -> " + _result_line(r))
            rs.append(dict(r, label=fname))
        GRID_RESULTS[nz] = [dict(ref, label=f"Original (noise {nz:g})")] + rs
        print(f"\n[Grid noise {nz:g}] ranked by accuracy (baseline = unfiltered noisy images: {ref['accuracy']:.2f}%)")
        for r in sorted(rs, key=lambda x: -x["accuracy"]):
            print(f"  {r['label']:<24s} {r['accuracy']:6.2f}% ({r['accuracy'] - ref['accuracy']:+6.2f} pp)  mAP50-95 {r['map50_95']:5.1f}%")