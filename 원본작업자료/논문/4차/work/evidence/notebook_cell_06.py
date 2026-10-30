DATA_ROOT = r"/root/추계학술대회/DataSet"
SPLITS = ["train", "val", "test"]
IMG_EXTS = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff")

REGION_RULE = {"top": 5, "left": 4, "bottom": 2, "right": 2}
BALL_CLASSES = None      # None: treat every class in the labels as a ball
OKNG_CSV = None          # path to a separate ground-truth OK/NG list (name,label), if you have one

_yaml_path = os.path.join(DATA_ROOT, "data.yaml")
if not os.path.isfile(_yaml_path):
    with open(_yaml_path, "w", encoding="utf-8") as f:
        f.write(f"path: {DATA_ROOT}\ntrain: images/train\nval: images/val\ntest: images/test\nnames:\n  0: ball\n")
    print(f"data.yaml was missing, created a new one: {_yaml_path}")
else:
    try:
        import yaml
        with open(_yaml_path, encoding="utf-8") as f:
            print("data.yaml:", yaml.safe_load(f))
    except Exception as e:
        print("Skipped reading data.yaml:", e)


def read_yolo_boxes(label_path, W, H, classes=BALL_CLASSES):
    boxes = []
    with open(label_path, encoding="utf-8") as f:
        for line in f:
            p = line.split()
            if len(p) < 5:
                continue
            c = int(float(p[0]))
            if classes is not None and c not in classes:
                continue
            xc, yc, bw, bh = (float(v) for v in p[1:5])
            boxes.append((xc * W, yc * H, bw * W, bh * H))
    return boxes


def list_dataset(root, splits):
    items, no_label = [], []
    for sp in splits:
        img_dir = os.path.join(root, "images", sp)
        lab_dir = os.path.join(root, "labels", sp)
        if not os.path.isdir(img_dir):
            print(f"[{sp}] image folder not found -> skipped: {img_dir}")
            continue
        paths = sorted(p for p in glob.glob(os.path.join(img_dir, "*")) if p.lower().endswith(IMG_EXTS))
        n_ok = 0
        for p in paths:
            stem = os.path.splitext(os.path.basename(p))[0]
            lp = os.path.join(lab_dir, stem + ".txt")
            if os.path.isfile(lp):
                items.append(dict(split=sp, stem=stem, key=f"{sp}/{stem}", img=p, lab=lp))
                n_ok += 1
            else:
                no_label.append(p)
        print(f"[{sp}] {len(paths)} images -> {n_ok} matched with labels")
    if no_label:
        print(f"WARNING: {len(no_label)} images excluded because they have no label file (e.g. {no_label[:3]})")
    return items


dataset = list_dataset(DATA_ROOT, SPLITS)
if not dataset:
    raise RuntimeError(f"No images to evaluate. Check DATA_ROOT and the folder layout: {DATA_ROOT}")
by_split = Counter(it["split"] for it in dataset)
print(f"Total {len(dataset)} images  {dict(by_split)}")