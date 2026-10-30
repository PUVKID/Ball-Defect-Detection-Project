DO_TRAIN = True
MODEL_SIZE = "yolov8n.pt"   # use yolov8s.pt / yolov8m.pt for higher accuracy (slower)
EPOCHS = 100
IMGSZ = 1280                # the originals are large and the balls are small, so larger than the default 640
BATCH = 8
TRAINED_WEIGHTS = None      # path to already-trained weights (use together with DO_TRAIN=False)

# ── [added] Oversampling + augmentation (train split only; val/test are never touched) ──
# Images are grouped by their label-based OK/NG judgement; the minority group is repeated (symlinks + label copies in a
# separate folder, the original dataset is not modified) until the two groups are about equally large.
OVERSAMPLE = True
OVERSAMPLE_MAX_FACTOR = 6   # a minority image appears at most this many times
AUG = dict(flipud=0.5, fliplr=0.5, scale=0.3, translate=0.1, hsv_v=0.4)   # makes the repeated copies differ from each other
OVERSAMPLED_ROOT = "yolo_oversampled"


def _link_or_copy(src, dst):
    if os.path.lexists(dst):
        os.remove(dst)
    try:
        os.symlink(os.path.abspath(src), dst)
    except (OSError, NotImplementedError):
        shutil.copyfile(src, dst)


def build_oversampled_dataset(pairs, dst_root, val_dir, max_factor=OVERSAMPLE_MAX_FACTOR):
    """pairs: [(key, image_path, label_path)] of the TRAIN split. Returns (data_yaml_path, info dict)."""
    ok = [p for p in pairs if gt_by_key[p[0]]["gt_pred"] == "OK"]
    ng = [p for p in pairs if gt_by_key[p[0]]["gt_pred"] == "NG"]
    minor, major = (ok, ng) if len(ok) < len(ng) else (ng, ok)
    factor = 1 if not minor else int(min(max_factor, max(1, round(len(major) / len(minor)))))
    minor_keys = {p[0] for p in minor}
    img_dir = os.path.join(dst_root, "images", "train")
    lab_dir = os.path.join(dst_root, "labels", "train")
    for d in (img_dir, lab_dir):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d, exist_ok=True)
    n_out = 0
    for key, img, lab in pairs:
        stem, ext = os.path.splitext(os.path.basename(img))
        for r in range(factor if key in minor_keys else 1):
            name = stem if r == 0 else f"{stem}_dup{r}"
            _link_or_copy(img, os.path.join(img_dir, name + ext))
            shutil.copyfile(lab, os.path.join(lab_dir, name + ".txt"))
            n_out += 1
    cfg = dict(path=os.path.abspath(dst_root), train="images/train", val=os.path.abspath(val_dir), names={0: "ball"})
    yaml_path = os.path.join(dst_root, "data.yaml")
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, allow_unicode=True, sort_keys=False)
    info = dict(n_ok=len(ok), n_ng=len(ng), factor=factor, minority="OK" if minor is ok else "NG", n_after=n_out)
    return yaml_path, info


train_yaml = _yaml_path
if DO_TRAIN:
    _tr_pairs = [(it["key"], it["img"], it["lab"]) for it in dataset if it["split"] == "train" and it["key"] in gt_by_key]
    _n_ok = sum(gt_by_key[k]["gt_pred"] == "OK" for k, _, _ in _tr_pairs)
    print(f"Train split GT balance: OK {_n_ok} / NG {len(_tr_pairs) - _n_ok}  (total {len(_tr_pairs)})")
    if OVERSAMPLE and _tr_pairs:
        _val_dir = os.path.join(DATA_ROOT, "images", "val")
        if not os.path.isdir(_val_dir):          # [fixed] no val folder: let YOLO validate on the train images
            _val_dir = os.path.join(DATA_ROOT, "images", "train")
        train_yaml, _info = build_oversampled_dataset(_tr_pairs, OVERSAMPLED_ROOT, _val_dir)
        print(f"Oversampling: minority = {_info['minority']} x{_info['factor']}  ->  {len(_tr_pairs)} -> {_info['n_after']} train images")
    model = YOLO(MODEL_SIZE)
    train_result = model.train(
        data=train_yaml, epochs=EPOCHS, imgsz=IMGSZ, batch=BATCH,
        project=RUNS_DIR, name="ball_detect", seed=SEED, patience=30, **AUG,
    )
    best_weights = str(train_result.save_dir / "weights" / "best.pt")
else:
    if not TRAINED_WEIGHTS:
        raise RuntimeError("With DO_TRAIN=False, set TRAINED_WEIGHTS to the path of the trained weights.")
    best_weights = TRAINED_WEIGHTS

print(f"\nWeights in use: {best_weights}")
yolo_model = YOLO(best_weights)