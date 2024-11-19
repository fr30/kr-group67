import math
from typing import List, TypeAlias
from src.utils import encode_literal

Clause: TypeAlias = List[int]


class CNFClauseSet:
    def __init__(self, formula: List[List[int]] = None):
        self.clauses = []
        if formula:
            for clause in formula:
                self.add_clause(clause)

    @classmethod
    def from_sudoku(cls, sudoku: str):
        n = int(math.sqrt(len(sudoku)))
        formula = []

        with open(f"data/sudoku-rules-{n}x{n}.txt", "r") as f:
            for line in f.readlines()[1:]:
                formula.append(list(map(int, line.strip().split(" ")[:-1])))

        for i, c in enumerate(sudoku):
            if c != ".":
                row = i // n + 1
                col = i % n + 1
                val = int(c, 17)
                formula.append([encode_literal(row, col, val, n)])

        return cls(formula)

    def __len__(self):
        return len(self.clauses)

    def __str__(self):
        return str(self.clauses)

    def add_clause(self, clause: List[int]):
        self.clauses.append(clause)

    def remove_literal(self, literal: int):
        for i in range(len(self.clauses)):
            self.clauses[i] = [
                elem for elem in self.clauses[i] if abs(elem) != abs(literal)
            ]
