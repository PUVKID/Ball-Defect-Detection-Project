# ── 26a. Difficulty strata + strict-accuracy McNemar (re-uses the saved per-image results, no training) ──
_names_all = ["Original"] + [n for n, _ in FILTERS_ROUND1] + [n for n, _ in FILTERS_ROUND2]
_names_all = [n for n in _names_all if n in PER_IMAGE]
print("Images per stratum: " + ", ".join(f"{d}: {sum(difficulty_of(it['key']) == d for it in CV_ITEMS)}" for d in STRAT_ORDER))
strat_df = stratified_table(_names_all)
display(strat_df.round(1))
strat_df.to_csv(os.path.join(FILTER_FIG_DIR, "table_stratified.csv"), index=False, encoding="utf-8-sig")

_rows = []
for nm in _names_all:
    if nm == "Original":
        continue
    b, c, p = strict_mcnemar("Original", nm)
    _s = lambda name: 100.0 * np.mean([int(r.get("miss") == 0 and r.get("extra") == 0) for r in PER_IMAGE[name]])
    _rows.append({"Method": nm, "Strict Acc (%)": _s(nm), "vs Original (pp)": _s(nm) - _s("Original"),
                  "newly worse": b, "newly better": c, "McNemar p": p,
                  "Significant (Bonferroni)": "Yes" if p < 0.05 / max(len(_names_all) - 1, 1) else "No"})
_sdf = pd.DataFrame(_rows).sort_values("Strict Acc (%)", ascending=False)
print(f"\nStrict accuracy of Original: {100.0 * np.mean([int(r.get('miss') == 0 and r.get('extra') == 0) for r in PER_IMAGE['Original']]):.2f}%  "
      f"(Bonferroni threshold {0.05 / max(len(_names_all) - 1, 1):.4f})")
display(_sdf.round({"Strict Acc (%)": 2, "vs Original (pp)": 2, "McNemar p": 4}))
_sdf.to_csv(os.path.join(FILTER_FIG_DIR, "table_strict_mcnemar.csv"), index=False, encoding="utf-8-sig")
