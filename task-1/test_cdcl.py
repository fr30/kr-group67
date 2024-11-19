from src.cdcl import CDCL
from src.cnf import CNFClauseSet


def test_unit_propagate():
    """
    Tests unit propagation assigns values for unit clauses
    and detects no conflicts for a valid formula.
    """
    formula = [[1], [2, -3], [-2]]
    cnf = CNFClauseSet(formula)
    cdcl = CDCL(cnf)

    # unit propagation
    conflict_clause = cdcl.unit_propagate()

    assert conflict_clause is None  # no conflicts expected
    assert 1 in cdcl.assignment  # literal 1 should be propagated
    assert -2 in cdcl.assignment  # literal -2 should be propagated


def test_analyze_conflict():
    """
    Tests conflict analysis generates a correct learned clause.
    """
    formula = [[1, -3], [2, -1], [-2, 3], [-1, -3]]
    cnf = CNFClauseSet(formula)
    cdcl = CDCL(cnf)

    # simulate assignments leading to a conflict
    cdcl.assignment = [1, -3, -2]
    conflict_clause = [-1, -3]

    # analyze the conflict
    learned_clause = cdcl.analyze_conflict(conflict_clause)

    assert learned_clause == [-3, -1]  # simplified conflict resolution


def test_learn_clause():
    """
    Test learned clauses are added to the CNF and tracked.
    """
    formula = [[1, 2], [-1, 3], [-3, -2]]
    cnf = CNFClauseSet(formula)
    cdcl = CDCL(cnf)

    # Learn a new clause
    learned_clause = [-2, -1]
    cdcl.learn_clause(learned_clause)

    assert learned_clause in cnf.clauses  # clause added to CNF
    # Clause tracked in learned_clauses
    assert learned_clause in cdcl.learned_clauses


def test_backtrack_to_level():
    """
    Tests backtracking removes assignments above the target decision level.
    """
    formula = [[1, 2], [-1, 3], [-3, -2]]
    cnf = CNFClauseSet(formula)
    cdcl = CDCL(cnf)

    # simulate decisions and assignments
    cdcl.assignment = [1, -2, 3]
    cdcl.decision_stack = [(1, 1), (-2, 2), (3, 3)]
    cdcl.decision_level = 3

    # perform backtracking
    learned_clause = [-2, 1]
    cdcl.backtrack_to_level(learned_clause)

    assert cdcl.decision_level == 2  # backtracked to level 2
    assert cdcl.assignment == [1, -2]  # only assignments up to level 2 remain


def test_make_decision():
    """
    Tests the decision-making process selects an unassigned variable
    and increments the decision level.
    """
    formula = [[1, 2], [-1, 3], [-3, -2]]
    cnf = CNFClauseSet(formula)
    cdcl = CDCL(cnf)

    # simulate initial assignment
    cdcl.assignment = [1]

    # make a decision
    cdcl.make_decision()

    assert cdcl.decision_level == 1  # decision level incremented
    assert len(cdcl.assignment) == 2  # one new decision added


def test_all_variables_assigned():
    """
    Tests detection of whether all variables are assigned.
    """
    formula = [[1, 2, 3], [-1, -2], [-3, 1]]
    cnf = CNFClauseSet(formula)
    cdcl = CDCL(cnf)

    # full assignment
    cdcl.assignment = [1, -2, 3]
    assert cdcl.all_variables_assigned() is True  # all variables assigned

    # partial assignment
    cdcl.assignment = [1, -2]
    assert cdcl.all_variables_assigned() is False  # some variables remain unassigned


def main():
    tests = [
        test_unit_propagate,
        test_analyze_conflict,
        test_learn_clause,
        test_backtrack_to_level,
        test_make_decision,
        test_all_variables_assigned,
    ]
    for test in tests:
        test()
        print(f"{test.__name__}: PASSED")


if __name__ == "__main__":
    main()
