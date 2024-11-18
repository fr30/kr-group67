from copy import deepcopy
from typing import List, Map, TypeAlias, Tuple
from abc import ABC, abstractmethod

Clause: TypeAlias = List[int]
Model: TypeAlias = Map[int, bool]


class CNFClauseSet:
    clauses: List[Clause] = []

    def add_clause(self, clause: List[int]):
        self.clauses.append(clause)

    def remove_literal(self, literal: int):
        for i in range(len(self.clauses)):
            self.clauses[i] = [
                elem for elem in self.clauses[i] if abs(elem) != abs(literal)
            ]

    def __len__(self):
        return len(self.clauses)


class DPLL(ABC):
    model: Model = {}

    def construct_cnf(self, formula: List[List[int]]) -> CNFClauseSet:
        cnf = CNFClauseSet()
        for clause in formula:
            cnf.add_clause(clause)
        return cnf

    # def solve(self, formula: List[List[int]]) -> Model:
    #     cnf = self.construct_cnf(formula)

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
                self.set_model_literal(literal, literal > 0)
                toremove.append(clause)
                found = True

        for clause in toremove:
            cnf.clauses.remove(clause)

        self.simplify_cnf(cnf)
        return found

    # Following function mutates cnf
    def remove_pure_literals(self, cnf: CNFClauseSet) -> bool:
        found = False
        literals = set()
        for clause in cnf.clauses:
            for literal in clause:
                literals.add(literal)

        for literal in literals:
            if -literal not in literals:
                self.set_model_literal(literal, literal > 0)
                found = True

        self.simplify_cnf(cnf)
        return found

    def set_model_literal(self, literal: int, value: bool) -> None:
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

        for clause in toremove:
            cnf.clauses.remove(clause)

    def fix_clauses(self, cnf: CNFClauseSet) -> None:
        toremove = []
        for clause in cnf.clauses:
            for literal in clause:
                # Remove clause if literal is true
                if self.istrue_literal(literal):
                    toremove.append(clause)
                # Shorten clause if literal is false
                else:
                    clause.remove(literal)

        for clause in toremove:
            cnf.clauses.remove(clause)

    def istrue_clause(self, clause: Clause) -> bool:
        return any(self.istrue_literal(literal) for literal in clause)

    def istrue_literal(self, literal: int) -> bool:
        return literal < 0 != self.model[abs(literal)]

    @abstractmethod
    def choose_literal(self, cnf: CNFClauseSet) -> int:
        pass


def main():
    print("Hello World!")


if __name__ == "__main__":
    main()
