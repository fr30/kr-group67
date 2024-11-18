import itertools

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Tuple, TypeAlias, Dict
from src.cnf import CNFClauseSet


Model: TypeAlias = Dict[int, bool]


class DPLL(ABC):
    def __init__(self):
        self.model = {}

    # Returns a model if satisfiable, None otherwise
    def backtrack(self, cnf: CNFClauseSet) -> Tuple[bool, Model]:
        self.remove_pure_unit(cnf)

        if len(cnf) == 0:
            return True, self.model

        if any(len(clause) == 0 for clause in cnf.clauses):
            return False, None

        literal = self.choose_literal(cnf)
        cnf_left = deepcopy(cnf)
        cnf_left.add_clause([literal])
        left = self.backtrack(cnf_left)
        if left[0]:
            return True, left[1]

        cnf_right = deepcopy(cnf)
        cnf_right.add_clause([-literal])
        right = self.backtrack(cnf_right)
        if right[0]:
            return True, right[1]

        return False, None

    # Remove pure literals and unit clauses
    def remove_pure_unit(self, cnf: CNFClauseSet) -> None:
        unit_clause, pure_literal = True, True
        while unit_clause or pure_literal:
            unit_clause = self.remove_unit_clauses(cnf)
            pure_literal = self.remove_pure_literals(cnf)

    def remove_unit_clauses(self, cnf: CNFClauseSet) -> bool:
        found = False
        toremove = []
        for clause in cnf.clauses:
            if len(clause) == 1:
                literal = clause[0]

                if self.set_model_literal(literal, literal > 0):
                    toremove.append(clause)
                    found = True

        for clause in toremove:
            cnf.clauses.remove(clause)

        self.simplify_cnf(cnf)
        return found

    def remove_pure_literals(self, cnf: CNFClauseSet) -> bool:
        found = False
        literals = set()
        for clause in cnf.clauses:
            for literal in clause:
                literals.add(literal)

        for literal in literals:
            if -literal not in literals:
                if self.set_model_literal(literal, literal > 0):
                    found = True

        self.simplify_cnf(cnf)
        return found

    def set_model_literal(self, literal: int, value: bool) -> None:
        if abs(literal) in self.model:
            return self.model[abs(literal)] == value
        self.model[abs(literal)] = value

    def simplify_cnf(self, cnf: CNFClauseSet) -> None:
        self.remove_tautologies(cnf)
        self.fix_clauses(cnf)

    def remove_tautologies(self, cnf: CNFClauseSet) -> None:
        toremove = []
        for clause in cnf.clauses:
            for literal in clause:
                if -literal in clause:
                    toremove.append(clause)

        toremove.sort()
        toremove = list(k for k, _ in itertools.groupby(toremove))
        for clause in toremove:
            cnf.clauses.remove(clause)

    def fix_clauses(self, cnf: CNFClauseSet) -> None:
        # print("=====Fixing clauses=====")
        # print(cnf)
        # print(self.model)
        toremove = []
        for clause in cnf.clauses:
            for literal in clause:
                # If undetermined, skip
                if abs(literal) not in self.model:
                    continue
                # print(literal, self.istrue_literal(literal), self.model)
                # Remove clause if literal is true
                if self.istrue_literal(literal):
                    toremove.append(clause)
                    break
                # Shorten clause if literal is false
                else:
                    # print("Removing literal", literal, clause)
                    clause.remove(literal)

        toremove.sort()
        toremove = list(k for k, _ in itertools.groupby(toremove))
        for clause in toremove:
            cnf.clauses.remove(clause)
        # print(toremove)
        # print(cnf)
        # print("====================")

    def istrue_literal(self, literal: int) -> bool:
        return not ((literal > 0) ^ (self.model[abs(literal)]))

    @abstractmethod
    def choose_literal(self, cnf: CNFClauseSet) -> int:
        pass
