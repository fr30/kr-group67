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

    # Read formula in DIMACS format
    filename = args.filename
    formula = []

    with open(filename, "r") as f:
        for line in f.readlines()[1:]:
            formula.append(list(map(int, line.strip().split(" ")[:-1])))

    # Solve formula
    cnf = CNFClauseSet(formula)
    dpll = dpll_cls(cnf)
    result = dpll.backtrack(cnf)

    if result[0]:
        print("SAT")
        print(result[1])
    else:
        print("UNSAT")
        print({})


if __name__ == "__main__":
    main()
