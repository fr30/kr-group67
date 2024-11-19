import random

from src.cnf import CNFClauseSet
from src.dpll import DPLL
from src.utils import Model


class DPLLDLIS(DPLL):
    def __init__(self, init_cnf: CNFClauseSet):
        super(DPLLDLIS, self).__init__(init_cnf)
        count_dict = dict()

        for clause in init_cnf.clauses:
            for literal in clause:
                # check if literal has key in dictionary
                if literal in count_dict:
                    # if present: add +1 to value of key
                    count_dict[literal] += 1
                # if not: add literal as key to dictionary, value becomes 1
                count_dict[literal] = count_dict.get(literal, 1)

        # print(count_dict)
        self.count_dict = count_dict

    def choose_literal(self, cnf: CNFClauseSet, model: Model) -> int:
        # select literal with highest count, if multiple options, then choose the first one in the dictionary
        candidate = max(self.count_dict, key=lambda l: self.count_dict[l])
        # print(self.count_dict, "choosing: ", candidate)

        # if literal has already been assigned
        while candidate in model:
            # remove it from the dictionary
            self.count_dict.pop(candidate, None)
            # and choose the next one with the highest count
            candidate = max(self.count_dict, key=lambda l: self.count_dict[l])

        return candidate
