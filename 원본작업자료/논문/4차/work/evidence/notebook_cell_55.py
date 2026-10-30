from matplotlib.gridspec import GridSpec

SHOW_INLINE = True
GRAPH_THEME = "light"     # "light" = the style of the rest of this notebook; "dark" = the dark style of the ResNet50 reference notebook
DARK_RC = {
    "figure.facecolor": "#0d1117", "axes.facecolor": "#161b22", "axes.edgecolor": "#444", "axes.labelcolor": "#aaa",
    "xtick.color": "#aaa", "ytick.color": "#aaa", "grid.color": "#333", "grid.linestyle": "--", "grid.alpha": 0.5,
    "legend.facecolor": "#222", "legend.labelcolor": "white", "text.color": "white",
}


def diagnose_fit_yolo(h):
    """'good' | 'overfit' | 'underfit' | 'unknown' from one fold's YOLO curves (box loss + mAP50-95 on 0-1)."""
    tl, vl, mp = h.get("loss") or [], h.get("val_loss") or [], h.get("map50_95") or []
    if not tl or not vl:
        return "unknown"
    if (mp[-1] if mp else 0.0) < 0.30:
        return "underfit"
    if vl[-1] > 1.25 * min(vl) and (vl[-1] - tl[-1]) > 0.25 * tl[-1]:
        return "overfit"
    return "good"


def _pad_stack(hists, key):
    series = [list(h[key]) for h in hists if h.get(key)]
    if not series:
        return None
    L = max(len(s) for s in series)
    return np.array([s + [s[-1]] * (L - len(s)) for s in series], dtype=float)


