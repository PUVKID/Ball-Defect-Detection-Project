# ── 28c. Operating-point sensitivity of the Original detector (conf threshold x match tolerance) ──────────
OP_CONFS = [0.10, 0.25, 0.40, 0.50, 0.60]
OP_TOLS = [0.3, 0.5, 0.7]


def predict_conf_floor(model, gray, conf_floor):
    pred = model.predict(cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR), imgsz=CV_IMGSZ, conf=conf_floor, iou=IOU_THRES, verbose=False)[0]
    xywh = pred.boxes.xywh.cpu().numpy() if len(pred.boxes) else np.zeros((0, 4))
    conf = pred.boxes.conf.cpu().numpy() if len(pred.boxes) else np.zeros(0)
    return xywh, conf


def operating_point_table(preds, items, confs, tols, skip_keys=()):
    """preds[key] = (xywh, conf) at the lowest threshold. Raising the threshold afterwards equals a run at that threshold
    (NMS keeps the highest-scoring box first, so low-score boxes never suppress high-score ones).
    Returns (strict DataFrame conf x tol, accuracy Series per conf, n images)."""
    skip = set(skip_keys)
    use = [it for it in items if it["key"] not in skip and it["key"] in preds]
    strict = {c: {} for c in confs}
    acc = {}
    for c in confs:
        ok_acc, st = 0, {t: 0 for t in tols}
        for it in use:
            g = gt_by_key[it["key"]]
            xywh, cf = preds[it["key"]]
            sel = cf >= c
            xs, cs = xywh[sel], cf[sel]
            pj = judge_boxes([(float(x), float(y)) for x, y, _, _ in xs], g["part"], (g["W"], g["H"]))
            ok_acc += int(pj["pred"] == g["gt_pred"])
            for t in tols:
                m = ball_match_stats(g["gt_boxes"], xs, cs, tol_frac=t)
                st[t] += int(m["miss"] == 0 and m["extra"] == 0)
        acc[c] = 100.0 * ok_acc / max(len(use), 1)
        for t in tols:
            strict[c][t] = 100.0 * st[t] / max(len(use), 1)
    sdf = pd.DataFrame(strict).T
    sdf.index.name, sdf.columns.name = "conf", "tol"
    return sdf, pd.Series(acc, name="accuracy"), len(use)


OP_RESULT = {}
if RUN_DIAG and USE_CV:
    _preds, _miss = {}, 0
    for it in tqdm(eval_items, desc="operating point", unit="img"):
        model = get_model("Original", identity_filter, FOLD_OF[it["key"]])
        if model is None:
            _miss += 1
            continue
        _preds[it["key"]] = predict_conf_floor(model, load_raw(it), min(OP_CONFS))
    if _preds:
        _sdf, _adf2, _n = operating_point_table(_preds, eval_items, OP_CONFS, OP_TOLS)
        print(f"\n(28c) Strict accuracy (%) of Original, {_n} images (rows: confidence threshold, columns: match tolerance x ball size)")
        display(_sdf.round(1))
        print("Plain OK/NG accuracy (%) per confidence threshold:", _adf2.round(1).to_dict())
        _ref = np.mean([int(r.get("miss") == 0 and r.get("extra") == 0) for r in PER_IMAGE["Original"]]) * 100 if PER_IMAGE.get("Original") else float("nan")
        print(f"Sanity: the cell (0.25, 0.5) should reproduce the CV result ({_ref:.1f}%): {_sdf.loc[0.25, 0.5]:.1f}%" if 0.25 in OP_CONFS and 0.5 in OP_TOLS else "")
        _fail = [it["key"] for it in eval_items if gt_by_key[it["key"]].get("loc_fail")]
        _sdf2, _adf3, _n2 = operating_point_table(_preds, eval_items, [0.25], [0.5], skip_keys=_fail)
        print(f"Without the {len(_fail)} images where the part was not found (centre fallback): {_n2} images | strict {_sdf2.loc[0.25, 0.5]:.1f}% | accuracy {_adf3[0.25]:.1f}%")
        _sdf.round(2).to_csv(os.path.join(FILTER_FIG_DIR, "diag_operating_point_strict.csv"), encoding="utf-8-sig")
        OP_RESULT = dict(strict=_sdf.round(2).to_dict(), acc=_adf2.round(2).to_dict(), n_fail=len(_fail),
                         strict_without_fail=float(_sdf2.loc[0.25, 0.5]), acc_without_fail=float(_adf3[0.25]))
    else:
        print("No cached Original fold detectors -> skipped.")