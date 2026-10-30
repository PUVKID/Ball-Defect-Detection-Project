COMBO_PARTS = ROUND2_COMBOS   # combined filter -> (first stage, second stage), defined in Section 10


def components_vs_combination():
    lookup = {r["name"]: r for r in results_round1}
    rows = []
    for r in results_round2:
        if r["name"] not in COMBO_PARTS:
            continue
        pa, pb = COMBO_PARTS[r["name"]]
        if pa not in lookup or pb not in lookup:
            continue                                  # a component was skipped
        ra, rb = lookup[pa], lookup[pb]
        best = ra if ra["accuracy"] >= rb["accuracy"] else rb
        _, _, p = mcnemar_between(best["name"], r["name"])
        gain = r["accuracy"] - best["accuracy"]
        rows.append({
            "Combination": r["name"], "Accuracy (%)": r["accuracy"],
            "Component A": pa, "A Acc. (%)": ra["accuracy"],
            "Component B": pb, "B Acc. (%)": rb["accuracy"],
            "Best Component": best["name"], "Gain vs Best Component (pp)": gain,
            "Verdict": "Combination better" if gain > 0 else ("Component better" if gain < 0 else "Tie"),
            "McNemar p vs Best Component": p,
            "Significant (p<0.05)": "-" if p is None else ("Yes" if p < 0.05 else "No"),
            "Combination F1 (%)": r["f1"], "Best Component F1 (%)": best["f1"],
        })
    df = pd.DataFrame(rows)
    return df.round({c: (4 if c.startswith("McNemar") else 2) for c in df.columns if df[c].dtype.kind == "f"})


def plot_components_vs_combination(df, save_name="fig_combo_vs_components.png"):
    x = np.arange(len(df))
    w = 0.27
    fig, ax = plt.subplots(figsize=(15, 6.8))
    series = [("Combination", df["Accuracy (%)"].values, [""] * len(df), "#1a9850"),
              ("Component A", df["A Acc. (%)"].values, df["Component A"].tolist(), "#fdae61"),
              ("Component B", df["B Acc. (%)"].values, df["Component B"].tolist(), "#74add1")]
    handles = []
    for k, (lab, vals, names, col) in enumerate(series):
        bars = ax.bar(x + (k - 1) * w, vals, width=w, color=col, edgecolor="none", zorder=3)
        handles.append(bars[0])
        for b, v, nm in zip(bars, vals, names):
            ax.text(b.get_x() + b.get_width() / 2, v + 0.6, f"{v:.1f}", ha="center", va="bottom",
                    fontsize=12, fontweight="bold", color="#1a1a1a")
            if nm:
                ax.text(b.get_x() + b.get_width() / 2, 2, nm, rotation=90, ha="center", va="bottom",
                        fontsize=11, fontweight="bold", color="#1a1a1a", zorder=4)
    base_acc = baseline_result["accuracy"]
    h = ax.axhline(base_acc, color="#888888", linestyle=":", linewidth=1.4, zorder=2)
    ax.set_xticks(x)
    ax.set_xticklabels(df["Combination"].tolist(), rotation=12)
    ax.set_xlabel("Combined Filter", fontsize=25, fontweight="bold")
    ax.set_ylabel("Overall Accuracy (%)", fontsize=25, fontweight="bold")
    ax.set_ylim(0, 115)
    ax.grid(axis="y", zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize=14)
    ax.tick_params(axis="y", labelsize=14)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_fontweight("bold")
    for spine in ax.spines.values():
        spine.set_color("#222222")
        spine.set_linewidth(0.9)
    leg = ax.legend(handles + [h], ["Combination", "Component A", "Component B", f"Original {base_acc:.2f}%"],
                    loc="lower right", bbox_to_anchor=(1.0, 1.01), ncol=4, frameon=True, fontsize=17)
    for text in leg.get_texts():
        text.set_fontweight("bold")
    fig.tight_layout()
    out_path = os.path.join(FILTER_FIG_DIR, save_name)
    fig.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.show()
    print(f"Saved: {out_path}")
    return out_path


df_combo = components_vs_combination()
if len(df_combo):
    show_and_save_table(df_combo, "combo_vs_components")
    plot_components_vs_combination(df_combo)
else:
    print("No combination has both of its components scored (check SKIP_FILTERS).")
