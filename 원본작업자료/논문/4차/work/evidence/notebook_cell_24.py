def draw_case(r, scale=0.3):
    g = cv2.imread(r["img"], cv2.IMREAD_GRAYSCALE)
    vis = cv2.cvtColor(cv2.normalize(g, None, 0, 255, cv2.NORM_MINMAX), cv2.COLOR_GRAY2BGR)
    part = r.get("part")
    if part is not None:
        cv2.polylines(vis, [np.array(part["poly"], np.int32).reshape(-1, 1, 2)], True, (0, 255, 255), 8)
        cx, cy = part["cx"], part["cy"]
        margin = LOC_PARAMS["inside_margin_frac"] * max(r["W"], r["H"])
        poly = np.array(part["poly"], np.float32).reshape(-1, 1, 2)
    for x, y, bw, bh in r["pred_boxes"]:
        ins = True
        if part is not None:
            ins = cv2.pointPolygonTest(poly, (float(x), float(y)), True) >= -margin
        col = (0, 220, 0) if ins else (0, 0, 255)
        cv2.rectangle(vis, (int(x - bw / 2), int(y - bh / 2)), (int(x + bw / 2), int(y + bh / 2)), col, 6)
    return cv2.cvtColor(cv2.resize(vis, (0, 0), fx=scale, fy=scale), cv2.COLOR_BGR2RGB)


def show_cases(rs, title, n_show=6, cols=3, scale=0.3):
    rs = rs[:n_show]
    if not rs:
        print(f"[{title}] no matching images.")
        return
    rows = (len(rs) + cols - 1) // cols
    plt.figure(figsize=(6 * cols, 5 * rows))
    for i, r in enumerate(rs):
        plt.subplot(rows, cols, i + 1)
        plt.imshow(draw_case(r, scale))
        plt.axis("off")
        c = r["yolo_counts"]
        plt.title(f"{r['key']}  GT {r['gt_pred']} -> YOLO {r['yolo_pred']}\n"
                  f"detected {c['top']}/{c['left']}/{c['bottom']}/{c['right']} (top/left/bottom/right)  {r['yolo_reason']}", fontsize=10)
    plt.suptitle(title, fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


rng = random.Random(SEED)
show_cases(rng.sample(results, min(6, len(results))), "(1) 6 random images")
show_cases([r for r in results if r["yolo_pred"] != r["gt_pred"]], "(2) Images judged differently from the label-based GT")
show_cases([r for r in results if r["loc_fail"]], "(3) Images where the rectangle detection failed")