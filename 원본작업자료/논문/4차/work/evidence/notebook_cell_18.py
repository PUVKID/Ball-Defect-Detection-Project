CONF_THRES = 0.25
IOU_THRES = 0.5

try:
    from tqdm.auto import tqdm
except ImportError:            # no progress bar available: iterate silently
    tqdm = lambda it, **kw: it

# [added] The OK/NG rule needs the EXACT ball count, so the confidence threshold matters a lot. Pick it on the VAL split
# (balanced accuracy, so the majority class cannot dominate), never on test.
TUNE_CONF = bool(by_split.get("test"))   # [fixed] without a test split, val is what gets scored, so tuning on it would leak
if TUNE_CONF:
    _val = [it for it in dataset if it["split"] == "val" and it["key"] in gt_by_key]
    if len(_val) >= 20:
        _raw = []
        for it in tqdm(_val, desc="conf sweep (val)", unit="img"):
            _p = yolo_model.predict(it["img"], imgsz=IMGSZ, conf=0.05, iou=IOU_THRES, verbose=False)[0]
            _xy = _p.boxes.xywh.cpu().numpy() if len(_p.boxes) else np.zeros((0, 4))
            _cf = _p.boxes.conf.cpu().numpy() if len(_p.boxes) else np.zeros(0)
            _raw.append((it, _xy, _cf))
        _best = (-1.0, CONF_THRES)
        for _c in np.arange(0.10, 0.80, 0.05):
            _hit = {"OK": [0, 0], "NG": [0, 0]}
            for it, _xy, _cf in _raw:
                _g = gt_by_key[it["key"]]
                _pts = [(float(x), float(y)) for (x, y, _, _), s in zip(_xy, _cf) if s >= _c]
                _pred = judge_boxes(_pts, _g["part"], (_g["W"], _g["H"]))["pred"]
                _hit[_g["gt_pred"]][0] += int(_pred == _g["gt_pred"])
                _hit[_g["gt_pred"]][1] += 1
            _rec = [h / n for h, n in _hit.values() if n]
            _bal = float(np.mean(_rec)) if _rec else 0.0
            if _bal > _best[0] + 1e-9:
                _best = (_bal, float(_c))
        CONF_THRES = round(_best[1], 2)
        print(f"CONF_THRES tuned on val: {CONF_THRES} (balanced accuracy {100 * _best[0]:.2f}%)")
    else:
        print(f"Too few val images ({len(_val)}) to tune CONF_THRES, keeping {CONF_THRES}")

# One process, one model (`yolo_model` from Section 5). The GPU is the bottleneck here, so extra worker processes
# would only add start-up time and GPU memory (every process loads its own model and CUDA context), and joblib
# prints nothing until a whole chunk is finished, which looks like a frozen notebook.
results, t0 = [], time.time()
for item in tqdm(dataset, desc="YOLO judgement", unit="img"):
    gt = gt_by_key.get(item["key"])
    if gt is None:                        # unreadable image: no ground truth was computed for it
        results.append(dict(item, error=True))
        continue
    pred = yolo_model.predict(item["img"], imgsz=IMGSZ, conf=CONF_THRES, iou=IOU_THRES, verbose=False)[0]
    xywh = pred.boxes.xywh.cpu().numpy() if len(pred.boxes) else np.zeros((0, 4))
    pts = [(float(x), float(y)) for x, y, _, _ in xywh]
    j = judge_boxes(pts, gt["part"], (gt["W"], gt["H"]))
    results.append(dict(item, error=False, W=gt["W"], H=gt["H"], pred_boxes=xywh.tolist(),
                        part=gt["part"], loc_fail=gt["part"] is None,
                        yolo_pred=j["pred"], yolo_reason=j["reason"], yolo_counts=j["counts"], n_det=len(pts)))
print(f"YOLO judgement done: {len(results)} images, {(time.time() - t0) / 60:.1f} min")
results = [r for r in results if not r.get("error")]
for r in results:
    r["gt_pred"] = gt_by_key[r["key"]]["gt_pred"]
