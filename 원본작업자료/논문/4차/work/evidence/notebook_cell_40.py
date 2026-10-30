round1_fig_paths = make_all_metric_plots(results_round1, "round1", baseline_result)
print(f"\nRound 1: {len(round1_fig_paths)} graphs saved.")
df_round1 = results_to_df(results_round1, baseline_result)
show_and_save_table(df_round1, "round1")