SAMPLE_KEY = None          # e.g. "test/<stem>"; None -> first scored image
GRID_ZOOM = None           # None = whole image in the base grids; or (x0, y0, x1, y1) as fractions, e.g. (0.3, 0.3, 0.7, 0.7)
GRID_ZOOM_AUTO = False      # also make the native-resolution zoom and the difference grids
GRID_ZOOM_PX = (700, 560)  # size (width, height) in original pixels of the automatic zoom window, centred on the balls
DIFF_GAIN = 1              # |filtered - Original| is multiplied by this in the difference grids (raise it for mild changes)
GRID_PANEL_MAX_DIM = 700   # long side of every grid panel in pixels
GRID_COLS = 4

_eval_by_key = {it["key"]: it for it in eval_items}
if SAMPLE_KEY is not None and SAMPLE_KEY not in _eval_by_key:
    raise KeyError(f"SAMPLE_KEY {SAMPLE_KEY!r} is not among the scored images (EVAL_SPLITS={EVAL_SPLITS}).")
sample_item = _eval_by_key[SAMPLE_KEY] if SAMPLE_KEY is not None else eval_items[0]
_t0 = time.perf_counter()
sample_gray = cv2.imread(sample_item["img"], cv2.IMREAD_GRAYSCALE)
read_sample_ms = (time.perf_counter() - _t0) * 1000
print(f"Sample image: {sample_item['key']}  ({sample_gray.shape[1]}x{sample_gray.shape[0]})")

# warm-up: the first GPU filter call and the first YOLO call are slow (CUDA / cuDNN / model initialisation)
apply_filter_gray(sample_gray, FILTERS_ROUND1[0][1])
_bgr = cv2.cvtColor(sample_gray, cv2.COLOR_GRAY2BGR)
yolo_centers(yolo_model, _bgr)
_t0 = time.perf_counter()
yolo_centers(yolo_model, _bgr)
yolo_sample_ms = (time.perf_counter() - _t0) * 1000
print(f"Single-image timings: read {read_sample_ms:.1f} ms, YOLO {yolo_sample_ms:.1f} ms")

# apply every filter once to the sample image and save the Original-vs-filtered example right away
filter_samples = {}      # filter name -> filtered uint8 image
filter_sample_ms = {}    # filter name -> filter time on the sample (ms)
filter_sample_gb = {}    # filter name -> peak GPU memory on the sample (GB)
filter_sample_stats = {}  # filter name -> (mean |change| in gray levels, % of pixels changed)
for _tag, _filters in (("Round 1", FILTERS_ROUND1), ("Round 2", FILTERS_ROUND2)):
    for _name, _fn in _filters:
        _t0 = time.time()
        if torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats()
        _filtered, _dt = apply_filter_gray(sample_gray, _fn)
        filter_sample_gb[_name] = torch.cuda.max_memory_allocated() / 1024 ** 3 if torch.cuda.is_available() else 0.0
        _delta = np.abs(_filtered.astype(np.int16) - sample_gray.astype(np.int16))
        filter_sample_stats[_name] = (float(_delta.mean()), 100.0 * float((_delta > 0).mean()))
        filter_samples[_name] = _filtered
        filter_sample_ms[_name] = _dt * 1000
        save_filter_example(_name, sample_gray, _filtered)
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        print(f"  [{_tag}] {_name:<24s} saved  (filter {_dt * 1000:9.1f} ms, peak GPU {filter_sample_gb[_name]:5.2f} GB, total {time.time() - _t0:5.1f} s)")
        print(f"      changed the image: mean |change| {filter_sample_stats[_name][0]:6.2f} gray levels, "
              f"{filter_sample_stats[_name][1]:5.1f}% of the pixels differ" + ("   <-- WARNING: image unchanged" if filter_sample_stats[_name][1] == 0 else ""))
print(f"\n{len(filter_samples)} example images saved -> {os.path.abspath(FILTER_SAMPLE_DIR)}")
_weak = [n for n, (m, _) in filter_sample_stats.items() if m < 1.0]
if _weak:
    print(f"WARNING - filters that changed the sample by less than 1 gray level on average: {_weak}\n"
          "  They should be extreme; check their parameters in FILTER_SPECS.")
if torch.cuda.is_available():
    _total_gb = torch.cuda.get_device_properties(0).total_memory / 1024 ** 3
    _worst = max(filter_sample_gb, key=filter_sample_gb.get)
    print(f"Peak GPU memory on this image: {filter_sample_gb[_worst]:.2f} GB ({_worst}) of {_total_gb:.1f} GB"
          + ("  <- close to the limit: a larger image may run out of memory" if filter_sample_gb[_worst] > 0.8 * _total_gb else ""))