def make_reference_graphs(group_key, results, title, xlabel, show_gpu=True):
    """results[0] = baseline of the group. Returns the list of saved PNG paths."""
    out_dir = os.path.join(FILTER_FIG_DIR, f"ref_graphs_{group_key}")
    os.makedirs(out_dir, exist_ok=True)
    n = len(results)
    labels = [r.get("label", r["name"]) for r in results]
    col = lambda k: np.array([np.nan if r.get(k) is None else r[k] for r in results], dtype=float)
    accs, ok_rec, ng_rec, ball, mapv, minc = (col(k) for k in ("accuracy", "ok_recall", "ng_recall", "ball_recall", "map50_95", "min_conf"))
    COLORS = [plt.cm.plasma(i / max(n - 1, 1)) for i in range(n)]
    C3 = ["#4CAF50", "#F44336", "#2196F3"]
    CLS = ["OK", "NG", "Ball detection"]
    fold_n = max(len(r.get("fold_acc") or []) for r in results)
    tag, saved = f"[{group_key}]", []
    wfig = max(13, 0.8 * n + 7)

    def savefig(name, show=True):
        path = os.path.join(out_dir, name)
        plt.savefig(path, dpi=150, bbox_inches="tight", facecolor=plt.rcParams["figure.facecolor"])
        plt.show() if (SHOW_INLINE and show) else plt.close()
        print(f"  saved: {path}")
        saved.append(path)

    def xt(ax, rot=25, fs=9):
        ax.set_xticks(range(n)); ax.set_xticklabels(labels, fontsize=fs, rotation=rot, ha="right")

    dark = GRAPH_THEME == "dark"
    TXT, GOLD = ("white", "#FFD700") if dark else ("#222222", "#c99700")
    with plt.rc_context(DARK_RC if dark else {}):
        # 1 ─ overall accuracy
        print(f"\n{tag} [graph 1/10] overall accuracy by {title}")
        fig, ax = plt.subplots(figsize=(wfig, 5))
        bars = ax.bar(range(n), accs, color=COLORS, edgecolor="#555", linewidth=0.8, zorder=3)
        ax.plot(range(n), accs, "o--", color=GOLD, lw=1.8, ms=7, zorder=4)
        for b, a in zip(bars, accs):
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.5, f"{a:.1f}%", ha="center", va="bottom", fontsize=9.5, color=TXT, fontweight="bold")
        ax.axhline(np.nanmean(accs), color="#FF6B6B", ls="--", lw=1.5, label=f"mean {np.nanmean(accs):.1f}%")
        ax.set_xlabel(xlabel, fontsize=12); ax.set_ylabel("Held-out accuracy (%)", fontsize=12)
        ax.set_title(f"OK/NG judgement accuracy by {title}\n(YOLOv8n | {CV_FOLDS}-fold CV | {results[0]['n_images']} images)", fontsize=14, fontweight="bold")
        ax.set_ylim(max(0, np.nanmin(accs) - 10), min(105, np.nanmax(accs) + 8)); ax.legend(fontsize=10); ax.grid(axis="y", zorder=0)
        xt(ax); plt.tight_layout(); savefig("01_overall_accuracy.png")

        # 2 ─ per-class accuracy
        print(f"\n{tag} [graph 2/10] accuracy per class")
        fig, ax = plt.subplots(figsize=(wfig + 1, 5.5)); width = 0.27; x = np.arange(n)
        for ci, (vals, c) in enumerate(zip((ok_rec, ng_rec, ball), C3)):
            rects = ax.bar(x + (ci - 1) * width, vals, width, label=CLS[ci], color=c, alpha=0.85, edgecolor="#555", linewidth=0.6)
            for rc, v in zip(rects, vals):
                ax.text(rc.get_x() + rc.get_width() / 2, rc.get_height() + 0.3, f"{v:.0f}", ha="center", va="bottom", fontsize=7.5, color=TXT)
        xt(ax, fs=9); ax.set_xlabel(xlabel, fontsize=12); ax.set_ylabel("Accuracy (%)", fontsize=12)
        ax.set_title("Accuracy per class (OK / NG / ball detection)", fontsize=14, fontweight="bold")
        ax.legend(fontsize=10, ncol=3, loc="lower right", bbox_to_anchor=(1.0, 1.01)); ax.grid(axis="y"); ax.set_ylim(0, 115); plt.tight_layout(); savefig("02_per_class_accuracy.png")

        # 3 ─ accuracy vs mAP50-95 (dual axis)
        print(f"\n{tag} [graph 3/10] mAP50-95 vs accuracy (dual axis)")
        fig, ax1 = plt.subplots(figsize=(wfig, 5)); ax2 = ax1.twinx()
        ax1.plot(range(n), accs, "o-", color="#4FC3F7", lw=2.2, ms=8, label="Accuracy (%)", zorder=4)
        ax2.plot(range(n), mapv, "s--", color="#FFB74D", lw=2.0, ms=7, label="mAP50-95 (%)", zorder=4)
        ax1.fill_between(range(n), accs, alpha=0.15, color="#4FC3F7"); ax2.fill_between(range(n), mapv, alpha=0.12, color="#FFB74D")
        ax1.set_xlabel(xlabel, fontsize=12); ax1.set_ylabel("Accuracy (%)", fontsize=12, color="#4FC3F7"); ax2.set_ylabel("mAP50-95 (%)", fontsize=12, color="#FFB74D")
        xt(ax1); ax1.set_title(f"mAP50-95 vs accuracy by {title}", fontsize=14, fontweight="bold")
        l1, b1 = ax1.get_legend_handles_labels(); l2, b2 = ax2.get_legend_handles_labels()
        ax1.legend(l1 + l2, b1 + b2, fontsize=10, loc="lower left"); ax1.grid(axis="y"); plt.tight_layout(); savefig("03_map_vs_accuracy.png")

        # 4 ─ confusion matrices (baseline vs hardest)
        print(f"\n{tag} [graph 4/10] confusion matrices (baseline vs hardest condition)")
        hard = int(np.nanargmin(accs[1:])) + 1 if n > 1 else 0
        pair = [0] if hard == 0 else [0, hard]
        fig, axes = plt.subplots(1, len(pair), figsize=(6 * len(pair), 5.5)); axes = np.atleast_1d(axes)
        for ax, idx in zip(axes, pair):
            r = results[idx]; cm = np.array([[r["tn"], r["fp"]], [r["fn"], r["tp"]]]); cmn = cm / (cm.sum(axis=1, keepdims=True) + 1e-9)
            im = ax.imshow(cmn, cmap="Blues", vmin=0, vmax=1)
            for i in range(2):
                for j in range(2):
                    ax.text(j, i, f"{cm[i, j]}\n({cmn[i, j] * 100:.1f}%)", ha="center", va="center", fontsize=10, color="white" if cmn[i, j] > 0.55 else ("#ccc" if dark else "#222222"))
            ax.set_xticks([0, 1]); ax.set_xticklabels(["OK", "NG"]); ax.set_yticks([0, 1]); ax.set_yticklabels(["OK", "NG"])
            ax.set_xlabel("Predicted class", fontsize=11); ax.set_ylabel("True class", fontsize=11)
            ax.set_title(f"Confusion matrix - {labels[idx]}\nAccuracy: {r['accuracy']:.1f}%", fontsize=12, fontweight="bold")
            plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        plt.suptitle("Confusion matrices: baseline vs hardest condition", fontsize=14, fontweight="bold", y=1.01); plt.tight_layout(); savefig("04_confusion_matrices.png")

        # 5 ─ learning curves of the baseline
        print(f"\n{tag} [graph 5/10] learning curves of the baseline (mean over folds)")
        hs = list((results[0].get("histories") or {}).values())
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        if hs:
            for key, color, lab in (("map50", "#4FC3F7", "mAP50"), ("map50_95", "#FFB74D", "mAP50-95")):
                m = _pad_stack(hs, key)
                if m is not None:
                    mean, std, ep = m.mean(0) * 100, m.std(0) * 100, range(1, m.shape[1] + 1)
                    ax1.plot(ep, mean, color=color, lw=2, label=f"val {lab}"); ax1.fill_between(ep, mean - std, mean + std, alpha=0.2, color=color)
            for key, color, lab in (("loss", "#4FC3F7", "train"), ("val_loss", "#FFB74D", "val")):
                m = _pad_stack(hs, key)
                if m is not None:
                    mean, std, ep = m.mean(0), m.std(0), range(1, m.shape[1] + 1)
                    ax2.plot(ep, mean, color=color, lw=2, label=f"{lab} box loss"); ax2.fill_between(ep, mean - std, mean + std, alpha=0.2, color=color)
        else:
            for ax in (ax1, ax2):
                ax.text(0.5, 0.5, "results.csv not found", ha="center", va="center", transform=ax.transAxes)
        ax1.set_title(f"Validation mAP - {labels[0]}\n(mean ± std over {len(hs)} folds)", fontsize=12, fontweight="bold")
        ax1.set_xlabel("Epoch"); ax1.set_ylabel("mAP (%)"); ax2.set_title(f"Box loss - {labels[0]}\n(mean ± std over {len(hs)} folds)", fontsize=12, fontweight="bold")
        ax2.set_xlabel("Epoch"); ax2.set_ylabel("box loss")
        for ax in (ax1, ax2):
            ax.grid()
            if hs: ax.legend()
        plt.tight_layout(); savefig("05_learning_curves_baseline.png")

        # 6 ─ heat map level x fold
        print(f"\n{tag} [graph 6/10] heat map condition x fold")
        hm = np.full((n, max(fold_n, 1)), np.nan)
        for i, r in enumerate(results):
            fa = r.get("fold_acc") or []
            hm[i, :len(fa)] = fa
        fig, ax = plt.subplots(figsize=(max(8, 1.6 * hm.shape[1] + 4), max(4, 0.55 * n + 2)))
        vmin = min(50, np.floor(np.nanmin(hm) - 5)) if np.isfinite(hm).any() else 50
        im = ax.imshow(hm, cmap="RdYlGn", aspect="auto", vmin=vmin, vmax=100)
        for i in range(hm.shape[0]):
            for j in range(hm.shape[1]):
                if np.isfinite(hm[i, j]):
                    ax.text(j, i, f"{hm[i, j]:.1f}", ha="center", va="center", fontsize=9, color="black" if 60 < hm[i, j] < 95 else "white")
        ax.set_xticks(range(hm.shape[1])); ax.set_xticklabels([f"Fold {k + 1}" for k in range(hm.shape[1])], fontsize=10)
        ax.set_yticks(range(n)); ax.set_yticklabels(labels, fontsize=9); ax.set_xlabel("Fold", fontsize=12); ax.set_ylabel(xlabel, fontsize=12)
        ax.set_title(f"Held-out accuracy (%) by {title} and fold", fontsize=14, fontweight="bold"); plt.colorbar(im, ax=ax, label="Accuracy (%)")
        plt.tight_layout(); savefig("06_heatmap_accuracy_by_fold.png")

        # 7 ─ over / under-fit verdicts
        print(f"\n{tag} [graph 7/10] over/under-fit verdicts")
        good, over, under = [], [], []
        for r in results:
            st = [diagnose_fit_yolo(h) for h in (r.get("histories") or {}).values()]
            good.append(st.count("good")); over.append(st.count("overfit")); under.append(st.count("underfit"))
        fig, ax = plt.subplots(figsize=(wfig, 5)); x = np.arange(n)
        p1 = ax.bar(x, good, color="#4CAF50", label="good"); ax.bar(x, over, bottom=good, color="#F44336", label="overfit")
        ax.bar(x, under, bottom=[g + o for g, o in zip(good, over)], color="#FFC107", label="underfit")
        for b, v in zip(p1, good):
            if v > 0: ax.text(b.get_x() + b.get_width() / 2, v / 2, str(v), ha="center", va="center", fontsize=10, color="white", fontweight="bold")
        xt(ax); ax.set_xlabel(xlabel, fontsize=12); ax.set_ylabel(f"Folds (of {fold_n})", fontsize=12)
        ax.set_title(f"Over/under-fit verdict by {title}\n({fold_n} folds, judged from the loss and mAP curves)", fontsize=14, fontweight="bold")
        ax.legend(fontsize=10); ax.grid(axis="y"); ax.set_ylim(0, fold_n + 2); plt.tight_layout(); savefig("07_fit_diagnosis.png")

        # 8 ─ radar
        print(f"\n{tag} [graph 8/10] radar chart")
        rad = list(dict.fromkeys([0, n // 2, hard])) if n > 2 else list(range(n))
        names = ["Accuracy", "OK accuracy", "NG accuracy", "Ball detection", "mAP50-95", "Min. confidence"]
        ang = [k / float(len(names)) * 2 * np.pi for k in range(len(names))]; ang += ang[:1]
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        for idx, color in zip(rad, ["#4FC3F7", "#FFB74D", "#F06292"]):
            r = results[idx]; v = [r.get(k) if r.get(k) is not None else 0.0 for k in ("accuracy", "ok_recall", "ng_recall", "ball_recall", "map50_95", "min_conf")]
            v = [0.0 if (isinstance(a, float) and np.isnan(a)) else a for a in v]; v += v[:1]
            ax.plot(ang, v, "o-", lw=2, color=color, label=labels[idx]); ax.fill(ang, v, alpha=0.1, color=color)
        ax.set_xticks(ang[:-1]); ax.set_xticklabels(names, fontsize=10); ax.set_ylim(0, 110); ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=8, color="#aaa")
        ax.set_title(f"Radar chart - {title}", fontsize=14, fontweight="bold", pad=20)
        ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.15), fontsize=10); plt.tight_layout(); savefig("08_radar_chart.png")

        # 9 ─ GPU timeline
        print(f"\n{tag} [graph 9/10] GPU timeline")
        if GPU_LOG:
            t = [(g["time"] - GPU_LOG[0]["time"]) / 60 for g in GPU_LOG]
            fig, (a1, a2, a3) = plt.subplots(3, 1, figsize=(14, 9), sharex=True)
            a1.plot(t, [g["used_mib"] for g in GPU_LOG], color="#4FC3F7", lw=1.8); a1.fill_between(t, [g["used_mib"] for g in GPU_LOG], alpha=0.2, color="#4FC3F7")
            a1.axhline(GPU_LOG[0]["total_mib"] * 0.90, color="#F44336", ls="--", lw=1.2, label="warning line (90%)")
            a1.set_ylabel("VRAM used (MiB)", fontsize=11); a1.legend(fontsize=9); a1.grid(); a1.set_title("GPU VRAM usage timeline (whole notebook run)", fontsize=13, fontweight="bold")
            a2.plot(t, [g["util_pct"] for g in GPU_LOG], color="#FFB74D", lw=1.8); a2.fill_between(t, [g["util_pct"] for g in GPU_LOG], alpha=0.2, color="#FFB74D")
            a2.set_ylabel("GPU utilisation (%)", fontsize=11); a2.grid(); a2.set_ylim(0, 110)
            a3.plot(t, [g["temp_c"] for g in GPU_LOG], color="#F06292", lw=1.8); a3.fill_between(t, [g["temp_c"] for g in GPU_LOG], alpha=0.2, color="#F06292")
            a3.axhline(85, color="#F44336", ls="--", lw=1.2, label="temperature warning (85°C)"); a3.set_ylabel("GPU temperature (°C)", fontsize=11)
            a3.set_xlabel("Elapsed time (min)", fontsize=12); a3.legend(fontsize=9); a3.grid(); plt.tight_layout(); savefig("09_gpu_timeline.png", show=show_gpu)
        else:
            print("  (GPU_LOG is empty: the nvidia-smi sampler did not run -> graph 9 skipped; no simulated data is drawn)")

        # 10 ─ dashboard
        print(f"\n{tag} [graph 10/10] dashboard")
        fig = plt.figure(figsize=(max(18, 0.9 * n + 12), 11)); gs = GridSpec(2, 3, figure=fig, hspace=0.55, wspace=0.35)
        a = fig.add_subplot(gs[0, 0]); a.plot(range(n), accs, "o-", color="#4FC3F7", lw=2.2, ms=7); a.fill_between(range(n), accs, alpha=0.2, color="#4FC3F7")
        for i, v in enumerate(accs): a.text(i, v + 0.5, f"{v:.1f}", ha="center", fontsize=8, color=TXT)
        a.set_title("1) Overall accuracy", fontsize=11, fontweight="bold"); a.set_ylabel("Accuracy (%)"); a.grid(); xt(a, fs=8)
        a = fig.add_subplot(gs[0, 1]); a.bar(range(n), mapv, color=COLORS, edgecolor="#555", linewidth=0.6)
        a.set_ylim(max(0, np.nanmin(mapv) - 5), min(105, np.nanmax(mapv) + 5)); a.set_title("2) mAP50-95 (%)", fontsize=11, fontweight="bold"); a.grid(axis="y"); xt(a, fs=8)
        for i, v in enumerate(mapv): a.text(i, v + 0.3, f"{v:.1f}", ha="center", fontsize=8, color=TXT)
        a = fig.add_subplot(gs[0, 2]); mat = np.vstack([ok_rec, ng_rec, ball]).T
        im = a.imshow(mat, cmap="YlGn", aspect="auto", vmin=max(0, np.nanmin(mat) - 10), vmax=100)
        a.set_xticks(range(3)); a.set_xticklabels(["OK", "NG", "Ball"], fontsize=8); a.set_yticks(range(n)); a.set_yticklabels(labels, fontsize=8)
        for i in range(n):
            for j in range(3): a.text(j, i, f"{mat[i, j]:.0f}", ha="center", va="center", fontsize=8, color="white" if (mat[i, j] >= 90 or mat[i, j] < 40) else "black")
        a.set_title("3) Per-class accuracy (%)", fontsize=11, fontweight="bold"); plt.colorbar(im, ax=a, fraction=0.046, pad=0.04)
        a = fig.add_subplot(gs[1, 0])
        if hs:
            m = _pad_stack(hs, "map50_95"); ml = _pad_stack(hs, "val_loss")
            if m is not None: a.plot(range(1, m.shape[1] + 1), m.mean(0) * 100, color="#4FC3F7", lw=1.8, label="val mAP50-95 (%)")
            if ml is not None:
                a2 = a.twinx(); a2.plot(range(1, ml.shape[1] + 1), ml.mean(0), color="#FFB74D", lw=1.8, ls="--", label="val box loss"); a2.set_ylabel("box loss")
        a.set_title("4) Learning curve (baseline)", fontsize=11, fontweight="bold"); a.set_xlabel("Epoch"); a.set_ylabel("mAP (%)"); a.grid()
        a = fig.add_subplot(gs[1, 1]); a.bar(range(n), good, color="#4CAF50", label="good"); a.bar(range(n), over, bottom=good, color="#F44336", label="overfit")
        a.bar(range(n), under, bottom=[g + o for g, o in zip(good, over)], color="#FFC107", label="underfit")
        a.set_title("5) Over/under-fit verdicts", fontsize=11, fontweight="bold"); a.set_ylabel("Folds"); a.legend(fontsize=8); a.grid(axis="y"); xt(a, fs=8)
        a = fig.add_subplot(gs[1, 2]); a.axis("off")
        order = sorted(range(n), key=lambda i: -accs[i])
        rows = [[labels[i], f"{accs[i]:.1f}%", f"{mapv[i]:.1f}", f"{good[i]}/{good[i] + over[i] + under[i]}", "A" if accs[i] >= 95 else ("B" if accs[i] >= 85 else "C")] for i in order]
        tbl = a.table(cellText=rows, colLabels=["Condition", "Accuracy", "mAP", "Good folds", "Grade"], loc="center", cellLoc="center")
        tbl.auto_set_font_size(False); tbl.set_fontsize(9.5 if n <= 10 else 8); tbl.scale(1.0, 1.5 if n <= 10 else 1.15)
        gcol = {"A": "#4CAF50", "B": "#FFC107", "C": "#F44336"}
        for (ri, ci), cell in tbl.get_celld().items():
            cell.set_facecolor(("#1e2530" if ri == 0 else "#161b22") if dark else ("#e6e6e6" if ri == 0 else "white")); cell.set_edgecolor("#444" if dark else "#bbbbbb")
            cell.set_text_props(color=gcol[rows[ri - 1][4]] if (ri > 0 and ci == 4) else TXT)
        a.set_title("6) Ranking", fontsize=11, fontweight="bold", pad=14)
        fig.suptitle(f"Experiment: {title} - YOLOv8n ball detection OK/NG judgement", fontsize=16, fontweight="bold", y=1.01)
        plt.tight_layout(); savefig("10_dashboard.png")
    return saved


