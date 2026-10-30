# ── 31. Paper numbers + bundle ────────────────────────────────────────────────────────────────────────
print("=" * 70)
print("v7 summary for the paper")
print("=" * 70)
PAPER_V7 = {}
if GHOST_ROWS:
    _p, _n_, _v = ghost_summary(GHOST_ROWS)
    PAPER_V7["ghost"] = dict(table=_p.round(2).to_dict(), verdict=_v)
    print("  [28a] ghost-at-erased-site % per method x site:", _p.round(1).to_dict())
    print("        ->", _v)
if SHORTCUT_DIAG.get("thumbnail"):
    PAPER_V7["thumbnail"] = SHORTCUT_DIAG["thumbnail"]
    for r in SHORTCUT_DIAG["thumbnail"]:
        print(f"  [28b] {r['Input']}: accuracy {r['Accuracy (%)']:.1f}% | balanced {r['Balanced (%)']:.1f}%")
if SHORTCUT_DIAG.get("global_auc"):
    PAPER_V7["global_auc"] = SHORTCUT_DIAG["global_auc"]
    print("  [28b] global-feature AUC:", {r["Feature"]: round(r["AUC (NG vs OK)"], 2) for r in SHORTCUT_DIAG["global_auc"]})
if OP_RESULT:
    PAPER_V7["operating_point"] = OP_RESULT
    print(f"  [28c] strict without the {OP_RESULT['n_fail']} fallback images: {OP_RESULT['strict_without_fail']:.1f}% (accuracy {OP_RESULT['acc_without_fail']:.1f}%)")
if REAL_RESULT:
    PAPER_V7["real_label"] = REAL_RESULT
    print(f"  [29]  label rule vs real list: {REAL_RESULT['rule_agree']}/{REAL_RESULT['n_matched']} = {REAL_RESULT['rule_agree_pct']:.2f}% "
          f"(CI {REAL_RESULT['ci'][0]:.1f} - {REAL_RESULT['ci'][1]:.1f}), {REAL_RESULT['n_disagree']} disagree")
for cond, df in MS_TABLES.items():
    PAPER_V7[f"ms::{cond}"] = df.round(3).to_dict(orient="records")
    print(f"\n  [30] {cond}")
    for _, r in df.sort_values("Strict mean", ascending=False).iterrows():
        extra = "" if r["Method"] == "Original" else f" | delta {r['Delta vs Original (pp)']:+.1f} pp [{r['CI low']:+.1f}, {r['CI high']:+.1f}] seeds better {r['seeds better']} -> {r['Verdict']}"
        print(f"      {r['Method']:<24s} strict {r['Strict mean']:5.1f} +- {r['Strict std']:4.1f} | accuracy {r['Acc mean']:5.1f} +- {r['Acc std']:4.1f}{extra}")

with open(os.path.join(FILTER_FIG_DIR, "paper_numbers_v7.json"), "w", encoding="utf-8") as f:
    json.dump(PAPER_V7, f, ensure_ascii=False, indent=1, default=float)

import zipfile
_patterns = ("ms_*.csv", "diag_*.csv", "real_label_*.csv", "table_*.csv", "verification_summary.*", "paper_numbers_v7.json",
             "fig_multiseed_strict.png", "fig_hard_shift_strict_heatmap.png", "hard_shift_*.json")
_bundle = os.path.join(FILTER_FIG_DIR, "v7_results_bundle.zip")
with zipfile.ZipFile(_bundle, "w", zipfile.ZIP_DEFLATED) as z:
    _seen = set()
    for pat in _patterns:
        for p in glob.glob(os.path.join(FILTER_FIG_DIR, pat)):
            if p not in _seen:
                z.write(p, os.path.basename(p))
                _seen.add(p)
print(f"\nBundle: {os.path.abspath(_bundle)} ({len(_seen)} files)")
print("Send back: the .ipynb with outputs (and the zip if the notebook is too big).")