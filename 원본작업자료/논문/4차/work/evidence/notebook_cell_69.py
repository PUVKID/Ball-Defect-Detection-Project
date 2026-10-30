# ── 29. Real OK/NG list ───────────────────────────────────────────────────────────────────────────────
REAL_LABEL_CSV = None            # e.g. r"/root/추계학술대회/real_okng.csv"   (columns: name,label)
REAL_LABEL_DIRS = {}             # e.g. {"OK": r"/root/.../OK", "NG": r"/root/.../NG"}
REAL_LABEL_FROM_NAME = False
REAL_LABEL_COLUMNS = ("name", "label")


def _norm_label(v):
    s = str(v).strip().upper()
    if s in ("OK", "GOOD", "PASS", "양품", "정상"):
        return "OK"
    if s in ("NG", "BAD", "FAIL", "불량"):
        return "NG"
    return None


def load_real_labels(csv_path=None, dirs=None, from_name=False, items=()):
    """stem -> 'OK' / 'NG' from a CSV, from folders, and / or from the file names."""
    real = {}
    if csv_path and os.path.isfile(csv_path):
        with open(csv_path, newline="", encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                nm, lab = (r.get(REAL_LABEL_COLUMNS[0]) or "").strip(), _norm_label(r.get(REAL_LABEL_COLUMNS[1]) or "")
                if nm and lab:
                    real[os.path.splitext(os.path.basename(nm))[0]] = lab
    for lab, d in (dirs or {}).items():
        lab = _norm_label(lab)
        if lab is None or not os.path.isdir(d):
            continue
        for p in glob.glob(os.path.join(d, "**", "*"), recursive=True):
            if p.lower().endswith(IMG_EXTS):
                real[os.path.splitext(os.path.basename(p))[0]] = lab
    if from_name:
        for it in items:
            low = it["stem"].lower()
            m = re.search(r"(?<![a-z])(ok|ng)(?![a-z])", low)
            lab = m.group(1).upper() if m else ("OK" if "양품" in low else ("NG" if "불량" in low else None))
            if lab:
                real[it["stem"]] = lab
    return real


def match_real_labels(real, items):
    """key -> label. Exact stem first, then a unique prefix match (followed by a non-alphanumeric character or the end)."""
    by_stem = {}
    for it in items:
        by_stem.setdefault(it["stem"], []).append(it["key"])
    out, ambiguous, unmatched = {}, [], []
    for rs, lab in real.items():
        if rs in by_stem:
            for k in by_stem[rs]:
                out[k] = lab
            continue
        pat = re.compile(re.escape(rs) + r"(?![0-9A-Za-z])")
        cands = [k for st, ks in by_stem.items() if pat.match(st) for k in ks]
        if len(cands) == 1:
            out[cands[0]] = lab
        elif cands:
            ambiguous.append(rs)
        else:
            unmatched.append(rs)
    return out, ambiguous, unmatched


def wilson_ci(k, n, z=1.96):
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100.0 * (c - h), 100.0 * (c + h)


REAL_RESULT = {}
if REAL_LABEL_CSV or REAL_LABEL_DIRS or REAL_LABEL_FROM_NAME:
    _real = load_real_labels(REAL_LABEL_CSV, REAL_LABEL_DIRS, REAL_LABEL_FROM_NAME, CV_ITEMS)
    REAL_BY_KEY, _amb, _unm = match_real_labels(_real, CV_ITEMS)
    print(f"Real labels read: {len(_real)} | matched to dataset images: {len(REAL_BY_KEY)} of {len(CV_ITEMS)} | ambiguous: {len(_amb)} | not found in the dataset: {len(_unm)}")
    if _unm:
        print("   e.g. not found:", _unm[:5], "| dataset names look like:", [it["stem"] for it in CV_ITEMS[:3]])
    if len(REAL_BY_KEY) < 0.5 * len(CV_ITEMS):
        print("WARNING: fewer than half of the images are matched -> check REAL_LABEL_* and the file names before using the numbers below.")
    _keys = [k for k in REAL_BY_KEY if k in gt_by_key]
    if _keys:
        _agree = sum(gt_by_key[k]["gt_pred"] == REAL_BY_KEY[k] for k in _keys)
        lo, hi = wilson_ci(_agree, len(_keys))
        print(f"\n(29-1) Label rule vs real list: {_agree}/{len(_keys)} = {100 * _agree / len(_keys):.2f}%  (95% Wilson CI {lo:.1f} - {hi:.1f})")
        cm = pd.crosstab(pd.Series([REAL_BY_KEY[k] for k in _keys], name="real"), pd.Series([gt_by_key[k]["gt_pred"] for k in _keys], name="label rule"))
        display(cm)
        _dis = [dict(key=k, real=REAL_BY_KEY[k], label_rule=gt_by_key[k]["gt_pred"], n_balls=len(gt_by_key[k]["gt_boxes"]),
                     counts=json.dumps(gt_by_key[k]["gt_counts"]), loc_fail=bool(gt_by_key[k].get("loc_fail")))
                for k in _keys if gt_by_key[k]["gt_pred"] != REAL_BY_KEY[k]]
        pd.DataFrame(_dis).to_csv(os.path.join(FILTER_FIG_DIR, "real_label_disagreements.csv"), index=False, encoding="utf-8-sig")
        print(f"   {len(_dis)} disagreeing images saved to real_label_disagreements.csv "
              f"(rule OK / real NG: {sum(d['real'] == 'NG' for d in _dis)} -> defect not visible in the ball pattern; "
              f"rule NG / real OK: {sum(d['real'] == 'OK' for d in _dis)} -> labelling or rectangle problem)")
        _rows = []
        for nm, per in PER_IMAGE.items():
            sub = [r for r in per if r["key"] in REAL_BY_KEY]
            if len(sub) < 20 or nm.startswith(("HARD ", "Noise std", "Blur sigma", "Data ", "Res ")) or "| noise" in nm:
                continue
            a = sum(r["pred"] == REAL_BY_KEY[r["key"]] for r in sub)
            _rows.append({"Method": nm, "n": len(sub), "Agreement with real (%)": 100.0 * a / len(sub),
                          "Agreement with label rule (%)": 100.0 * sum(r["pred"] == r["gt_pred"] for r in sub) / len(sub)})
        if _rows:
            _rdf = pd.DataFrame(_rows).sort_values("Agreement with real (%)", ascending=False)
            print("\n(29-2) Every method against the real list (normal condition):")
            display(_rdf.round(2))
            _rdf.round(3).to_csv(os.path.join(FILTER_FIG_DIR, "real_label_methods.csv"), index=False, encoding="utf-8-sig")
        if "Original" in PER_IMAGE:
            _o = {r["key"]: r for r in PER_IMAGE["Original"] if r["key"] in REAL_BY_KEY}
            _b = sum(gt_by_key[k]["gt_pred"] == REAL_BY_KEY[k] and _o[k]["pred"] != REAL_BY_KEY[k] for k in _o)
            _c = sum(gt_by_key[k]["gt_pred"] != REAL_BY_KEY[k] and _o[k]["pred"] == REAL_BY_KEY[k] for k in _o)
            print(f"\n(29-3) Original detector vs label rule, both judged against the real list: rule right / detector wrong {_b}, "
                  f"rule wrong / detector right {_c}, exact McNemar p = {mcnemar_exact(_b, _c):.4f}")
            _ok_real = [k for k in _o if REAL_BY_KEY[k] == "NG"]
            _ng_rec = sum(_o[k]["pred"] == "NG" for k in _ok_real)
            print(f"   real-NG images the detector flags: {_ng_rec}/{len(_ok_real)} ({100 * _ng_rec / max(len(_ok_real), 1):.1f}%) | "
                  f"real-OK images it passes: {sum(_o[k]['pred'] == 'OK' for k in _o if REAL_BY_KEY[k] == 'OK')}/{sum(REAL_BY_KEY[k] == 'OK' for k in _o)}")
        REAL_RESULT = dict(n_matched=len(_keys), rule_agree=_agree, rule_agree_pct=100.0 * _agree / len(_keys), ci=[lo, hi], n_disagree=len(_dis))
else:
    print("Real OK/NG list not given (REAL_LABEL_CSV / REAL_LABEL_DIRS / REAL_LABEL_FROM_NAME) -> section skipped; the paper keeps this as a limitation.")