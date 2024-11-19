import random

from src.cnf import CNFClauseSet
from src.dpll import DPLL
from src.utils import Model, list_diff


class DPLLRandom(DPLL):
    def __init__(self, init_cnf: CNFClauseSet):
        super(DPLLRandom, self).__init__(init_cnf)
        literals_set = set()
        for clause in init_cnf.clauses:
            for literal in clause:
                literals_set.add(abs(literal))
        self.all_literals = list(literals_set)

    def choose_literal(self, cnf: CNFClauseSet, model: Model) -> int:
        available_literals = self.all_literals
        available_literals = list_diff(self.all_literals, model.keys())
        return random.choice(available_literals)
