METRIC_SPECS = [
    dict(key="accuracy", ylabel="Overall Accuracy (%)", fname="01_overall_accuracy"),
    dict(key="top_acc", ylabel="Top Region Accuracy (%)", fname="02_top_region_accuracy"),
    dict(key="left_acc", ylabel="Left Region Accuracy (%)", fname="03_left_region_accuracy"),
    dict(key="bottom_acc", ylabel="Bottom Region Accuracy (%)", fname="04_bottom_region_accuracy"),
    dict(key="right_acc", ylabel="Right Region Accuracy (%)", fname="05_right_region_accuracy"),
    dict(key="ok_recall", ylabel="OK Class Accuracy (%)", fname="06_ok_class_accuracy"),
    dict(key="ng_recall", ylabel="NG Class Accuracy (%)", fname="07_ng_class_accuracy"),
    dict(key="precision", ylabel="Precision (%)", fname="08_precision"),
    dict(key="f1", ylabel="F1 Score (%)", fname="09_f1_score"),
    dict(key="avg_time_ms", ylabel="Avg Filter Time (ms/image)", fname="10_avg_filter_time", time_metric=True),
    # [added] continuous metrics that do not saturate at 100% (only drawn when the run produced them, i.e. in CV mode)
    dict(key="ball_recall", ylabel="Ball Recall (%)", fname="11_ball_recall"),
    dict(key="map50_95", ylabel="mAP50-95 (%)", fname="12_map50_95"),
    dict(key="min_conf", ylabel="Mean Min. Confidence (%)", fname="13_min_confidence"),
    dict(key="loc_err_px", ylabel="Mean Center Error (px)", fname="14_center_error", time_metric=True),
    dict(key="strict_acc", ylabel="Strict Accuracy (%)", fname="15_strict_accuracy"),   # [added v5]
]


def make_all_metric_plots(results_round, round_tag, baseline):
    names = [r["name"] for r in results_round]
    n_bars = len(names)
    paths = []
    for spec in METRIC_SPECS:
        values = [r.get(spec["key"]) for r in results_round]
        if any(v is None or (isinstance(v, float) and math.isnan(v)) for v in values + [baseline.get(spec["key"])]):
            continue                                  # metric not available in this run
        is_time = spec.get("time_metric", False)
        paths.append(plot_clean_bar(
            labels=names, values=values,
            xlabel="Filter", ylabel=spec["ylabel"], save_name=f"fig_{round_tag}_{spec['fname']}.png",
            value_fmt="{:.2f}" if is_time else "{:.2f}%",
            ymax=None if is_time else 110,
            threshold=None if is_time else baseline[spec["key"]],
            threshold_label=None if is_time else f"Original {baseline[spec['key']]:.2f}%",
            rotation=35 if n_bars >= 5 else 12,
            figsize=(13.5, 6.6) if n_bars >= 5 else (11, 5.8),
            higher_is_better=not is_time,
            out_dir=FILTER_FIG_DIR,
            legend_above=True,
            value_fontsize=14 if n_bars >= 8 else 17,   # 10 bars: 17 pt value labels touch each other
        ))
    return paths


TABLE_COLUMNS = [
    ("name", "Filter"), ("accuracy", "Accuracy (%)"),
    ("top_acc", "Top (%)"), ("left_acc", "Left (%)"), ("bottom_acc", "Bottom (%)"), ("right_acc", "Right (%)"),
    ("bal_acc", "Balanced Acc (%)"), ("pred_ng_pct", "Predicted NG (%)"), ("ok_recall", "OK Recall (%)"), ("ng_recall", "NG Recall (%)"), ("precision", "Precision (%)"), ("f1", "F1 (%)"),
    ("ball_recall", "Ball Recall (%)"), ("map50", "mAP50 (%)"), ("map50_95", "mAP50-95 (%)"), ("min_conf", "Min Conf (%)"),
    ("loc_err_px", "Center Err (px)"), ("extra_per_img", "Extra Det./img"), ("fold_std", "Fold Acc Std (pp)"),
    ("strict_acc", "Strict Acc (%)"), ("majority_acc", "Majority-class Baseline (%)"),
    ("ref_acc", "Acc vs OKNG_CSV (%)"), ("gt_vs_ref_acc", "Label Rule vs OKNG_CSV (%)"),
    ("avg_time_ms", "Filter Time (ms/img)"), ("yolo_time_ms", "YOLO Time (ms/img)"),
    ("newly_correct", "Newly Correct vs Original"), ("newly_wrong", "Newly Wrong vs Original"),
    ("mcnemar_p", "McNemar p vs Original"), ("params", "Parameters"),
]


def wilson_ci(k, n, z=1.96):
    """95% Wilson score interval (in %) for k successes out of n."""
    if n == 0:
        return 0.0, 0.0
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100 * (centre - half), 100 * (centre + half)


def results_to_df(results_round, baseline):
    """Table with the Original baseline as the first row."""
    rows = [baseline] + list(results_round)
    df = pd.DataFrame([{label: r.get(key) for key, label in TABLE_COLUMNS} for r in rows])
    df["Parameters"] = df["Parameters"].fillna("-")
    for col in ("Strict Acc (%)", "Majority-class Baseline (%)", "Acc vs OKNG_CSV (%)", "Label Rule vs OKNG_CSV (%)"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    if df["Acc vs OKNG_CSV (%)"].isna().all():            # no OKNG_CSV -> hide the two reference columns
        df = df.drop(columns=["Acc vs OKNG_CSV (%)", "Label Rule vs OKNG_CSV (%)"])
    df.insert(2, "Accuracy 95% CI", ["%.1f - %.1f" % wilson_ci(r["tp"] + r["tn"], r["n_images"]) for r in rows])
    df.insert(2, "Acc. change vs Original (pp)", df["Accuracy (%)"] - baseline["accuracy"])
    for col in ("Newly Correct vs Original", "Newly Wrong vs Original"):
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    df["McNemar p vs Original"] = pd.to_numeric(df["McNemar p vs Original"], errors="coerce")
    df["Significant (p<0.05)"] = ["-" if pd.isna(p) else ("Yes" if p < 0.05 else "No") for p in df["McNemar p vs Original"]]
    lead = ["Filter", "Parameters", "Accuracy (%)", "Accuracy 95% CI", "Acc. change vs Original (pp)", "Newly Correct vs Original",
            "Newly Wrong vs Original", "McNemar p vs Original", "Significant (p<0.05)"]
    df = df[lead + [col for col in df.columns if col not in lead]]
    return df.round({col: (4 if col == "McNemar p vs Original" else 2) for col in df.columns
                     if col not in ("Filter", "Parameters", "Accuracy 95% CI", "Significant (p<0.05)", "Newly Correct vs Original", "Newly Wrong vs Original")})


def show_and_save_table(df, round_tag):
    path = os.path.join(FILTER_FIG_DIR, f"table_{round_tag}.csv")
    df.to_csv(path, index=False, encoding="utf-8-sig")
    display(df)
    print(f"Saved: {path}")