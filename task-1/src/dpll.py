import itertools

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Tuple
from src.cnf import CNFClauseSet
from src.utils import Model


class DPLL(ABC):
    def __init__(self, init_cnf: CNFClauseSet):
        self.cnf = init_cnf

    def solve(self) -> Tuple[bool, Model]:
        cnf = deepcopy(self.cnf)
        return self.backtrack(cnf, {})

    # Returns a model if satisfiable, None otherwise
    def backtrack(self, cnf: CNFClauseSet, model: Model) -> Tuple[bool, Model]:
        self.remove_pure_unit(cnf, model)

        if len(cnf) == 0:
            return True, model

        if any(len(clause) == 0 for clause in cnf.clauses):
            return False, None

        literal = self.choose_literal(cnf, model)
        cnf_left, model_left = deepcopy(cnf), deepcopy(model)
        cnf_left.add_clause([literal])
        left = self.backtrack(cnf_left, model_left)
        if left[0]:
            return True, left[1]

        cnf_right, model_right = deepcopy(cnf), deepcopy(model)
        cnf_right.add_clause([-literal])
        right = self.backtrack(cnf_right, model_right)
        if right[0]:
            return True, right[1]

        return False, None

    # Remove pure literals and unit clauses
    def remove_pure_unit(self, cnf: CNFClauseSet, model: Model) -> None:
        unit_clause, pure_literal = True, True
        while unit_clause or pure_literal:
            unit_clause = self.remove_unit_clauses(cnf, model)
            pure_literal = self.remove_pure_literals(cnf, model)

    def remove_unit_clauses(self, cnf: CNFClauseSet, model: Model) -> bool:
        found = False
        toremove = []
        for clause in cnf.clauses:
            if len(clause) == 1:
                literal = clause[0]

                if self.set_model_literal(model, literal, literal > 0):
                    toremove.append(clause)
                    found = True

        for clause in toremove:
            cnf.clauses.remove(clause)

        self.simplify_cnf(cnf, model)
        return found

    def remove_pure_literals(self, cnf: CNFClauseSet, model: Model) -> bool:
        found = False
        literals = set()
        for clause in cnf.clauses:
            for literal in clause:
                literals.add(literal)

        for literal in literals:
            if -literal not in literals:
                if self.set_model_literal(model, literal, literal > 0):
                    found = True

        self.simplify_cnf(cnf, model)
        return found

    def set_model_literal(self, model: Model, literal: int, value: bool) -> bool:
        if abs(literal) in model:
            return model[abs(literal)] == value
        model[abs(literal)] = value
        return True  # Or false? run tests

    def simplify_cnf(self, cnf: CNFClauseSet, model: Model) -> None:
        self.remove_tautologies(cnf)
        self.fix_clauses(cnf, model)

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

    def fix_clauses(self, cnf: CNFClauseSet, model: Model) -> None:
        toremove = []
        for clause in cnf.clauses:
            for literal in clause:
                # If undetermined, skip
                if abs(literal) not in model:
                    continue
                # Remove clause if literal is true
                if self.istrue_literal(literal, model):
                    toremove.append(clause)
                    break
                # Shorten clause if literal is false
                else:
                    clause.remove(literal)

        toremove.sort()
        toremove = list(k for k, _ in itertools.groupby(toremove))
        for clause in toremove:
            cnf.clauses.remove(clause)

    def istrue_literal(self, literal: int, model: Model) -> bool:
        return not ((literal > 0) ^ (model[abs(literal)]))

    @abstractmethod
    def choose_literal(self, cnf: CNFClauseSet) -> int:
        pass
