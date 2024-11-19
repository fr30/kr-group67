from typing import List, Tuple, Optional


class CDCL:
    def __init__(self, cnf):
        self.cnf = cnf
        self.assignment = []
        self.learned_clauses = []
        self.decision_level = 0
        self.decision_stack = []

    def backtrack(self) -> Tuple[bool, List[int]]:
        while True:
            conflict_clause = self.unit_propagate()
            if conflict_clause:
                if self.decision_level == 0:
                    return False, []  # UNSAT
                learned_clause = self.analyze_conflict(conflict_clause)
                self.learn_clause(learned_clause)
                self.backtrack_to_level(learned_clause)
            elif self.all_variables_assigned():
                return True, self.assignment  # SAT
            else:
                self.make_decision()
        return False, []  # Default fallback

    def unit_propagate(self) -> Optional[List[int]]:
        for clause in self.cnf.clauses:
            unassigned = [lit for lit in clause if abs(
                lit) not in map(abs, self.assignment)]
            if len(unassigned) == 0:
                if not any(lit in self.assignment for lit in clause):
                    return clause  # Conflict
            elif len(unassigned) == 1:
                self.assignment.append(unassigned[0])
                self.decision_stack.append(
                    (unassigned[0], self.decision_level))
        return None  # No conflicts

    def analyze_conflict(self, conflict_clause: List[int]) -> List[int]:
        # Simplified conflict analysis (replace with UIP-based logic for real-world cases)
        decision_literals = [
            lit for lit in self.assignment if -lit in conflict_clause]
        learned_clause = list(
            set(conflict_clause + [-lit for lit in decision_literals]))
        return learned_clause

    def learn_clause(self, clause: List[int]):
        if clause not in self.cnf.clauses:
            self.cnf.add_clause(clause)
            self.learned_clauses.append(clause)

    def backtrack_to_level(self, learned_clause: List[int]):
        # Determine the highest decision level in the learned clause
        decision_levels = [self.decision_stack[i][1] for i, (lit, level) in enumerate(
            self.decision_stack) if abs(lit) in map(abs, learned_clause)]
        self.decision_level = max(decision_levels) if decision_levels else 0

        # Remove all assignments above this level
        while self.decision_stack and self.decision_stack[-1][1] > self.decision_level:
            self.assignment.pop()
            self.decision_stack.pop()

    def make_decision(self):
        unassigned_vars = set(abs(lit)
                              for clause in self.cnf.clauses for lit in clause)
        unassigned_vars -= set(abs(lit) for lit in self.assignment)
        if unassigned_vars:
            # Replace with VSIDS or other heuristic
            decision = next(iter(unassigned_vars))
            self.assignment.append(decision)
            self.decision_stack.append((decision, self.decision_level))
            self.decision_level += 1

    def all_variables_assigned(self) -> bool:
        all_vars = set(abs(lit)
                       for clause in self.cnf.clauses for lit in clause)
        return all_vars.issubset(set(abs(lit) for lit in self.assignment))
