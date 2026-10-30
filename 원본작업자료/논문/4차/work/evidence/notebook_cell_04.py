# ── Common plot function (same style as plot_clean_bar in paper_figures_resnet50.ipynb) ──
def _bar_colors(values, vmin=None, vmax=None, cmap_name="RdYlGn"):
    vals = np.asarray(values, dtype=float)
    lo = vmin if vmin is not None else np.nanmin(vals)
    hi = vmax if vmax is not None else np.nanmax(vals)
    if hi - lo == 0:
        norm_vals = np.ones_like(vals) * 0.6
    else:
        norm_vals = (vals - lo) / (hi - lo)
        norm_vals = 0.15 + np.clip(norm_vals, 0, 1) * 0.75
    cmap = plt.get_cmap(cmap_name)
    return [cmap(v) for v in norm_vals]


def plot_clean_bar(
    labels, values, xlabel, ylabel, save_name,
    value_fmt="{:.1f}%", ymax=None, ymin=0,
    show_max=True, show_min=True,
    threshold=None, threshold_label=None,
    figsize=(11, 5.6), rotation=0,
    value_fontsize=17,
    higher_is_better=True,
    out_dir=None,
    legend_above=False,   # [added] True: legend row above the axes (so it never covers the value labels); False = original behaviour
):
    values = np.asarray(values, dtype=float)
    if higher_is_better:
        colors = _bar_colors(values)
    else:
        colors = _bar_colors(values, vmin=np.nanmax(values), vmax=np.nanmin(values))

    fig, ax = plt.subplots(figsize=figsize)
    bars = ax.bar(labels, values, color=colors, edgecolor="none", zorder=3, width=0.62)

    pad = (np.nanmax(values) - np.nanmin(values)) * 0.02 + 0.4
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width() / 2, v + pad, value_fmt.format(v),
                ha="center", va="bottom", fontsize=value_fontsize, fontweight="bold", color="#1a1a1a")

    handles, labels_leg = [], []
    if show_max:
        mx = np.nanmax(values)
        h = ax.axhline(mx, color="#e05a5a", linestyle="--", linewidth=1.4, zorder=2)
        handles.append(h); labels_leg.append(f"Max {mx:.1f}{'%' if '%' in value_fmt else ''}")
    if show_min:
        mn = np.nanmin(values)
        h = ax.axhline(mn, color="#2f9e8f", linestyle="--", linewidth=1.4, zorder=2)
        handles.append(h); labels_leg.append(f"Min {mn:.1f}{'%' if '%' in value_fmt else ''}")
    if threshold is not None:
        h = ax.axhline(threshold, color="#888888", linestyle=":", linewidth=1.4, zorder=2)
        handles.append(h); labels_leg.append(threshold_label or f"{threshold} Threshold")

    ax.set_xlabel(xlabel, fontsize=25, fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=25, fontweight="bold")
    top = ymax if ymax is not None else np.nanmax(values) * 1.18
    ax.set_ylim(ymin, top)
    ax.grid(axis="y", zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelrotation=rotation, labelsize=14)
    ax.tick_params(axis="y", labelsize=14)
    for lbl in ax.get_xticklabels():
        lbl.set_fontweight("bold")
    for lbl in ax.get_yticklabels():
        lbl.set_fontweight("bold")
    for spine in ax.spines.values():
        spine.set_color("#222222")
        spine.set_linewidth(0.9)
    if handles:
        if legend_above:
            leg = ax.legend(handles, labels_leg, loc="lower right", bbox_to_anchor=(1.0, 1.01), ncol=len(handles),
                            frameon=True, fontsize=19)
        else:
            leg = ax.legend(handles, labels_leg, loc="upper right", frameon=True, fontsize=19)
        for text in leg.get_texts():
            text.set_fontweight("bold")

    fig.tight_layout()
    out_path = os.path.join(out_dir or FIG_DIR, save_name)
    fig.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.show()
    print(f"Saved: {out_path}")
    return out_path