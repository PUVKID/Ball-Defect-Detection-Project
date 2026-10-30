def _pct(a, b):
    return 100.0 * a / b if b else 0.0

n = len(results)
acc = _pct(sum(r["yolo_pred"] == r["gt_pred"] for r in results), n)
print(f"All {n} images  OK/NG judgement accuracy (vs label-based GT): {acc:.2f}%")

tp = sum(r["gt_pred"] == "NG" and r["yolo_pred"] == "NG" for r in results)
fn = sum(r["gt_pred"] == "NG" and r["yolo_pred"] == "OK" for r in results)
fp = sum(r["gt_pred"] == "OK" and r["yolo_pred"] == "NG" for r in results)
tn = sum(r["gt_pred"] == "OK" and r["yolo_pred"] == "OK" for r in results)
ng_recall = _pct(tp, tp + fn); ok_recall = _pct(tn, tn + fp)
precision = _pct(tp, tp + fp) if (tp + fp) else 0.0
f1 = 2 * precision * ng_recall / (precision + ng_recall) if (precision + ng_recall) else 0.0
print(f"NG recall {ng_recall:.2f}% | OK recall {ok_recall:.2f}% | NG Precision {precision:.2f}% | F1 {f1:.2f}%")
print(f"Balanced accuracy {(ok_recall + ng_recall) / 2:.2f}%   (plain accuracy hides a collapse onto the majority class)")
print("GT balance per split: " + ", ".join(f"{sp} OK {sum(r['split'] == sp and r['gt_pred'] == 'OK' for r in results)}/NG {sum(r['split'] == sp and r['gt_pred'] == 'NG' for r in results)}" for sp in SPLITS))
print(f"Confusion matrix:  NG->NG {tp}  NG->OK {fn}  OK->NG {fp}  OK->OK {tn}")

print("\n[Accuracy per split]")
for sp in SPLITS:
    rs = [r for r in results if r["split"] == sp]
    if not rs:
        continue
    a = _pct(sum(r["yolo_pred"] == r["gt_pred"] for r in rs), len(rs))
    print(f"  {sp:5s} {len(rs):5d} images  accuracy {a:6.2f}%")

print("\n[Top 10 reasons for mismatches (judged differently from the label-based GT)]")
mism = [r for r in results if r["yolo_pred"] != r["gt_pred"]]
for reason, cnt in Counter((r["gt_pred"], r["yolo_pred"], r["yolo_reason"]) for r in mism).most_common(10):
    print(f"  {cnt:4d} images  GT {reason[0]} -> YOLO {reason[1]}   (count difference: {reason[2]})")

# (optional) compare with a separate ground-truth OK/NG list
if OKNG_CSV and os.path.isfile(OKNG_CSV):
    ref = {}
    with open(OKNG_CSV, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            ref[os.path.splitext(row["name"].strip())[0]] = row["label"].strip().upper()
    rr = [(r, ref[r["stem"]]) for r in results if r["stem"] in ref]
    if rr:
        a2 = _pct(sum(r["yolo_pred"] == y for r, y in rr), len(rr))
        print(f"\n[Ground-truth CSV comparison] {len(rr)} images  YOLO agreement {a2:.2f}%")

csv_path = os.path.join(FIG_DIR, "yolo_judgement_results.csv")
with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
    wr = csv.writer(f)
    wr.writerow(["key", "split", "gt_pred", "yolo_pred", "match", "yolo_reason", "n_det", "loc_fail"])
    for r in results:
        wr.writerow([r["key"], r["split"], r["gt_pred"], r["yolo_pred"],
                     int(r["gt_pred"] == r["yolo_pred"]), r["yolo_reason"], r["n_det"], int(r["loc_fail"])])
print(f"\nPer-image results saved: {csv_path}")

print("\nNOTE: these numbers are NOT held-out (the detector trained on the train images and best.pt was picked on val). "
      "Use them as a sanity check; the paper numbers are the cross-validated ones from Section 14 on.")