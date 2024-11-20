import sys
import numpy as np
import pandas as pd
import random

from src.cnf import CNFClauseSet
from src.utils import print_sudoku

sys.setrecursionlimit(5000)

def main():
    # MAKE DATASETS

    #   4x4
    easy_4x4, hard_4x4 = [], []

    with open(f"data/4x4.txt", "r") as f:
        all_sudokus = f.read().splitlines()
    
    for sudoku in all_sudokus:
        givens = sum(c.isdigit() for c in sudoku)
        if givens == 6:
            easy_4x4.append(sudoku)
        else: # givens == 4
            hard_4x4.append(sudoku)

    with open("data/easy-4x4.txt", "w") as file:
        file.write("\n".join(easy_4x4))
    with open("data/hard-4x4.txt", "w") as file:
        file.write("\n".join(hard_4x4))


    #   9x9
    easy_9x9, hard_9x9, harder_9x9 = [], [], []

    for d in ["top95.sdk.txt", "top870.sdk.txt", "top91.sdk.txt", "top100.sdk.txt", "top2365.sdk.txt", "1000-sudokus.txt", "damnhard.sdk.txt", "sudokus_1mil.txt"]:
        with open(f"data/{d}", "r") as f:
            all_sudokus = f.read().splitlines()
            if len(all_sudokus) > 2500:
                # randomly select 1000 lines from kaggle dataset
                all_sudokus = random.choices(all_sudokus, k=2500)

        for sudoku in all_sudokus:
            givens = sum(c.isdigit() for c in sudoku)
            if givens < 21: # small set
                harder_9x9.append(sudoku)
            elif 21 <= givens <= 25: 
                hard_9x9.append(sudoku)
            elif givens > 30: # randomly sampled from sudokus_1mil.txt
                easy_9x9.append(sudoku)

        with open("data/easy-9x9.txt", "w") as file:
            file.write("\n".join(easy_9x9))
        with open("data/hard-9x9.txt", "w") as file:
            file.write("\n".join(hard_9x9))
        with open("data/harder-9x9.txt", "w") as file:
            file.write("\n".join(harder_9x9))


if __name__ == "__main__":
    main()
