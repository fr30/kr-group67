from typing import List, TypeAlias


Clause: TypeAlias = List[int]


class CNFClauseSet:
    def __init__(self, formula: List[List[int]] = None):
        self.clauses = []
        if formula:
            for clause in formula:
                self.add_clause(clause)

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


def construct_cnf(self, formula: List[List[int]]) -> CNFClauseSet:
    cnf = CNFClauseSet()
    for clause in formula:
        cnf.add_clause(clause)
    return cnf
