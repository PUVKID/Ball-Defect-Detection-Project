# ── 30b. Multi-seed report ────────────────────────────────────────────────────────────────────────────
def _strict_vec(rows):
    return {r["key"]: int(r.get("miss") == 0 and r.get("extra") == 0) for r in rows}


def _acc_vec(rows):
    return {r["key"]: int(r["match"]) for r in rows}


def ms_cluster_boot(diff_by_key, group_of, n_boot=5000, seed=0):
    """Mean of the per-image differences and its 95% percentile CI when whole near-duplicate groups are resampled."""
    keys = sorted(diff_by_key)
    uniq = {}
    idx = np.array([uniq.setdefault(group_of.get(k, k), len(uniq)) for k in keys])
    d = np.array([diff_by_key[k] for k in keys], float)
    c = len(uniq)
    S = np.bincount(idx, weights=d, minlength=c)
    N = np.bincount(idx, minlength=c).astype(float)
    pick = np.random.default_rng(seed).integers(0, c, (n_boot, c))
    boots = S[pick].sum(axis=1) / N[pick].sum(axis=1)
    return float(d.mean()), float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))


def ms_report(rows_by, seeds, conditions, ref="Original", group_of=None, n_boot=5000):
    """One DataFrame per condition (see Section 30 text). rows_by[(cond, seed, method)] = per-image rows."""
    group_of = group_of or {}
    tables = {}
    for cond, spec in conditions.items():
        methods = [m for m in spec["methods"] if all((cond, s, m) in rows_by for s in seeds)]
        if ref not in methods:
            continue
        seeds_ = list(seeds)
        sv = {m: {s: _strict_vec(rows_by[(cond, s, m)]) for s in seeds_} for m in methods}
        av = {m: {s: _acc_vec(rows_by[(cond, s, m)]) for s in seeds_} for m in methods}
        rec = []
        for m in methods:
            ps = [100.0 * np.mean(list(sv[m][s].values())) for s in seeds_]
            pa = [100.0 * np.mean(list(av[m][s].values())) for s in seeds_]
            r = {"Method": m}
            for s, v in zip(seeds_, ps):
                r[f"strict s{s}"] = v
            r["Strict mean"], r["Strict std"] = float(np.mean(ps)), (float(np.std(ps, ddof=1)) if len(ps) > 1 else float("nan"))
            r["Acc mean"], r["Acc std"] = float(np.mean(pa)), (float(np.std(pa, ddof=1)) if len(pa) > 1 else float("nan"))
            if m != ref:
                ref_ps = [100.0 * np.mean(list(sv[ref][s].values())) for s in seeds_]
                deltas = [a - b for a, b in zip(ps, ref_ps)]
                keys = set.intersection(*[set(sv[m][s]) & set(sv[ref][s]) for s in seeds_])
                dk = {k: float(np.mean([sv[m][s][k] - sv[ref][s][k] for s in seeds_])) for k in keys}
                mean_d, lo, hi = ms_cluster_boot(dk, group_of, n_boot)
                pvals = []
                for s in seeds_:
                    b = sum(sv[ref][s][k] == 1 and sv[m][s][k] == 0 for k in keys)
                    c = sum(sv[ref][s][k] == 0 and sv[m][s][k] == 1 for k in keys)
                    pvals.append(mcnemar_exact(b, c))
                r.update({"Delta vs Original (pp)": 100.0 * mean_d, "CI low": 100.0 * lo, "CI high": 100.0 * hi,
                          "seeds better": f"{sum(d > 0 for d in deltas)}/{len(deltas)}", "seeds worse": f"{sum(d < 0 for d in deltas)}/{len(deltas)}",
                          "per-seed McNemar p": " / ".join(f"{p:.3g}" for p in pvals)})
                same_sign = all(d > 0 for d in deltas) or all(d < 0 for d in deltas)
                r["Verdict"] = ("robust better" if mean_d > 0 else "robust worse") if (same_sign and (lo > 0 or hi < 0)) else (
                    "inconsistent" if not same_sign else "not significant")
            rec.append(r)
        tables[cond] = pd.DataFrame(rec)
    return tables


MS_TABLES = {}
if RUN_MULTISEED and USE_CV and MS_ROWS:
    MS_TABLES = ms_report(MS_ROWS, MS_SEEDS, MS_CONDITIONS, group_of=globals().get("DUP_GROUP_OF", {}))
    for cond, df in MS_TABLES.items():
        print(f"\n=== {cond}: strict accuracy (%) over seeds {MS_SEEDS}  (std = across seeds, ddof=1) ===")
        display(df.round(2))
        df.round(3).to_csv(os.path.join(FILTER_FIG_DIR, f"ms_table_{safe_filename(cond)}.csv"), index=False, encoding="utf-8-sig")
    _n = len(MS_TABLES)
    if _n:
        _fig, _axes = plt.subplots(1, _n, figsize=(6.5 * _n, 4.6), squeeze=False)
        for ax, (cond, df) in zip(_axes[0], MS_TABLES.items()):
            x = np.arange(len(df))
            ax.bar(x, df["Strict mean"], yerr=df["Strict std"].fillna(0), capsize=4, color="#9bb7d4", edgecolor="black")
            for s in MS_SEEDS:
                ax.scatter(x, df[f"strict s{s}"], s=26, zorder=3, label=f"seed {s}")
            ax.set_xticks(x)
            ax.set_xticklabels(df["Method"], rotation=30, ha="right", fontsize=11)
            ax.set_ylabel("Strict accuracy (%)")
            ax.set_title(cond, fontsize=13)
            ax.set_ylim(0, 105)
            ax.grid(axis="y", alpha=0.3)
        _axes[0][0].legend(fontsize=9)
        _fig.tight_layout()
        _p = os.path.join(FILTER_FIG_DIR, "fig_multiseed_strict.png")
        _fig.savefig(_p, dpi=300, bbox_inches="tight", facecolor="white")
        plt.show()
        print(f"Saved: {_p}")
elif RUN_MULTISEED:
    print("No multi-seed rows (USE_CV off or the runs were skipped).")