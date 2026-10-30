round2_fig_paths = make_all_metric_plots(results_round2, "round2", baseline_result)
print(f"\nRound 2: {len(round2_fig_paths)} graphs saved.")
df_round2 = results_to_df(results_round2, baseline_result)
show_and_save_table(df_round2, "round2")