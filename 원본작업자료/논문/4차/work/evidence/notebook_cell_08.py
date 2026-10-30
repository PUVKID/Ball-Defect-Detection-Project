def _ellipse(k):
    k = max(1, int(k)) | 1
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))


LOC_PARAMS = dict(
    work_long=736,
    std_ksize_grid=(15, 21, 9),        # [fixed] retry with several texture windows
    close_ksize=9,
    open_ksize_grid=(61, 41, 81, 101, 31),  # [fixed] retry with several opening kernels
    min_area_frac=0.10,
    max_area_frac=0.85,
    inside_margin_frac=0.01,
)


def _locate_part_once(sm, h, w, std_ksize, open_ksize, close_ksize):
    f = sm.astype(np.float32)
    k = std_ksize
    mean = cv2.boxFilter(f, -1, (k, k))
    sq = cv2.boxFilter(f * f, -1, (k, k))
    std = np.sqrt(np.clip(sq - mean * mean, 0, None))
    u8 = cv2.normalize(std, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    _, th = cv2.threshold(u8, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, _ellipse(close_ksize))

    pad = cv2.copyMakeBorder(th, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
    inv = 255 - pad
    cv2.floodFill(inv, np.zeros((h + 4, w + 4), np.uint8), (0, 0), 0)
    filled = th | inv[1:-1, 1:-1]

    op = cv2.morphologyEx(filled, cv2.MORPH_OPEN, _ellipse(open_ksize))
    n, lab, stats, cent = cv2.connectedComponentsWithStats(op)
    if n <= 1:
        return None
    cid = int(lab[h // 2, w // 2])
    if cid == 0:
        cand = [i for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] >= 0.05 * h * w]
        if not cand:
            return None
        cid = min(cand, key=lambda i: math.hypot(cent[i][0] - w / 2, cent[i][1] - h / 2))
    comp = (lab == cid).astype(np.uint8) * 255
    cs, _ = cv2.findContours(comp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cs:
        return None
    hull = cv2.convexHull(max(cs, key=cv2.contourArea))
    area_frac = cv2.contourArea(hull) / float(h * w)
    M = cv2.moments(hull)
    if M["m00"] <= 0:
        return None
    return dict(poly=hull.reshape(-1, 2).astype(np.float32), cx=M["m10"] / M["m00"], cy=M["m01"] / M["m00"],
                area_frac=area_frac)


def locate_part(gray, P=LOC_PARAMS):
    # [fixed] try every std_ksize x open_ksize combination and pick the candidate with the largest area ratio inside the min~max range.
    H, W = gray.shape
    s = min(1.0, P["work_long"] / max(H, W))
    sm = cv2.resize(gray, (max(1, int(round(W * s))), max(1, int(round(H * s)))), interpolation=cv2.INTER_AREA) if s < 1.0 else gray
    h, w = sm.shape
    sx, sy = W / w, H / h

    best = None
    for std_ksize in P["std_ksize_grid"]:
        for open_ksize in P["open_ksize_grid"]:
            r = _locate_part_once(sm, h, w, std_ksize, open_ksize, P["close_ksize"])
            if r is None:
                continue
            if P["min_area_frac"] <= r["area_frac"] <= P["max_area_frac"]:
                if best is None or r["area_frac"] > best["area_frac"]:
                    best = r
    if best is None:
        # if no candidate is inside the range (part shot unusually large or small), use the largest candidate overall and flag it as suspect
        for std_ksize in P["std_ksize_grid"]:
            for open_ksize in P["open_ksize_grid"]:
                r = _locate_part_once(sm, h, w, std_ksize, open_ksize, P["close_ksize"])
                if r is not None and (best is None or r["area_frac"] > best["area_frac"]):
                    best = r
        if best is not None:
            best["out_of_range"] = True
    if best is None:
        return None

    best.setdefault("out_of_range", False)
    poly = best["poly"] * np.array([sx, sy], np.float32)
    return dict(poly=poly, cx=float(best["cx"] * sx), cy=float(best["cy"] * sy),
                area_frac=float(best["area_frac"]), ok=not best["out_of_range"])