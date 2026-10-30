plot_clean_bar(["Overall"], [acc], "", "OK/NG Judgement Accuracy (%)", "01_overall_accuracy.png",
               ymax=110, threshold=99, threshold_label="99% Threshold", show_min=False)

split_labels = [sp for sp in SPLITS if any(r["split"] == sp for r in results)]
split_acc = [_pct(sum(r["yolo_pred"] == r["gt_pred"] for r in results if r["split"] == sp),
                   sum(r["split"] == sp for r in results)) for sp in split_labels]
plot_clean_bar(split_labels, split_acc, "Split", "Accuracy (%)", "02_split_accuracy.png", ymax=110)

plot_clean_bar(["OK Recall", "NG Recall", "Precision", "F1"], [ok_recall, ng_recall, precision, f1],
               "Metric", "Score (%)", "03_ok_ng_metrics.png", ymax=110, show_min=False)

cm = np.array([[tn, fp], [fn, tp]])
fig, ax = plt.subplots(figsize=(5.5, 5))
im = ax.imshow(cm, cmap="Blues")
for i in range(2):
    for j in range(2):
        ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                fontsize=18, fontweight="bold", color="white" if cm[i, j] > cm.max() / 2 else "black")
ax.set_xticks([0, 1]); ax.set_xticklabels(["Pred OK", "Pred NG"], fontsize=13, fontweight="bold")
ax.set_yticks([0, 1]); ax.set_yticklabels(["True OK", "True NG"], fontsize=13, fontweight="bold")
ax.set_title("Confusion Matrix", fontsize=15, fontweight="bold")
fig.tight_layout()
cm_path = os.path.join(FIG_DIR, "04_confusion_matrix.png")
fig.savefig(cm_path, dpi=300, bbox_inches="tight", facecolor="white")
plt.show()
print(f"Saved: {cm_path}")