def print_runtime_estimate():
    """Rough estimate: (filter time + YOLO time + image read) measured on the sample x number of scored images."""
    n_img = len(eval_items)
    fixed_ms = yolo_sample_ms + read_sample_ms
    rounds = (("Baseline", [("Original", None)]), ("Round 1", FILTERS_ROUND1),
              ("Round 2", FILTERS_ROUND2))
    print(f"\nRough runtime estimate  (FILTER_MODE = {FILTER_MODE}, {n_img} images per filter, RUN_PRESET = {RUN_PRESET})")
    total, n_methods = 0.0, 0
    for tag, filters in rounds:
        round_min = 0.0
        for name, _ in filters:
            if name in SKIP_FILTERS:
                continue
            n_methods += 1
            m = ((0.0 if name == "Original" else filter_sample_ms[name]) + fixed_ms) * n_img / 1000.0 / 60.0
            round_min += m
            if m >= 1.0:
                print(f"    {name:<24s} ~{m:8.1f} min")
        total += round_min
        print(f"  {tag:<9s} ~{round_min:8.1f} min")
    print(f"  {'Total':<9s} ~{total:8.1f} min  (~{total / 60:.1f} h)   [single-image based; the real time also depends on disk and GPU load]")
    if FILTER_MODE == "train_per_filter":
        if USE_CV:
            print(f"  NOTE: CV adds {n_methods * len(_run_folds)} YOLO trainings ({n_methods} methods x {len(_run_folds)} folds, "
                  f"{FILTER_EPOCHS} epochs each; about 2 min each for 360 images on an RTX 4090). Finished folds are reused on re-runs.")
        else:
            print(f"  NOTE: train_per_filter adds one YOLO training per filter ({n_methods - 1} trainings) on top of this.")


print_runtime_estimate()


def _auto_zoom_fractions():
    """A native-resolution window around the balls: the top-most ball and its 4 nearest neighbours."""
    H, W = sample_gray.shape
    zw, zh = min(GRID_ZOOM_PX[0], W), min(GRID_ZOOM_PX[1], H)
    boxes = gt_by_key[sample_item["key"]].get("gt_boxes") or []
    if boxes:
        pts = np.array([(b[0], b[1]) for b in boxes], dtype=float)
        top = pts[np.argmin(pts[:, 1])]
        near = pts[np.argsort(np.hypot(pts[:, 0] - top[0], pts[:, 1] - top[1]))[:5]]
        cx, cy = near.mean(axis=0)
    else:
        cx, cy = W / 2, H / 2
    x0 = int(np.clip(cx - zw / 2, 0, W - zw))
    y0 = int(np.clip(cy - zh / 2, 0, H - zh))
    return (x0 / W, y0 / H, (x0 + zw) / W, (y0 + zh) / H)


def _grid_panel(img, zoom=None):
    zoom = GRID_ZOOM if zoom is None else zoom
    if zoom is not None:
        h, w = img.shape
        x0, y0, x1, y1 = zoom
        img = img[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)]
    h, w = img.shape
    s = GRID_PANEL_MAX_DIM / max(h, w)
    if s < 1.0:
        img = cv2.resize(img, (max(1, int(w * s)), max(1, int(h * s))), interpolation=cv2.INTER_AREA)
    return img


def make_grid_figure(filter_names, save_name, mode="image", zoom=None, ncols=GRID_COLS):
    """Grid of (a) Original followed by the given filters, all applied to the same sample image.
    mode="image": the filtered images; mode="diff": |filtered - Original| multiplied by DIFF_GAIN."""
    panels = [("Original", sample_gray)]
    for n in filter_names:
        if mode == "diff":
            d = np.abs(filter_samples[n].astype(np.int16) - sample_gray.astype(np.int16))
            panels.append((f"{n}\n(mean change {filter_sample_stats[n][0]:.2f})", np.clip(d * DIFF_GAIN, 0, 255).astype(np.uint8)))
        else:
            panels.append((n, filter_samples[n]))
    nrows = math.ceil(len(panels) / ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.6 * ncols, 4.6 * nrows))
    axes = np.atleast_1d(axes).ravel()
    for i, (ax, (label, img)) in enumerate(zip(axes, panels)):
        ax.imshow(_grid_panel(img, zoom), cmap="gray", vmin=0, vmax=255)
        ax.set_title(f"({chr(97 + i)}) {label}", fontsize=16, fontweight="bold")
        ax.axis("off")
    for ax in axes[len(panels):]:
        ax.axis("off")
    fig.tight_layout()
    out_path = os.path.join(FILTER_SAMPLE_DIR, save_name)
    fig.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.show()
    print(f"Saved: {out_path}")
    return out_path


_r1_names = [n for n, _ in FILTERS_ROUND1]
_r2_names = [n for n, _ in FILTERS_ROUND2]
grid_round1_path = make_grid_figure(_r1_names, "grid_original_round1.png")
grid_round2_path = make_grid_figure(_r2_names, "grid_original_round2.png")
if GRID_ZOOM_AUTO:
    _zoom = GRID_ZOOM if GRID_ZOOM is not None else _auto_zoom_fractions()
    print(f"Zoom window (fractions x0, y0, x1, y1): {tuple(round(v, 3) for v in _zoom)}")
    for _tag, _names in (("round1", _r1_names), ("round2", _r2_names)):
        make_grid_figure(_names, f"grid_original_{_tag}_zoom.png", zoom=_zoom)
        make_grid_figure(_names, f"grid_original_{_tag}_diff.png", mode="diff", zoom=_zoom)
