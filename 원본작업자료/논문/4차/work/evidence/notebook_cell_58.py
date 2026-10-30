# ── 25b. Run the five checks ──────────────────────────────────────────
VERIFICATION = {}
if not USE_CV:
    print("The checks use the CV fold detectors (USE_CV = True) -> skipped.")
else:
    # (1) permutation test on the saved per-image judgements of Original
    acc1, null1, p1 = permutation_test(PER_IMAGE["Original"])
    VERIFICATION["permutation"] = dict(acc=100 * acc1, null_mean=100 * null1.mean(), null_max=100 * null1.max(), p=p1)
    print(f"(1) Permutation: real accuracy {100 * acc1:.2f}% | shuffled-GT accuracy {100 * null1.mean():.1f}% +- {100 * null1.std():.1f} "
          f"(max over {len(null1)} shuffles {100 * null1.max():.1f}%) | p <= {p1:.4g}")

    # (2)-(4) interventions on the clean OK images, judged by the fold detector that never saw them
    _ok_items = [it for it in eval_items if gt_by_key[it["key"]]["gt_pred"] == "OK" and gt_by_key[it["key"]]["part"] is not None]
    cf = {k: run_counterfactuals(k, _ok_items) for k in ("erase_all", "remove_one", "insert_one")}
    pc = lambda rows, f: 100.0 * sum(f(r) for r in rows) / max(len(rows), 1)
    ea, rm, ins = cf["erase_all"], cf["remove_one"], cf["insert_one"]
    VERIFICATION["erase_all"] = dict(n=len(ea), mean_det=float(np.mean([r["n_det"] for r in ea])) if ea else float("nan"),
                                     zero_det_pct=pc(ea, lambda r: r["n_det"] == 0))
    VERIFICATION["remove_one"] = dict(n=len(rm), ghost_pct=pc(rm, lambda r: r["near_target"]), flip_pct=pc(rm, lambda r: r["pred"] == "NG"),
                                      exact_pct=pc(rm, lambda r: r["counts_equal"]),
                                      others_ok_pct=pc(rm, lambda r: r["miss"] == 0))
    VERIFICATION["insert_one"] = dict(n=len(ins), found_pct=pc(ins, lambda r: r["near_target"]), flip_pct=pc(ins, lambda r: r["pred"] == "NG"),
                                      exact_pct=pc(ins, lambda r: r["counts_equal"]))
    print(f"(2) Erase all balls ({len(ea)} images): mean detections {VERIFICATION['erase_all']['mean_det']:.2f} (a real image has 13) | "
          f"{VERIFICATION['erase_all']['zero_det_pct']:.1f}% of images give no detection at all")
    v = VERIFICATION["remove_one"]
    print(f"(3) Remove one ball ({v['n']} images): ghost box at the erased spot {v['ghost_pct']:.1f}% | verdict flips to NG {v['flip_pct']:.1f}% | "
          f"region counts exactly as expected {v['exact_pct']:.1f}% | the other balls all found {v['others_ok_pct']:.1f}%")
    v = VERIFICATION["insert_one"]
    print(f"(4) Insert one ball ({v['n']} images): new ball found {v['found_pct']:.1f}% | verdict flips to NG {v['flip_pct']:.1f}% | "
          f"region counts exactly as expected {v['exact_pct']:.1f}%   (informational: pasted balls are synthetic)")

    # (5) shortcut baseline without any localisation
    sc = global_shortcut_baseline(CV_ITEMS)
    if sc:
        VERIFICATION["shortcut"] = sc
        for k, (a, b) in sc.items():
            print(f"(5) Image-level classifier on {k}: accuracy {a:.1f}% | balanced {b:.1f}%  (majority-class baseline {baseline_result.get('majority_acc', float('nan')):.1f}%)")

    # verdict table
    V = VERIFICATION
    verdict = [
        ("1 permutation", f"real {V['permutation']['acc']:.1f}% vs shuffled {V['permutation']['null_mean']:.1f}%, p<={V['permutation']['p']:.1g}",
         "p < 0.001", V["permutation"]["p"] < 0.001),
        ("2 erase all balls", f"{V['erase_all']['mean_det']:.2f} detections / image", "<= 0.5 per image", V["erase_all"]["mean_det"] <= 0.5),
        ("3 remove one ball", f"ghost {V['remove_one']['ghost_pct']:.1f}%, exact counts {V['remove_one']['exact_pct']:.1f}%",
         "ghost <= 5% and exact >= 90%", V["remove_one"]["ghost_pct"] <= 5 and V["remove_one"]["exact_pct"] >= 90),
        ("4 insert one ball", f"found {V['insert_one']['found_pct']:.1f}%, flip {V['insert_one']['flip_pct']:.1f}%",
         "informational (>= 80% found)", V["insert_one"]["found_pct"] >= 80),
    ]
    if "shortcut" in V:
        worst = max(b for _, b in V["shortcut"].values())
        verdict.append(("5 global shortcut", f"best balanced accuracy {worst:.1f}%", "<= 75% (no shortcut)", worst <= 75))
    vdf = pd.DataFrame([dict(Check=a, Result=b, Criterion=c, Verdict="PASS" if d else "CHECK") for a, b, c, d in verdict])
    display(vdf)
    vdf.to_csv(os.path.join(FILTER_FIG_DIR, "verification_summary.csv"), index=False, encoding="utf-8-sig")
    with open(os.path.join(FILTER_FIG_DIR, "verification_summary.json"), "w", encoding="utf-8") as f:
        json.dump(V, f, ensure_ascii=False, indent=1, default=float)
    print("CHECK means: read the number, do not conclude 'guessing' from one test alone (inpainting can leave a ghost the detector fires on).")
