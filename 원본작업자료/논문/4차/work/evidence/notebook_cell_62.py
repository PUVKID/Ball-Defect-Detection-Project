# ── 26c. Combined stress WITH retraining (low data + noise), Original vs the filters that did best in 26b ──
RUN_HARD_RETRAIN = True
HARD_COND = dict(noise=40, frac=0.25, imgsz=None)     # between the plateau and the cliff of the single-factor sweeps
HARD_FILTERS = ["Gaussian Blur (max)", "Histogram Equalization", "CLAHE (max)", "Gamma 0.3", "Invert"]

HARD_RESULTS = []
if RUN_HARD_RETRAIN and not USE_CV:
    print("The hard retraining needs USE_CV = True -> skipped.")
elif RUN_HARD_RETRAIN:
    _tag = f"noise {HARD_COND['noise']:g}, data {int(round(100 * HARD_COND['frac']))}%" + (f", {HARD_COND['imgsz']}px" if HARD_COND["imgsz"] else "")
    _todo = [("Original", SAME)] + [(n, f) for n, f in FILTERS_ROUND1 if n in HARD_FILTERS and n not in SKIP_FILTERS]
    print(f"Hard retraining ({_tag}): {len(_todo)} methods x {len(_run_folds)} folds = {len(_todo) * len(_run_folds)} trainings")
    for fname, fn in _todo:
        nm = f"HARD {fname} | {_tag}"
        print(f"\n[Hard] {fname} ...")
        r = run_condition(nm, fn, **HARD_COND)
        r["label"] = fname
        r["hard_name"] = nm
        HARD_RESULTS.append(r)
        print("  -> " + _result_line(r))
        if r["pred_ng_pct"] >= 95 or r["pred_ng_pct"] <= 5:
            print("     WARNING: the detector collapsed onto one answer -> this level is too hard to compare methods (lower the noise or raise the data share)")
    ref_nm = HARD_RESULTS[0]["hard_name"]
    rows_h = []
    for r in HARD_RESULTS:
        b, c, p = (0, 0, 1.0) if r["hard_name"] == ref_nm else strict_mcnemar(ref_nm, r["hard_name"])
        rows_h.append({"Method": r["label"], "Accuracy (%)": r["accuracy"], "Strict Acc (%)": r["strict_acc"], "Ball Recall (%)": r["ball_recall"],
                       "mAP50-95 (%)": r["map50_95"], "Fold Acc Std (pp)": r["fold_std"], "Strict: newly worse": b, "Strict: newly better": c, "Strict McNemar p": p})
    hdf = pd.DataFrame(rows_h)
    print(f"\nHard mode ({_tag}); the McNemar test compares strict correctness with Original under the same condition:")
    display(hdf.round(3))
    hdf.to_csv(os.path.join(FILTER_FIG_DIR, "table_hard_retrain.csv"), index=False, encoding="utf-8-sig")
    print("\nPer difficulty stratum:")
    sdf = stratified_table([r["hard_name"] for r in HARD_RESULTS])
    sdf["Method"] = sdf["Method"].map({r["hard_name"]: r["label"] for r in HARD_RESULTS})
    display(sdf.round(1))
