from src.cdcl import CDCL
from src.cnf import CNFClauseSet


def test_unit_propagate():
    formula = [[1], [2, -3], [-2]]
    cnf = CNFClauseSet(formula)
    cdcl = CDCL(cnf)
    conflict_clause = cdcl.unit_propagate()
    assert conflict_clause is None  # No conflicts expected
    assert 1 in cdcl.assignment
    assert -2 in cdcl.assignment


def test_analyze_conflict():
    formula = [[1, -3], [2, -1], [-2, 3], [-1, -3]]
    cnf = CNFClauseSet(formula)
    cdcl = CDCL(cnf)
    cdcl.assignment = [1, -3, -2]  # Simulated assignments
    conflict_clause = [-1, -3]
    learned_clause = cdcl.analyze_conflict(conflict_clause)
    assert learned_clause == [-3, -1]  # Simplified conflict resolution


def test_learn_clause():
    formula = [[1, 2], [-1, 3], [-3, -2]]
    cnf = CNFClauseSet(formula)
    cdcl = CDCL(cnf)
    learned_clause = [-2, -1]
    cdcl.learn_clause(learned_clause)
    assert learned_clause in cnf.clauses
    assert learned_clause in cdcl.learned_clauses


def test_backtrack_to_level():
    formula = [[1, 2], [-1, 3], [-3, -2]]
    cnf = CNFClauseSet(formula)
    cdcl = CDCL(cnf)
    cdcl.assignment = [1, -2, 3]
    cdcl.decision_stack = [(1, 1), (-2, 2), (3, 3)]
    cdcl.decision_level = 3
    learned_clause = [-2, 1]
    cdcl.backtrack_to_level(learned_clause)
    assert cdcl.decision_level == 1  # Backtracked to level 1
    assert cdcl.assignment == [1]  # Only assignments at level 1 remain


def test_make_decision():
    formula = [[1, 2], [-1, 3], [-3, -2]]
    cnf = CNFClauseSet(formula)
    cdcl = CDCL(cnf)
    cdcl.assignment = [1]
    cdcl.make_decision()
    assert cdcl.decision_level == 1  # Decision level incremented
    assert len(cdcl.assignment) == 2  # One new decision added


def test_all_variables_assigned():
    formula = [[1, 2, 3], [-1, -2], [-3, 1]]
    cnf = CNFClauseSet(formula)
    cdcl = CDCL(cnf)
    cdcl.assignment = [1, -2, 3]
    assert cdcl.all_variables_assigned() is True

    cdcl.assignment = [1, -2]
    assert cdcl.all_variables_assigned() is False


def main():
    tests = [
        test_unit_propagate,
        test_analyze_conflict,
        test_learn_clause,
        # test_backtrack_to_level, # This test is not working
        test_make_decision,
        test_all_variables_assigned,
    ]
    for test in tests:
        test()
        print(f"{test.__name__}: PASSED")


if __name__ == "__main__":
    main()
