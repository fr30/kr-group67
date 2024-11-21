from matplotlib import pyplot as plt
import pandas as pd
import scipy.stats as stats
import scikit_posthocs as sp
import seaborn as sns

root = '/Users/achiot/Desktop/KR/kr-group67/task-1/results/'
data_paths = ['easy-4x4.csv', 'hard-4x4.csv',
              'easy-9x9.csv', 'hard-9x9.csv', 'harder-9x9.csv']

combined_data = []
for data_path in data_paths:
    data = pd.read_csv(root + data_path)
    combined_data.append(data)

combined_data = pd.concat(combined_data, ignore_index=True)

# Kruskal-Wallis test and Dunn's post-hoc test for each metric
for metric in ['exec_time', 'branch_count']:
    print(f"\n=== Kruskal-Wallis Test for {metric} ===")

    grouped_data = [combined_data[combined_data['algorithm']
                                  == algo][metric] for algo in ['random', 'dlis', 'jsw']]

    # Kruskal-Wallis test
    stat, p = stats.kruskal(*grouped_data)
    print(f"Kruskal-Wallis Statistic: {stat}, p-value: {p}")

    if p < 0.05:
        print("Reject null hypothesis: Significant differences between groups.")
        print("Performing Dunn's post-hoc test...")

        # Dunn's post-hoc test
        dunn_results = sp.posthoc_dunn(
            combined_data, val_col=metric, group_col='algorithm', p_adjust='bonferroni')
        print("Dunn's Post-Hoc Test Results:")
        print(dunn_results)
    else:
        print("Fail to reject null hypothesis: No significant differences between groups.")

# results
# === Kruskal-Wallis Test for exec_time ===
# Kruskal-Wallis Statistic: 86.35942334032285, p-value: 1.767215416416121e-19
# Reject null hypothesis: Significant differences between groups.
# Performing Dunn's post-hoc test...
# Dunn's Post-Hoc Test Results:
#                 dlis           jsw        random
# dlis    1.000000e+00  4.472483e-01  1.459915e-12
# jsw     4.472483e-01  1.000000e+00  1.276498e-17
# random  1.459915e-12  1.276498e-17  1.000000e+00

# === Kruskal-Wallis Test for branch_count ===
# Kruskal-Wallis Statistic: 271.99286977346475, p-value: 8.659618711504033e-60
# Reject null hypothesis: Significant differences between groups.
# Performing Dunn's post-hoc test...
# Dunn's Post-Hoc Test Results:
#                 dlis           jsw        random
# dlis    1.000000e+00  1.000000e+00  8.419233e-46
# jsw     1.000000e+00  1.000000e+00  8.419233e-46
# random  8.419233e-46  8.419233e-46  1.000000e+00

    dunn_results = sp.posthoc_dunn(
        combined_data, val_col=metric, group_col='algorithm', p_adjust='bonferroni'
    )

    plt.figure(figsize=(8, 6))
    sns.heatmap(dunn_results, annot=True, fmt=".3f",
                cmap="coolwarm", cbar=True)
    plt.title(f"Dunn's Post-Hoc Test for {metric.capitalize()} (p-values)")
    plt.xlabel('Algorithm')
    plt.ylabel('Algorithm')
    output_path = f"{root}/plots/{metric}_pairwise_comp.png"
    plt.savefig(output_path, bbox_inches='tight')
    print(f"Saved {metric} boxplot to {output_path}")
    plt.close()
