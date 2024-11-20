import os
import pandas as pd

from src.cnf import CNFClauseSet
from src.dpll_random import DPLLRandom
from src.dpll_dlis import DPLLDLIS
from src.dpll_jsw import DPLLDLJW

DATA_PATH = "./data"
RESULTS_PATH = "./results"
NUM_RUNS = 15
ENABLE_MULTIPROCESSING = False
WARMUP_ROUNDS = 3

test_sets = [
    "easy-4x4.txt",
    "hard-4x4.txt",
    "easy-9x9.txt",
    "hard-9x9.txt",
    # "harder-9x9.txt"
]


def main():
    for filename in test_sets:
        exp_data_df = run_experiment(filename)
        filename_noext = filename.split(".")[0]
        exp_data_df.to_csv(
            os.path.join(RESULTS_PATH, f"{filename_noext}.csv"), index=False
        )


def run_experiment(filename):
    solver_names = ["random", "dlis", "jsw"]
    solvers = {"random": DPLLRandom, "dlis": DPLLDLIS, "jsw": DPLLDLJW}
    sudokus = []
    res_df = pd.DataFrame(
        columns=["algorithm", "run_id", "sudoku_id", "exec_time", "branch_count"]
    )

    with open(os.path.join(DATA_PATH, filename), "r") as f:
        for line in f.readlines():
            sudokus.append(line.strip())

    cnfs = [CNFClauseSet.from_sudoku(sudoku) for sudoku in sudokus]

    if ENABLE_MULTIPROCESSING:
        import multiprocessing

        with multiprocessing.Pool(processes=len(solver_names)) as pool:
            results = [
                pool.apply_async(
                    _run_exp,
                    args=(solvers[solver_name], solver_name, cnfs, WARMUP_ROUNDS),
                )
                for solver_name in solver_names
            ]

            for result in results:
                res_df = pd.concat([res_df, result.get()])
    else:
        for solver_name in solver_names:
            res_df = pd.concat(
                [
                    res_df,
                    _run_exp(solvers[solver_name], solver_name, cnfs, WARMUP_ROUNDS),
                ]
            )

    return res_df


def _run_exp(solver_cls, solver_name, cnfs, warmup_rounds):
    res_df = pd.DataFrame(
        columns=["algorithm", "run_id", "sudoku_id", "exec_time", "branch_count"]
    )

    for i, cnf in enumerate(cnfs):
        for _ in range(warmup_rounds):
            solver = solver_cls(cnf)
            result = solver.solve()

        for run_id in range(NUM_RUNS):
            solver = solver_cls(cnf)
            result = solver.solve()

            if not result[0]:
                raise ValueError("Unsatisfiable CNF")

            res_df = pd.concat(
                [
                    res_df,
                    pd.DataFrame(
                        {
                            "algorithm": solver_name,
                            "run_id": run_id,
                            "sudoku_id": i,
                            "exec_time": solver.exec_time,
                            "branch_count": solver.branch_count,
                        },
                        index=[0],
                    ),
                ]
            )

    return res_df


if __name__ == "__main__":
    main()
