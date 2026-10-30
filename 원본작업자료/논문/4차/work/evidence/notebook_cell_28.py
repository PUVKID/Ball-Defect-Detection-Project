# ── The filters of the experiment: function + fixed (maximum-strength) parameters ──
FILTER_SPECS = {
    "Invert": dict(fn=invert_gpu, params={}),
    "Otsu Threshold": dict(fn=otsu_threshold_gpu, params={}),
    "Solarize": dict(fn=solarize_gpu, params={}),
    "Histogram Equalization": dict(fn=hist_equalize_gpu, params={}),
    "CLAHE (max)": dict(fn=clahe_gpu, params=dict(clip_limit=40.0, tiles=16)),
    "Gamma 0.3": dict(fn=gamma_gpu, params=dict(gamma=0.3)),
    "Gaussian Blur (max)": dict(fn=gaussian_blur_gpu, params=dict(sigma=20.0)),
    "Sobel Edges": dict(fn=sobel_edges_gpu, params={}),
    "Emboss": dict(fn=emboss_gpu, params=dict(gain=4.0)),
    "Unsharp (max)": dict(fn=unsharp_gpu, params=dict(amount=8.0, sigma=2.0)),
}
ROUND1_ORDER = list(FILTER_SPECS)

ROUND2_COMBOS = {   # combined filter -> (first stage, second stage); "A+B" = A first, then B
    "Invert+CLAHE": ("Invert", "CLAHE (max)"),
    "Blur+Otsu": ("Gaussian Blur (max)", "Otsu Threshold"),
    "Sobel+Invert": ("Sobel Edges", "Invert"),
    "HistEq+Emboss": ("Histogram Equalization", "Emboss"),
    "Unsharp+Sobel": ("Unsharp (max)", "Sobel Edges"),
}


def make_filter(name):
    spec = FILTER_SPECS[name]
    return ParamFilter(name, spec["fn"], spec["params"])


def build_filter_lists():
    """(Round 1, Round 2) lists of (name, filter)."""
    r1 = [(n, make_filter(n)) for n in ROUND1_ORDER]
    r2 = [(cn, Chain(make_filter(a), make_filter(b))) for cn, (a, b) in ROUND2_COMBOS.items()]
    return r1, r2


FILTERS_ROUND1, FILTERS_ROUND2 = build_filter_lists()
print(f"Round 1: {len(FILTERS_ROUND1)} single filters registered: {[n for n, _ in FILTERS_ROUND1]}")
print(f"Round 2: {len(FILTERS_ROUND2)} combined filters registered: {[n for n, _ in FILTERS_ROUND2]}")
