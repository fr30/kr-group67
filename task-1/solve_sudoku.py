import argparse

from src.cnf import CNFClauseSet
from src.dpll_random import DPLLRandom
from src.dpll_dlis import DPLLDLIS


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="Name of file to read from")
    parser.add_argument(
        "method",
        type=str,
        choices=["random", "dlis", "cdcl"],
        default="random",
        nargs="?",
        help="Method to use for DPLL",
    )
    args = parser.parse_args()

    # Choose algorithm
    method = args.method
    if method == "random":
        dpll_cls = DPLLRandom
    elif method == "dlis":
        dpll_cls = DPLLDLIS
    elif method == "cdcl":
        raise NotImplementedError
    else:
        raise ValueError("Invalid method")

    # Read the sudoku file
    filename = args.filename
    sudokus = []

    with open(filename, "r") as f:
        for line in f.readlines():
            sudokus.append(line.strip())

    results = []
    # Parse and solve sudoku
    for sudoku in sudokus:
        cnf = CNFClauseSet.from_sudoku(sudoku)
        dpll = dpll_cls(cnf)
        result = dpll.solve()
        results.append(result)

    filename_noext = filename.split(".")[0]
    with open(f"{filename_noext}.out", "w") as f:
        for result in results:
            if result[0]:
                f.write(f"{result[1]}\n")
            else:
                f.write("UNSAT\n")


if __name__ == "__main__":
    main()
