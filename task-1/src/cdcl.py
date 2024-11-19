from typing import List, Tuple, Optional


class CDCL:
    def __init__(self, cnf):
        """
        Initializes the CDCL solver with a CNF formula.
        """
        self.cnf = cnf
        self.assignment = []
        self.learned_clauses = []
        self.decision_level = 0
        self.decision_stack = []

    def backtrack(self) -> Tuple[bool, List[int]]:
        """
        Main CDCL solving loop.
        Returns a tuple: (SAT/UNSAT, assignments).
        """
        while True:
            conflict_clause = self.unit_propagate()
            if conflict_clause:
                if self.decision_level == 0:
                    return False, []  # UNSAT: No backtracking possible
                learned_clause = self.analyze_conflict(conflict_clause)
                self.learn_clause(learned_clause)
                self.backtrack_to_level(learned_clause)
            elif self.all_variables_assigned():
                return True, self.assignment  # SAT: All variables assigned
            else:
                self.make_decision()

    def unit_propagate(self) -> Optional[List[int]]:
        """
        Performs unit propagation. Assign values for unit clauses.
        Returns a conflicting clause if a conflict is detected.
        """
        for clause in self.cnf.clauses:
            unassigned = [
                lit for lit in clause if abs(lit) not in map(abs, self.assignment)
            ]
            if len(unassigned) == 0:
                # clause is unsatisfied under current assignments
                if not any(lit in self.assignment for lit in clause):
                    return clause  # Conflict detected
            elif len(unassigned) == 1:
                # found a unit clause; propagate its literal
                self.assignment.append(unassigned[0])
                self.decision_stack.append(
                    (unassigned[0], self.decision_level))
        return None  # no conflicts detected

    def analyze_conflict(self, conflict_clause: List[int]) -> List[int]:
        """
        Analyzes a conflict and derive a learned clause.
        """
        decision_literals = [
            lit for lit in self.assignment if -lit in conflict_clause
        ]
        # simplified conflict resolution logic (expand for UIP if needed)
        learned_clause = list(
            set(conflict_clause + [-lit for lit in decision_literals])
        )
        return learned_clause

    def learn_clause(self, clause: List[int]):
        """
        Adds a learned clause to the CNF formula.
        """
        if clause not in self.cnf.clauses:
            self.cnf.add_clause(clause)
            self.learned_clauses.append(clause)

    def backtrack_to_level(self, learned_clause: List[int]):
        """
        Backtracks to the highest decision level in the learned clause.
        """
        levels = [
            level for lit, level in self.decision_stack
            if abs(lit) in map(abs, learned_clause)
        ]
        target_level = max(levels) if levels else 0
        self.decision_level = target_level

        # remove all assignments above the target decision level
        while self.decision_stack and self.decision_stack[-1][1] > self.decision_level:
            lit, level = self.decision_stack.pop()
            self.assignment.remove(lit)

    def make_decision(self):
        """
        Chooses an unassigned variable and assign it a value.
        """
        unassigned_vars = {
            abs(lit) for clause in self.cnf.clauses for lit in clause
        }
        unassigned_vars -= {abs(lit) for lit in self.assignment}
        if unassigned_vars:
            # default decision-making strategy (expand with heuristics if needed)
            decision = next(iter(unassigned_vars))
            self.assignment.append(decision)
            self.decision_stack.append((decision, self.decision_level))
            self.decision_level += 1

    def all_variables_assigned(self) -> bool:
        """
        Checks if all variables in the CNF formula are assigned.
        """
        all_vars = {
            abs(lit) for clause in self.cnf.clauses for lit in clause
        }
        return all_vars.issubset({abs(lit) for lit in self.assignment})
