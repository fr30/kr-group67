import random

from src.cnf import CNFClauseSet
from src.dpll import DPLL
from src.utils import Model, list_diff


class DPLLDLIS(DPLL):
    def __init__(self, init_cnf: CNFClauseSet):
        super(DPLLDLIS, self).__init__(init_cnf)
        literals_set = set()
        for clause in init_cnf.clauses:
            for literal in clause:
                literals_set.add(abs(literal))
        self.all_literals = list(literals_set)

    def choose_literal(self, cnf: CNFClauseSet, model: Model) -> int:
        """
        DLIS heuristic, where we count occurrences of each unassigned literal.
        """
        literal_counts = dict()
        # only checking literals that have not been assigned/satisfied
        available_literals = list_diff(self.all_literals, model.keys())

        # calculate DLIS scores
        for clause in cnf.clauses:
            # count occurrence for each unassigned literal in the clause
            for literal in clause:
                # if literal has not been assigned
                if literal in available_literals:
                    # if literal does not exist yet in dictionary, assign count 0 then +1, otherwise just +1
                    literal_counts[literal] = literal_counts.get(literal, 0) + 1
        print(literal_counts)

        # select literal with the highest count
        candidate = max(literal_counts, key=literal_counts.get) 
        return candidate
