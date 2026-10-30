import os, sys, glob, json, math, time, random, csv, shutil, hashlib
from collections import Counter, defaultdict
import numpy as np
import cv2

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

_missing = []
try:
    from joblib import Parallel, delayed
except ImportError:
    _missing.append("joblib")
try:
    from ultralytics import YOLO
except ImportError:
    _missing.append("ultralytics")
try:
    import pandas as pd
except ImportError:
    _missing.append("pandas")
try:
    import yaml
except ImportError:
    _missing.append("pyyaml")
try:
    import torch
    import torch.nn.functional as F
except ImportError:
    _missing.append("torch")
try:
    import kornia
    import kornia.filters
    import kornia.enhance
except ImportError:
    _missing.append("kornia")
if _missing:
    raise RuntimeError(f"The following packages are required. Install them and restart the kernel:\n    pip install {' '.join(_missing)}")

try:
    from IPython.display import display
except ImportError:
    display = print

# ── GPU setup (every filter runs as a GPU tensor op) ──
REQUIRE_GPU = True
if torch.cuda.is_available():
    DEVICE = torch.device("cuda")
    print(f"Using GPU: {torch.cuda.get_device_name(0)}")
elif REQUIRE_GPU:
    raise RuntimeError("No CUDA GPU found (torch.cuda.is_available() == False). Check the CUDA driver / PyTorch-CUDA "
                       "install, or set REQUIRE_GPU = False to run the filters on the CPU (very slow).")
else:
    DEVICE = torch.device("cpu")
    print("WARNING: no GPU found, the filters will run on the CPU.")
print(f"PyTorch: {torch.__version__} / CUDA: {torch.version.cuda}")

# ── Font setup ─────────────────────────────────────────────────────
font_path = r"C:\Users\PUVKID\AppData\Local\Microsoft\Windows\Fonts\NanumGothic.ttf"
font_bold_path = r"C:\Users\PUVKID\AppData\Local\Microsoft\Windows\Fonts\NanumGothicBold.ttf"
_linux_fallback = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
_linux_fallback_bold = "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf"

if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    if os.path.exists(font_bold_path):
        fm.fontManager.addfont(font_bold_path)
    font_name = fm.FontProperties(fname=font_path).get_name()
elif os.path.exists(_linux_fallback):
    fm.fontManager.addfont(_linux_fallback)
    if os.path.exists(_linux_fallback_bold):
        fm.fontManager.addfont(_linux_fallback_bold)
    font_name = fm.FontProperties(fname=_linux_fallback).get_name()
else:
    font_name = "DejaVu Sans"
    print("NanumGothic font not found. Falling back to DejaVu Sans.")

matplotlib.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": [font_name, "DejaVu Sans"], "axes.unicode_minus": False,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "axes.edgecolor": "#222222", "axes.labelcolor": "#222222",
    "xtick.color": "#222222", "ytick.color": "#222222", "text.color": "#222222",
    "grid.color": "#d9d9d9", "grid.linestyle": "-", "grid.alpha": 0.8,
    "legend.facecolor": "white", "legend.edgecolor": "#bbbbbb", "legend.labelcolor": "#222222",
})

FIG_DIR = "yolo_ok_ng_figures"              # baseline graphs (Sections 1~8)
RUNS_DIR = "yolo_runs"                      # YOLO training runs
FILTER_FIG_DIR = "yolo_filter_figures"      # filter experiment: graphs + tables
FILTER_SAMPLE_DIR = "yolo_filter_samples"   # filter experiment: Original vs filtered examples
FILTERED_ROOT = "yolo_filtered_datasets"    # only used when FILTER_MODE = "train_per_filter"
for _d in (FIG_DIR, FILTER_FIG_DIR, FILTER_SAMPLE_DIR):
    os.makedirs(_d, exist_ok=True)
print(f"Baseline figure folder: {os.path.abspath(FIG_DIR)}")
print(f"Filter experiment figure folder: {os.path.abspath(FILTER_FIG_DIR)}")
print(f"Logical cores: {os.cpu_count()}")

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)