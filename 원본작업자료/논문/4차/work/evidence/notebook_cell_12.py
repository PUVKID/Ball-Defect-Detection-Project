def _gt_worker(item):
    cv2.setNumThreads(1)
    g = cv2.imread(item["img"], cv2.IMREAD_GRAYSCALE)
    if g is None:
        return dict(item, error=True)
    H, W = g.shape
    boxes = read_yolo_boxes(item["lab"], W, H)
    part = locate_part(g)
    j = judge_boxes([(b[0], b[1]) for b in boxes], part, (W, H))
    return dict(item, error=False, W=W, H=H, gt_boxes=boxes,
                part=part, loc_fail=part is None,
                loc_suspect=(part is not None and not part["ok"]),
                area_frac=float("nan") if part is None else part["area_frac"],
                gt_pred=j["pred"], gt_reason=j["reason"], gt_counts=j["counts"])


t0 = time.time()
gt_results = Parallel(n_jobs=-1, backend="loky", verbose=5)(delayed(_gt_worker)(it) for it in dataset)
print(f"Ground truth (GT) computed: {len(gt_results)} images, {(time.time() - t0) / 60:.1f} min")
gt_results = [r for r in gt_results if not r.get("error")]
gt_by_key = {r["key"]: r for r in gt_results}

n = len(gt_results)
print(f"\nRectangle detection failures (loc_fail): {sum(r['loc_fail'] for r in gt_results)}/{n}  "
      f"(out of range (loc_suspect): {sum(r['loc_suspect'] for r in gt_results)}/{n})")
print(f"GT OK {sum(r['gt_pred']=='OK' for r in gt_results)} / NG {sum(r['gt_pred']=='NG' for r in gt_results)}")