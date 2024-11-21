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

    plt.figure(figsize=(10, 6))
    sns.boxplot(x='algorithm', y=metric, data=combined_data)
    plt.title(f'Boxplot of {metric} by Algorithm')
    plt.ylabel(metric.capitalize())
    plt.xlabel('Algorithm')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    output_path = f"{root}/plots/{metric}_boxplot_2.png"
    plt.savefig(output_path, bbox_inches='tight')
    print(f"Saved {metric} boxplot to {output_path}")
    plt.close()
