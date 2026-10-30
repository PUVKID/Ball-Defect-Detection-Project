RUN_SWEEPS = True
SWEEP_LEVELS = dict(
    blur=[0, 8, 16, 32, 64, 128, 256],
    noise=[0, 10, 20, 40, 80, 120],
    resolution=[IMGSZ, 960, 640, 480, 320, 224],      # multiples of 32
    data=[1.0, 0.5, 0.25, 0.1, 0.05],
)
SWEEP_ORDER = ["blur", "noise", "resolution", "data"]
SWEEP_CLEAN_FILTERED = True


class _OriginalRef:
    """Identity filter that shares the 'original' image folder with the baseline (no extra copy on disk)."""
    root_key = "original"

    def __call__(self, t):
        return t

    def describe(self):
        return "-"

    def signature(self):
        return ""


SAME = _OriginalRef()


def set_condition(noise=0.0, train_frac=1.0, imgsz=None):
    """Switches the global stress settings that the CV functions read (noise, training share, detector size)."""
    global STRESS_NOISE_STD, STRESS_TRAIN_FRAC, STRESS_IMGSZ, CV_IMGSZ, _STRESS_TAG
    STRESS_NOISE_STD, STRESS_TRAIN_FRAC, STRESS_IMGSZ = noise, train_frac, imgsz
    CV_IMGSZ = imgsz or IMGSZ
    _STRESS_TAG = f"_n{noise:g}" if noise else ""


def cleanup_filtered(name, fn):
    root = filtered_root_for(name, fn)
    shutil.rmtree(root, ignore_errors=True)
    for d in glob.glob(os.path.abspath(root) + f"_cv{CV_FOLDS}f*") + glob.glob(os.path.abspath(root) + "_os"):
        shutil.rmtree(d, ignore_errors=True)


_BASE_COND = dict(noise=STRESS_NOISE_STD, frac=STRESS_TRAIN_FRAC, imgsz=STRESS_IMGSZ)
_BASELINE_VALUE = dict(blur=0, noise=_BASE_COND["noise"], resolution=_BASE_COND["imgsz"] or IMGSZ, data=_BASE_COND["frac"])
_LABEL = dict(blur=lambda v: "Original" if v == 0 else f"σ{v:g}", noise=lambda v: "Original" if v == 0 else f"noise {v:g}",
              resolution=lambda v: f"{v}px", data=lambda v: f"{int(round(100 * v))}%")
SWEEP_TITLE = dict(blur=("blur strength", "Gaussian blur σ (px)"), noise=("noise level", "Gaussian noise std (gray levels)"),
                   resolution=("input resolution", "Detector input size (px)"), data=("training data amount", "Share of training images used"))


def _sweep_levels(axis):
    lv = list(SWEEP_LEVELS[axis])
    base = _BASELINE_VALUE[axis]
    lv = [base] + [v for v in lv if v != base]
    if RUN_PRESET == "quick" and len(lv) > 3:
        lv = [lv[0], lv[len(lv) // 2], lv[-1]]
    return lv


def _level_name_and_cond(axis, v):
    cond = dict(_BASE_COND)
    if axis == "blur":
        return f"Blur sigma={v:g}", ParamFilter(f"Blur sigma={v:g}", gaussian_blur_gpu, dict(sigma=float(v))), cond
    if axis == "noise":
        cond["noise"] = v
        return f"Noise std={v:g}", SAME, cond
    if axis == "resolution":
        cond["imgsz"] = v
        return f"Res {v}", SAME, cond
    cond["frac"] = v
    return f"Data {int(round(100 * v))}pct", SAME, cond


def run_condition(name, fn, noise, frac, imgsz):
    """One 5-fold CV run of `fn` under a stress condition (cached; the settings are restored afterwards)."""
    prev = (STRESS_NOISE_STD, STRESS_TRAIN_FRAC, STRESS_IMGSZ)
    set_condition(noise, frac, imgsz)
    try:
        r = cached_result(name, fn)
        if r is not None:
            print(f"  [{name}] reusing the saved result")
            return r
        t0 = time.time()
        r = evaluate_cv(name, fn, eval_items)
        r["params"] = f"{filter_params_str(fn)} | noise {noise:g}, train share {frac:g}, imgsz {CV_IMGSZ}"
        save_result(name, fn, r)
        if SWEEP_CLEAN_FILTERED and not (fn is SAME and not noise):
            cleanup_filtered(name, fn)
        r["minutes"] = (time.time() - t0) / 60
        return r
    finally:
        set_condition(*prev)


SWEEP_RESULTS, NOISE_BY_LEVEL = {}, {}
if RUN_SWEEPS and not USE_CV:
    print("Sweeps need USE_CV = True (FILTER_MODE = 'train_per_filter') -> skipped.")
elif RUN_SWEEPS:
    _n_new = sum(len(_sweep_levels(a)) - 1 for a in SWEEP_ORDER) * len(_run_folds)
    print(f"Sweeps: {_n_new} new trainings ({FILTER_EPOCHS} epochs each, roughly {_n_new * 2 / 60:.1f} h on a fast GPU; "
          "low-resolution and low-data levels are faster).")
    for axis in SWEEP_ORDER:
        res = []
        for v in _sweep_levels(axis):
            lbl = _LABEL[axis](v)
            if v == _BASELINE_VALUE[axis]:
                r = dict(baseline_result, label=lbl)
            else:
                nm, fn, cond = _level_name_and_cond(axis, v)
                print(f"\n[Sweep {axis}] {lbl}  ({nm}) ...")
                r = dict(run_condition(nm, fn, cond["noise"], cond["frac"], cond["imgsz"]), label=lbl)
                print("  -> " + _result_line(r))
            res.append(r)
            if axis == "noise":
                NOISE_BY_LEVEL[v] = r
        SWEEP_RESULTS[axis] = res
        print(f"\n[Sweep {axis}] summary")
        print(f"  {'level':>8s} | {'accuracy':>8s} | {'bal.acc':>7s} | {'ball rec.':>9s} | {'mAP50-95':>8s} | {'fold std':>8s}")
        for r in res:
            print(f"  {r['label']:>8s} | {r['accuracy']:7.2f}% | {r['bal_acc']:6.2f}% | {r['ball_recall']:8.2f}% | "
                  f"{r['map50_95']:7.1f}% | {r['fold_std']:7.2f}")