# ── 30a. Multi-seed runs ──────────────────────────────────────────────────────────────────────────────
RUN_MULTISEED = True
MS_SEEDS = [42, 43, 44]
MS_BASE_SEED = SEED                      # the seed of Sections 1-27 (its results are read from the caches, not retrained)
MS_CONDITIONS = {
    "normal": dict(kind="normal", noise=0.0, frac=1.0, imgsz=None,
                   methods=["Original", "Invert", "CLAHE (max)", "Invert+CLAHE"]),
    "hard (noise 40 + 25% data)": dict(kind="hard", noise=40, frac=0.25, imgsz=None,
                                       methods=["Original", "CLAHE (max)", "Histogram Equalization", "Gamma 0.3", "Gaussian Blur (max)", "Invert"]),
    "noise 80": dict(kind="noise", noise=80, frac=1.0, imgsz=None,
                     methods=["Original", "Gaussian Blur (max)", "CLAHE (max)"]),
}
_SEED_TAG = ""                           # "" for the base seed, "_s43" ... otherwise (part of every cache key)


def _noisy(gray, key):                   # [v7] same as v6 for the base seed; a new noise realisation for every other seed
    if not STRESS_NOISE_STD:
        return gray
    k = key + _SEED_TAG
    rng = np.random.default_rng(int(hashlib.md5(k.encode("utf-8")).hexdigest()[:8], 16))
    return np.clip(gray.astype(np.float32) + rng.normal(0.0, STRESS_NOISE_STD, gray.shape), 0, 255).astype(np.uint8)


def set_condition(noise=0.0, train_frac=1.0, imgsz=None):      # [v7] noisy copies of other seeds get their own folder
    global STRESS_NOISE_STD, STRESS_TRAIN_FRAC, STRESS_IMGSZ, CV_IMGSZ, _STRESS_TAG
    STRESS_NOISE_STD, STRESS_TRAIN_FRAC, STRESS_IMGSZ = noise, train_frac, imgsz
    CV_IMGSZ = imgsz or IMGSZ
    _STRESS_TAG = (f"_n{noise:g}" + _SEED_TAG) if noise else ""


class SeedContext:
    """with SeedContext(43): ...  -> new folds, new inner val split, new training seed, new noise realisation, separate cache keys."""

    def __init__(self, seed):
        self.seed = seed

    def __enter__(self):
        g = globals()
        self.saved = {k: g[k] for k in ("SEED", "FOLD_OF", "FOLD_TAG", "_SEED_TAG")}
        g["_MODELS"].clear()
        if self.seed != MS_BASE_SEED:
            g["SEED"] = self.seed
            g["_SEED_TAG"] = f"_s{self.seed}"
            g["FOLD_OF"] = assign_folds(CV_ITEMS, CV_FOLDS, self.seed)
            g["FOLD_TAG"] = self.saved["FOLD_TAG"] + g["_SEED_TAG"]
            set_condition(STRESS_NOISE_STD, STRESS_TRAIN_FRAC, STRESS_IMGSZ)
        return self

    def __exit__(self, *exc):
        g = globals()
        g.update(self.saved)
        g["_MODELS"].clear()
        set_condition(STRESS_NOISE_STD, STRESS_TRAIN_FRAC, STRESS_IMGSZ)
        return False


def _ms_hard_tag(noise, frac, imgsz):
    return f"noise {noise:g}, data {int(round(100 * frac))}%" + (f", {imgsz}px" if imgsz else "")


def ms_method_name(kind, method, noise, frac, imgsz):
    """The names under which Sections 14-26 saved these runs (so the base seed reuses their caches)."""
    if kind == "normal":
        return method
    if kind == "hard":
        return f"HARD {method} | {_ms_hard_tag(noise, frac, imgsz)}"
    if kind == "noise":
        return f"Noise std={noise:g}" if method == "Original" else f"{method} | noise {noise:g}"
    raise ValueError(kind)


def ms_filter(method):
    if method == "Original":
        return SAME
    allf = dict(FILTERS_ROUND1 + FILTERS_ROUND2)
    if method not in allf:
        raise KeyError(f"unknown filter {method!r}; known: {sorted(allf)}")
    return allf[method]


