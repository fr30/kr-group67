from matplotlib import pyplot as plt
import pandas as pd
import scipy.stats as stats
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

    all_results = []

    for data_path in data_paths:
        data = pd.read_csv(root + data_path)
        file_results = run_stat_tests(data, data_path)
        all_results.extend(file_results)

    file_results = run_stat_tests(combined_data, 'combined')
    all_results.extend(file_results)

    plot_boxplots(
        combined_data, '/Users/achiot/Desktop/KR/kr-group67/task-1/results/plots/')

    # results_df = pd.DataFrame(all_results)

    # output_path = root + 'stat_test_results.csv'
    # results_df.to_csv(output_path, index=False)
    # print(f"Results saved to {output_path}")


def run_stat_tests(data, file_name):
    """
    Checks for normality of differences and,
    depending on the result
    performs paired t-test or wilcoxon signed-rank test
    """

    if data['branch_count'].dtype != int:
        data['branch_count'] = pd.to_numeric(
            data['branch_count'], errors='coerce').fillna(0).astype(int)

    perfromance_random = data[data['algorithm'] == 'random']
    performance_dlis = data[data['algorithm'] == 'dlis']
    performance_jsw = data[data['algorithm'] == 'jsw']

    perfromance_random = perfromance_random.sort_values(
        'sudoku_id').reset_index(drop=True)
    performance_dlis = performance_dlis.sort_values(
        'sudoku_id').reset_index(drop=True)
    performance_jsw = performance_jsw.sort_values(
        'sudoku_id').reset_index(drop=True)

    algorithms = [('Random', perfromance_random),
                  ('DLIS', performance_dlis), ('JSW', performance_jsw)]
    metrics = ['exec_time', 'branch_count']

    results = []

    for i, (name1, algo1) in enumerate(algorithms):
        for j, (name2, algo2) in enumerate(algorithms):
            if i < j:
                for metric in metrics:
                    differences = algo1[metric] - algo2[metric]

                    # check if all differences are constant
                    # for some experiments (e.g. easy-4x4) the difference in branching count is constant (always 0 i think)
                    # commented it out because we can just say it is not significant
                    # if differences.nunique() == 1:
                    #     results.append({
                    #         'Dataset': file_name,
                    #         'Algorithm 1': name1,
                    #         'Algorithm 2': name2,
                    #         'Metric': metric,
                    #         'Test': 'None',
                    #         'p-value': None,
                    #         'Result': f"All differences constant: {differences.iloc[0]}"
                    #     })
                    #     continue

                    # check for normality
                    stat, p = stats.shapiro(differences)
                    if p > 0.05:
                        # paired t-test
                        t_stat, t_p = stats.ttest_rel(
                            algo1[metric], algo2[metric])
                        results.append({
                            'Dataset': file_name,
                            'Algorithm 1': name1,
                            'Algorithm 2': name2,
                            'Metric': metric,
                            'Test': 'Paired T-Test',
                            'p-value': t_p,
                            'Result': 'Significant' if t_p < 0.05 else 'Not Significant'
                        })
                    else:
                        # wilcoxon signed-rank test if non-normality
                        w_stat, w_p = stats.wilcoxon(
                            algo1[metric], algo2[metric])
                        results.append({
                            'Dataset': file_name,
                            'Algorithm 1': name1,
                            'Algorithm 2': name2,
                            'Metric': metric,
                            'Test': 'Wilcoxon Signed-Rank Test',
                            'p-value': w_p,
                            'Result': 'Significant' if w_p < 0.05 else 'Not Significant'
                        })

    return results


def plot_boxplots(data, output_dir):
    """
    Plot boxplots for each metric without outliers.
    Grouped by algorithms.
    """
    metrics = ['exec_time', 'branch_count']

    for metric in metrics:
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='algorithm', y=metric, data=data,
                    showfliers=False)  # Hides outliers
        plt.title(f'Boxplot of {metric} (Without Outliers)')
        plt.ylabel(metric.capitalize())
        plt.xlabel('Algorithm')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Save the plot
        output_path = f"{output_dir}{metric}_boxplot_no_outliers.png"
        plt.savefig(output_path, bbox_inches='tight')
        print(f"Saved {metric} boxplot (no outliers) to {output_path}")
        plt.close()


if __name__ == "__main__":
    main()