# ── draw the 10 graphs for every experiment group that has results ──
FINAL_GROUPS = []
if "results_round1" in globals() and "results_round2" in globals():
    _filt = [dict(baseline_result, label="Original")] + [dict(r, label=r["name"]) for r in list(results_round1) + list(results_round2)]
    FINAL_GROUPS.append(("filters", _filt, "preprocessing filter", "Preprocessing filter"))
for _ax in SWEEP_ORDER:
    if _ax in SWEEP_RESULTS:
        FINAL_GROUPS.append((f"sweep_{_ax}", SWEEP_RESULTS[_ax], SWEEP_TITLE[_ax][0], SWEEP_TITLE[_ax][1]))
for _nz, _rs in GRID_RESULTS.items():
    FINAL_GROUPS.append((f"grid_noise{_nz:g}", _rs, f"filter at noise σ={_nz:g}", f"Preprocessing filter (noise σ={_nz:g})"))

if not USE_CV:
    print("The reference graph set needs the CV results (USE_CV = True) -> skipped.")
else:
    ALL_GRAPH_PATHS = {}
    for _i, (_key, _res, _title, _xl) in enumerate(FINAL_GROUPS):
        if len(_res) < 1 or any(r.get("map50_95") is None for r in _res):
            print(f"[{_key}] skipped: results without CV metrics (run the CV cells first)")
            continue
        print("=" * 70 + f"\n{_key}: {len(_res)} conditions\n" + "=" * 70)
        ALL_GRAPH_PATHS[_key] = make_reference_graphs(_key, _res, _title, _xl, show_gpu=(_i == 0))
        _df = results_to_df(_res[1:], _res[0])
        _df.insert(0, "Level", [r.get("label", r["name"]) for r in _res[:1] + _res[1:]])
        _df.to_csv(os.path.join(FILTER_FIG_DIR, f"table_{_key}.csv"), index=False, encoding="utf-8-sig")
    print("\n" + "=" * 70)
    print(f"Done: {sum(len(v) for v in ALL_GRAPH_PATHS.values())} graphs in {len(ALL_GRAPH_PATHS)} groups -> {os.path.abspath(FILTER_FIG_DIR)}")
    for _k, _v in ALL_GRAPH_PATHS.items():
        print(f"  {_k:<22s} {len(_v)} graphs   (table_{_k}.csv)")
    with open(os.path.join(FILTER_FIG_DIR, "sweep_results.json"), "w", encoding="utf-8") as f:
        json.dump({k: v for k, v in dict(sweeps=SWEEP_RESULTS, grid={str(k): v for k, v in GRID_RESULTS.items()}).items()}, f, ensure_ascii=False, indent=1)