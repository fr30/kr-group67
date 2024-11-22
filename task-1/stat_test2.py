from matplotlib import pyplot as plt
import pandas as pd
import scipy.stats as stats
import scikit_posthocs as sp
import seaborn as sns


def main():
    root = '/Users/achiot/Desktop/KR/kr-group67/task-1/results/'
    data_paths = ['easy-4x4.csv', 'hard-4x4.csv',
                  'easy-9x9.csv', 'hard-9x9.csv', 'harder-9x9.csv']

    combined_data = []
    for data_path in data_paths:
        data = pd.read_csv(root + data_path)
        combined_data.append(data)

    combined_data = pd.concat(combined_data, ignore_index=True)

    all_results_KW = []
    all_results_Dunn = []

    for data_path in data_paths:
        data = pd.read_csv(root + data_path)
        file_results_KW, file_results_Dunn = run_stat_tests(data, data_path)
        all_results_KW.extend(file_results_KW)
        all_results_Dunn.extend(file_results_Dunn)

    combined_results_KW, combined_results_Dunn = run_stat_tests(
        combined_data, 'combined')
    all_results_KW.extend(combined_results_KW)
    all_results_Dunn.extend(combined_results_Dunn)

    results_df_KW = pd.DataFrame(all_results_KW)
    output_path = root + 'stat_test_results_KW.csv'
    results_df_KW.to_csv(output_path, index=False)

    results_df_Dunn = pd.DataFrame(all_results_Dunn)
    output_path = root + 'stat_test_results_Dunn.csv'
    results_df_Dunn.to_csv(output_path, index=False)


def run_stat_tests(data, file_name):
    """
    Perform Kruskal-Wallis and Dunn's post-hoc tests for execution time and branch count.
    """
    results_KW = []
    results_Dunn = []
    for metric in ['exec_time', 'branch_count']:
        grouped_data = [data[data['algorithm'] == algo][metric]
                        for algo in ['random', 'dlis', 'jsw']]

        # Check if all groups have variability
        if any(group.nunique() == 1 for group in grouped_data):
            print(
                f"Skipping Kruskal-Wallis for {metric} in {file_name}: One or more groups have identical values.")
            results_KW.append({
                'Dataset': file_name,
                'Metric': metric,
                'Test': 'Kruskal-Wallis',
                'Statistic': None,
                'p-value': None,
                'Result': 'All numbers identical, test skipped'
            })
            continue

        # Kruskal-Wallis test
        stat, p = stats.kruskal(*grouped_data)

        # Record Kruskal-Wallis results
        results_KW.append({
            'Dataset': file_name,
            'Metric': metric,
            'Test': 'Kruskal-Wallis',
            'Statistic': stat,
            'p-value': p,
            'Result': 'Significant' if p < 0.05 else 'Not Significant'
        })

        # If significant, perform Dunn's post-hoc test
        if p < 0.05:
            dunn_results = sp.posthoc_dunn(
                data, val_col=metric, group_col='algorithm', p_adjust='bonferroni'
            )

            # Record Dunn's post-hoc test results
            for algo1 in dunn_results.index:
                for algo2 in dunn_results.columns:
                    if algo1 != algo2:
                        results_Dunn.append({
                            'Dataset': file_name,
                            'Metric': metric,
                            'Test': "Dunn's Post-Hoc",
                            'Algorithm 1': algo1,
                            'Algorithm 2': algo2,
                            'p-value': dunn_results.loc[algo1, algo2],
                            'Result': 'Significant' if dunn_results.loc[algo1, algo2] < 0.05 else 'Not Significant'
                        })
        else:
            results_Dunn.append({
                'Dataset': file_name,
                'Metric': metric,
                'Test': "Dunn's Post-Hoc",
                'Algorithm 1': None,
                'Algorithm 2': None,
                'p-value': None,
                'Result': 'Kruskal-Wallis not significant, test skipped'
            })
    return results_KW, results_Dunn


if __name__ == "__main__":
    main()
