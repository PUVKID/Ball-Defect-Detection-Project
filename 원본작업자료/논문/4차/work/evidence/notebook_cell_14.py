# ── 4b. Data audit ───────────────────────────────────────────────────
GROUP_FOLDS = True      # keep near-duplicate images in the same CV fold (Section 11 reads this)
DUP_SIZE = 128          # thumbnail size of the duplicate check
DUP_MAD = 1.0           # near-duplicate = mean absolute gray difference of the thumbnails below this (gray levels)

_n_gt = len(gt_results)
_gt_ok = sum(r["gt_pred"] == "OK" for r in gt_results)
_gt_ng = _n_gt - _gt_ok
_major = "OK" if _gt_ok >= _gt_ng else "NG"
print(f"GT class balance: OK {_gt_ok} ({100 * _gt_ok / _n_gt:.1f}%) / NG {_gt_ng} ({100 * _gt_ng / _n_gt:.1f}%)")
print(f"=> a detector that always answers '{_major}' already scores {100 * max(_gt_ok, _gt_ng) / _n_gt:.1f}%  (report this majority-class baseline next to every accuracy)")

print("\nLabelled balls per image:")
for cls in ("OK", "NG"):
    cnt = Counter(len(r["gt_boxes"]) for r in gt_results if r["gt_pred"] == cls)
    print(f"  GT {cls}: " + (", ".join(f"{k} balls x{v}" for k, v in sorted(cnt.items())) or "-"))
print("\nNOTE: GT and the YOLO judgement use the same rectangle (`part`) and the same rule, and detections outside the rectangle are ignored.\n"
      "      The OK/NG accuracy therefore measures 'are the balls inside the rectangle found exactly', not an independent OK/NG label.\n"
      "      Set OKNG_CSV (name,label) for agreement with a real OK/NG list, and read 'Strict Acc' (all labelled balls found, no extra detection anywhere).")


def find_dup_groups(items, size=DUP_SIZE, mad_thresh=DUP_MAD):
    """Union-find over image pairs whose size x size gray thumbnails differ by less than mad_thresh on average."""
    X = np.zeros((len(items), size * size), np.float32)
    for i, it in enumerate(items):
        g = cv2.imread(it["img"], cv2.IMREAD_GRAYSCALE)
        X[i] = cv2.resize(g, (size, size), interpolation=cv2.INTER_AREA).astype(np.float32).ravel()
    parent = list(range(len(items)))

    def find_root(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    n_pairs = 0
    for i in range(len(items) - 1):
        d = np.abs(X[i + 1:] - X[i]).mean(axis=1)
        for j in np.nonzero(d < mad_thresh)[0]:
            n_pairs += 1
            ra, rb = find_root(i), find_root(i + 1 + int(j))
            if ra != rb:
                parent[rb] = ra
    return {it["key"]: find_root(i) for i, it in enumerate(items)}, n_pairs


_audit_items = [it for it in dataset if it["key"] in gt_by_key]
_t0 = time.time()
_gid, _n_pairs = find_dup_groups(_audit_items)
_groups = defaultdict(list)
for _k, _g in _gid.items():
    _groups[_g].append(_k)
_multi = [v for v in _groups.values() if len(v) > 1]
_sizes = sorted((len(v) for v in _groups.values()), reverse=True)
print(f"\nNear-duplicate check ({DUP_SIZE}px thumbnails, mean abs diff < {DUP_MAD:g}): {_n_pairs} similar pairs, "
      f"{len(_multi)} groups with >1 image ({sum(len(v) for v in _multi)} images), largest group {_sizes[0]}  [{time.time() - _t0:.0f} s]")
print(f"  groups spanning several splits: {sum(len({x.split('/')[0] for x in v}) > 1 for v in _multi)}"
      f" | groups with mixed OK/NG labels: {sum(len({gt_by_key[x]['gt_pred'] for x in v}) > 1 for v in _multi)}")

DUP_GROUP_OF = {}
if not _multi:
    print("  -> no near-duplicates found: the plain stratified folds are fine (GROUP_FOLDS has no effect).")
elif _sizes[0] > 0.2 * len(_audit_items):
    print(f"  WARNING: the largest group ({_sizes[0]}) is bigger than one CV fold -> DUP_MAD is too loose for this data, grouping switched off. "
          "Lower DUP_MAD (e.g. 0.5) and run this cell again.")
elif GROUP_FOLDS:
    DUP_GROUP_OF = _gid
    print("  -> duplicates found: Section 11 keeps every group inside one fold (the weights / result caches get a '_grp' tag, so old random-fold caches are not reused).")
else:
    print("  -> duplicates found but GROUP_FOLDS = False: the CV numbers may be optimistic.")
