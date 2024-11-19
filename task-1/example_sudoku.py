import sys

from src.cnf import CNFClauseSet
from src.utils import print_sudoku
from src.cdcl import CDCL
from src.dpll_random import DPLLRandom
from src.dpll_dlis import DPLLDLIS

sys.setrecursionlimit(5000)


def main():
    n = 9  # sudoku size, choose between [4, 9, 16]
    with open(f"data/test-{n}x{n}.txt", "r") as f:
        sudoku = f.readlines()[0].strip()

    for i, c in enumerate(sudoku):
        print(c, end="")
        if i % n == n - 1:
            print()

    cnf = CNFClauseSet.from_sudoku(sudoku)
    solver = DPLLRandom(cnf)
    # solver = DPLLDLIS(cnf)
    # solver = CDCL(cnf)

    result, model = solver.solve()

    if not result:
        print("UNSAT")
        return

    print()
    print_sudoku(model, n)


if __name__ == "__main__":
    main()
