# ── 27. What to report (printed from the numbers above) ──
print("=" * 70)
print("Summary for the paper")
print("=" * 70)
if VERIFICATION:
    for a, b, c, d in verdict:
        print(f"  [{'PASS ' if d else 'CHECK'}] {a}: {b}   (criterion: {c})")
else:
    print("  (run Section 25b first)")
if SHIFT_RESULTS:
    _best = S.drop(index="Original")["mean"].idxmax()
    print(f"\n  Shift test: mean strict accuracy Original {S.loc['Original', 'mean']:.1f}% | best filter {_best} {S.loc[_best, 'mean']:.1f}% "
          f"({S.loc[_best, 'mean'] - S.loc['Original', 'mean']:+.1f} pp) | worst {S['mean'].idxmin()} {S['mean'].min():.1f}%")
if HARD_RESULTS:
    print("\n  Hard retraining (" + _tag + "):")
    for r in sorted(HARD_RESULTS, key=lambda x: -x["strict_acc"]):
        print(f"    {r['label']:<24s} accuracy {r['accuracy']:6.2f}% | strict {r['strict_acc']:6.2f}% | mAP50-95 {r['map50_95']:5.1f}%")
print("\nReport: (a) Strict Acc and the majority-class baseline next to every accuracy, (b) the verification table, "
      "(c) shift / hard-mode tables with the McNemar p-values, (d) the stratified table (n per stratum). Do not report Sections 5-8.")
