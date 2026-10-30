import platform, datetime
_ver = lambda mod: getattr(sys.modules.get(mod), "__version__", "n/a")
environment = dict(
    date=datetime.datetime.now().isoformat(timespec="seconds"), python=platform.python_version(),
    torch=_ver("torch"), kornia=_ver("kornia"), ultralytics=_ver("ultralytics"),
    opencv=cv2.__version__, numpy=np.__version__,
    gpu=torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu",
    seed=SEED, conf=CONF_THRES, iou=IOU_THRES, imgsz=IMGSZ, weights=_weights_id(),
)
all_results = {"environment": environment, "filter_mode": FILTER_MODE, "run_preset": RUN_PRESET, "eval_splits": EVAL_SPLITS,
               "cv": dict(use=USE_CV, folds=CV_FOLDS, run_folds=_run_folds, val_frac=CV_VAL_FRAC, train_frac=STRESS_TRAIN_FRAC,
                          imgsz=CV_IMGSZ, noise_std=STRESS_NOISE_STD, filter_epochs=FILTER_EPOCHS),
               "n_images": len(eval_items), "baseline": baseline_result,
               "round1": results_round1, "round2": results_round2}
json_path = os.path.join(FILTER_FIG_DIR, "results_summary.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)

# combined table: Original + Round 1 + Round 2
df_all = pd.concat([
    df_round1.iloc[:1].assign(Round="Baseline"),
    df_round1.iloc[1:].assign(Round="Round 1"),
    df_round2.iloc[1:].assign(Round="Round 2"),
], ignore_index=True)
df_all.insert(0, "Round", df_all.pop("Round"))
csv_all = os.path.join(FILTER_FIG_DIR, "table_all.csv")
df_all.to_csv(csv_all, index=False, encoding="utf-8-sig")

# per-image predictions of every method (for error analysis and paired tests)
pi_path = os.path.join(FILTER_FIG_DIR, "per_image_predictions.csv")
pd.DataFrame([r for rows in PER_IMAGE.values() for r in rows]).to_csv(pi_path, index=False, encoding="utf-8-sig")
print(f"Saved: {json_path}\nSaved: {csv_all}\nSaved: {pi_path}")

# overview graph: overall accuracy of every method
ov = [baseline_result] + list(results_round1) + list(results_round2)
plot_clean_bar(
    labels=[r["name"] for r in ov], values=[r["accuracy"] for r in ov],
    xlabel="Filter", ylabel="Overall Accuracy (%)", save_name="fig_all_overview_overall_accuracy.png",
    value_fmt="{:.2f}%", ymax=110, rotation=35, figsize=(21, 7.5), value_fontsize=13,
    threshold=baseline_result["accuracy"], threshold_label=f"Original {baseline_result['accuracy']:.2f}%",
    out_dir=FILTER_FIG_DIR, legend_above=True,
)

print(f"\nRUN_PRESET = {RUN_PRESET}, {len(eval_items)} images per filter, splits = {EVAL_SPLITS}")
print(f"Original (no filter): accuracy {baseline_result['accuracy']:.2f}%  NG recall {baseline_result['ng_recall']:.2f}%")
for tag, rs in (("Round 1 - single filters", results_round1), ("Round 2 - combined filters", results_round2)):
    print(f"\n[{tag}] ranked by overall accuracy")
    _nz = lambda v: 0.0 if v is None or (isinstance(v, float) and math.isnan(v)) else v
    for r in sorted(rs, key=lambda x: (-x["accuracy"], -_nz(x.get("map50_95")))):     # accuracy ties -> mAP50-95 decides
        d = r["accuracy"] - baseline_result["accuracy"]
        extra = (f"  mAP50-95 {r['map50_95']:5.1f}%  ball recall {r['ball_recall']:6.2f}%  center err {r['loc_err_px']:5.2f}px"
                 if _nz(r.get("map50_95")) else "")
        print(f"  {r['name']:<24s} accuracy {r['accuracy']:6.2f}% ({d:+.2f} pp)  NG recall {r['ng_recall']:6.2f}%{extra}  "
              f"filter {r['avg_time_ms']:9.2f} ms/img")

# significance against Original (exact McNemar on the paired per-image judgements)
sig = [(r["name"], r["accuracy"] - baseline_result["accuracy"], r["newly_wrong"], r["newly_correct"], r["mcnemar_p"])
       for r in list(results_round1) + list(results_round2) if r.get("mcnemar_p") is not None]
if sig:
    bonf = 0.05 / len(sig)
    print(f"\n[Significance vs Original - exact McNemar test]   * p < 0.05   ** p < {bonf:.4f} (Bonferroni, {len(sig)} comparisons)")
    for nm, d, nw, nc, p in sorted(sig, key=lambda x: x[4]):
        mark = "**" if p < bonf else ("*" if p < 0.05 else "")
        print(f"  {nm:<24s} {d:+7.2f} pp   newly wrong {nw:4d} / newly correct {nc:4d}   p = {p:.4g} {mark}")

n_fig = len(round1_fig_paths) + len(round2_fig_paths)
n_samples = len(glob.glob(os.path.join(FILTER_SAMPLE_DIR, "*_example.png")))
print(f"\nGraphs: {n_fig} (+1 overview, +1 combination-vs-components) -> {os.path.abspath(FILTER_FIG_DIR)}")
n_grids = len(glob.glob(os.path.join(FILTER_SAMPLE_DIR, "grid_*.png")))
print(f"Original-vs-filtered example images: {n_samples} (+{n_grids} grid figures) -> {os.path.abspath(FILTER_SAMPLE_DIR)}")
