def _sync():
    if torch.cuda.is_available():
        torch.cuda.synchronize()


def to_gpu_tensor(gray_np):
    t = torch.from_numpy(gray_np).float().to(DEVICE) / 255.0
    return t.unsqueeze(0).unsqueeze(0)  # (1,1,H,W)


def to_gray_np(t):
    arr = t.detach().squeeze().clamp(0, 1).cpu().numpy()
    return (arr * 255.0).round().astype(np.uint8)


def identity_filter(t):
    """'Original' baseline: no filtering."""
    return t


# ── A filter together with the parameters it is run with ──────────
class ParamFilter:
    """A filter function bound to its parameters, so tables and caches show exactly what was run."""

    def __init__(self, name, fn, params):
        self.name, self.fn, self.params = name, fn, dict(params)

    def __call__(self, t):
        return self.fn(t, **self.params)

    def describe(self):
        return ", ".join(f"{k}={v}" for k, v in self.params.items()) or "-"

    def signature(self):
        return json.dumps({self.name: self.params}, sort_keys=True)


class Chain:
    """Two filters applied one after the other (first stage first)."""

    def __init__(self, *stages):
        self.stages = stages

    def __call__(self, t):
        for stage in self.stages:
            t = stage(t)
        return t

    def describe(self):
        return " > ".join(f"{s.name}[{s.describe()}]" for s in self.stages)

    def signature(self):
        return "|".join(s.signature() for s in self.stages)


# ── 1) Invert (negative image) ───────────────────────────────────
def invert_gpu(t):
    return 1.0 - t


# ── 2) Otsu threshold (black-and-white image, automatic threshold) ──
def otsu_threshold_gpu(t):
    x = (t.clamp(0, 1) * 255).round()
    hist = torch.histc(x, bins=256, min=0, max=256)            # bin i = gray level i
    p = hist / hist.sum()
    levels = torch.arange(256, device=t.device, dtype=t.dtype)
    omega = torch.cumsum(p, dim=0)                              # share of pixels <= level
    mu = torch.cumsum(p * levels, dim=0)
    sigma_between = (mu[-1] * omega - mu) ** 2 / (omega * (1 - omega)).clamp(min=1e-12)
    thr = torch.argmax(sigma_between)
    return (x > thr).to(t.dtype)


# ── 3) Solarize (everything brighter than the image mean is inverted) ──
def solarize_gpu(t):
    return torch.where(t > t.mean(), 1.0 - t, t)


# ── 4) Histogram equalization (global) ───────────────────────────
def hist_equalize_gpu(t):
    return kornia.enhance.equalize(t)


# ── 5) CLAHE with a huge clip limit (maximum local contrast) ─────
def clahe_gpu(t, clip_limit=40.0, tiles=16):
    return kornia.enhance.equalize_clahe(t, clip_limit=clip_limit, grid_size=(tiles, tiles))


# ── 6) Gamma (strong brightening) ────────────────────────────────
def gamma_gpu(t, gamma=0.3):
    return t.clamp(0, 1) ** gamma


# ── 7) Gaussian blur with a huge sigma (fine texture disappears; the balls stay visible as soft blobs) ──
def gaussian_blur_gpu(t, sigma=20.0):
    k = int(sigma * 6) | 1                                      # odd kernel covering +-3 sigma
    return kornia.filters.gaussian_blur2d(t, (k, k), (sigma, sigma), border_type="reflect")


# ── 8) Sobel edge map (stretched to the full range) ──────────────
def sobel_edges_gpu(t):
    g = kornia.filters.sobel(t, normalized=True)
    return (g / g.amax().clamp(min=1e-6)).clamp(0, 1) ** 0.5


# ── 9) Emboss (relief) ───────────────────────────────────────────
def emboss_gpu(t, gain=4.0):
    k = torch.tensor([[-2.0, -1.0, 0.0], [-1.0, 0.0, 1.0], [0.0, 1.0, 2.0]], device=t.device, dtype=t.dtype).view(1, 1, 3, 3)   # weights sum to 0: flat areas -> mid-gray
    out = F.conv2d(F.pad(t, (1, 1, 1, 1), mode="reflect"), k)
    return (gain * out + 0.5).clamp(0, 1)


# ── 10) Unsharp mask with a huge amount ──────────────────────────
def unsharp_gpu(t, amount=8.0, sigma=2.0):
    k = int(sigma * 6) | 1
    blurred = kornia.filters.gaussian_blur2d(t, (k, k), (sigma, sigma), border_type="reflect")
    return (t + amount * (t - blurred)).clamp(0, 1)
