import random

from src.cnf import CNFClauseSet
from src.dpll import DPLL


class DPLLRandom(DPLL):
    def __init__(self, init_cnf: CNFClauseSet):
        super(DPLLRandom, self).__init__()
        literals_set = set()
        for clause in init_cnf.clauses:
            for literal in clause:
                literals_set.add(literal)
        self.literals_left = list(literals_set)
        random.shuffle(self.literals_left)

    def choose_literal(self, cnf: CNFClauseSet) -> int:
        candidate = self.literals_left.pop()
        while candidate in self.model:
            candidate = self.literals_left.pop()
        return candidate
