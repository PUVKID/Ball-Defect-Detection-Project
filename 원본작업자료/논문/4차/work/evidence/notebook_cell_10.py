def assign_region(x, y, cx, cy):
    ang = math.degrees(math.atan2(-(y - cy), x - cx))
    if -45 <= ang < 45:
        return "right"
    elif 45 <= ang < 135:
        return "top"
    elif ang >= 135 or ang < -135:
        return "left"
    return "bottom"


def judge_boxes(pts, part, img_wh, params=LOC_PARAMS):
    W, H = img_wh
    if part is None:
        cx, cy = W / 2.0, H / 2.0
        inside = [True] * len(pts)
    else:
        poly = part["poly"].reshape(-1, 1, 2).astype(np.float32)
        cx, cy = part["cx"], part["cy"]
        margin = params["inside_margin_frac"] * max(W, H)
        inside = [cv2.pointPolygonTest(poly, (float(x), float(y)), True) >= -margin for x, y in pts]

    counts = {k: 0 for k in REGION_RULE}
    for (x, y), ins in zip(pts, inside):
        if ins:
            counts[assign_region(x, y, cx, cy)] += 1

    ok = all(counts[k] == REGION_RULE[k] for k in REGION_RULE)
    diff = {k: counts[k] - REGION_RULE[k] for k in REGION_RULE if counts[k] != REGION_RULE[k]}
    reason = ", ".join(f"{k} {v:+d}" for k, v in diff.items())
    return dict(counts=counts, pred="OK" if ok else "NG", reason=reason, inside=inside)