_RES_KEYS = ("accuracy", "bal_acc", "strict_acc", "ball_recall", "map50_95", "fold_std", "pred_ng_pct", "ng_recall", "ok_recall")
MS_ROWS, MS_RES = {}, {}                 # (condition, seed, method) -> per-image rows / scalar results


def ms_cleanup(name, fn, noise, frac, imgsz):
    """Delete the filtered copy of a finished run (several GB). The shared 'original' folder is never touched."""
    if fn is SAME and not noise:
        return
    prev = (STRESS_NOISE_STD, STRESS_TRAIN_FRAC, STRESS_IMGSZ)
    set_condition(noise, frac, imgsz)
    try:
        cleanup_filtered(name, fn)
    finally:
        set_condition(*prev)


def run_multiseed(conditions, seeds):
    global SWEEP_CLEAN_FILTERED
    snapshot = dict(PER_IMAGE)
    clean_prev = SWEEP_CLEAN_FILTERED
    SWEEP_CLEAN_FILTERED = False         # cleaned here instead: a filtered copy is reused by all seeds when it has no noise
    try:
        for cond, spec in conditions.items():
            for method in spec["methods"]:
                fn = ms_filter(method)
                nm = ms_method_name(spec["kind"], method, spec["noise"], spec["frac"], spec["imgsz"])
                for si, seed in enumerate(seeds):
                    print(f"\n[multi-seed] {cond} | {method} | seed {seed}" + ("  (base seed: from the caches)" if seed == MS_BASE_SEED else ""))
                    with SeedContext(seed):
                        r = run_condition(nm, fn, spec["noise"], spec["frac"], spec["imgsz"])
                        MS_ROWS[(cond, seed, method)] = [dict(x) for x in PER_IMAGE[nm]]
                        MS_RES[(cond, seed, method)] = {k: r.get(k) for k in _RES_KEYS}
                        print("  -> " + _result_line(r))
                        if spec["noise"] or si == len(seeds) - 1:
                            ms_cleanup(nm, fn, spec["noise"], spec["frac"], spec["imgsz"])
    finally:
        SWEEP_CLEAN_FILTERED = clean_prev
        PER_IMAGE.clear()
        PER_IMAGE.update(snapshot)       # the multi-seed rows must not overwrite the base-seed rows of the later sections


def ms_count_trainings(conditions, seeds):
    n = 0
    for spec in conditions.values():
        n += len(spec["methods"]) * len([s for s in seeds if s != MS_BASE_SEED]) * CV_FOLDS
    return n


if RUN_MULTISEED and not USE_CV:
    print("Multi-seed needs USE_CV = True -> skipped.")
elif RUN_MULTISEED:
    _n = ms_count_trainings(MS_CONDITIONS, MS_SEEDS)
    print(f"Multi-seed: seeds {MS_SEEDS} (base seed {MS_BASE_SEED} from the caches), {_n} new trainings of {FILTER_EPOCHS} epochs "
          f"-> roughly {_n * 1.5 / 60:.1f} - {_n * 2.5 / 60:.1f} h on a fast GPU (data-25% runs are faster). Cached runs are skipped.")
    run_multiseed(MS_CONDITIONS, MS_SEEDS)
    _rows_out = [dict(condition=c, seed=s, method=m, key=r["key"], gt_pred=r["gt_pred"], pred=r["pred"], match=r["match"],
                      miss=r.get("miss"), extra=r.get("extra")) for (c, s, m), rows in MS_ROWS.items() for r in rows]
    pd.DataFrame(_rows_out).to_csv(os.path.join(FILTER_FIG_DIR, "ms_per_image.csv"), index=False, encoding="utf-8-sig")
    pd.DataFrame([dict(condition=c, seed=s, method=m, **v) for (c, s, m), v in MS_RES.items()]).to_csv(
        os.path.join(FILTER_FIG_DIR, "ms_run_results.csv"), index=False, encoding="utf-8-sig")
    print(f"\nSaved ms_per_image.csv ({len(_rows_out)} rows) and ms_run_results.csv")