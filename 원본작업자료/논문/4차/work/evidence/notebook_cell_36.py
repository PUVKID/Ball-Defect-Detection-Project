print("=" * 70)
print(f"Baseline: Original (no filter) x {len(eval_items)} images")
print("=" * 70)
baseline_result = cached_result("Original", identity_filter)
if baseline_result is None:
    if USE_CV:     # same recipe as every filter: train per fold on the unfiltered images, score the held-out fold
        baseline_result = evaluate_cv("Original", identity_filter, eval_items)
    else:
        baseline_result = evaluate_inference_only("Original", identity_filter, eval_items, yolo_model, save_example=False)
    save_result("Original", identity_filter, baseline_result)
else:
    print(f"  reusing the saved result ({os.path.basename(RESULT_CACHE_DIR)}/, REUSE_RESULTS = True)")
print("  -> " + _result_line(baseline_result) + f" | OK recall {baseline_result['ok_recall']:.2f}% | F1 {baseline_result['f1']:.2f}%")
