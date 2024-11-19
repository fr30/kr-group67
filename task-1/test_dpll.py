from src.dpll_random import DPLLRandom
from src.cnf import CNFClauseSet


def test_remove_unit_clauses():
    formula = [[1, 2, 3, 4, 5], [1], [-2], [3], [4, 5]]
    cnf = CNFClauseSet(formula)
    model = {}
    dpll = DPLLRandom(cnf)
    dpll.remove_unit_clauses(cnf, model)
    # Should return [[4, 5]], model: {1: True, 2: False, 3: True}
    assert len(cnf) == 1
    assert len(cnf.clauses[0]) == 2
    assert 4 in cnf.clauses[0]
    assert 5 in cnf.clauses[0]
    assert len(model) == 3


def test_remove_unit_clauses_invalid():
    formula = [[3], [-3]]
    cnf = CNFClauseSet(formula)
    model = {}
    dpll = DPLLRandom(cnf)
    dpll.remove_unit_clauses(cnf, model)
    # Should return [[]]
    assert len(cnf) == 1
    assert len(cnf.clauses[0]) == 0


def test_remove_pure_literals():
    formula = [[1, 2, 3, 4, 5], [1], [-2], [3], [2, 4, -5]]
    cnf = CNFClauseSet(formula)
    model = {}
    dpll = DPLLRandom(cnf)
    dpll.remove_pure_literals(cnf, model)
    # Should return [[-2]], model: {1: True, 3: True, 4: True}
    assert len(cnf) == 1
    assert len(cnf.clauses[0]) == 1
    assert -2 in cnf.clauses[0]
    assert len(model) == 3


def test_remove_pure_unit():
    formula = [[1, 2, 3, 4, 5], [1], [-2], [3], [4, 5]]
    cnf = CNFClauseSet(formula)
    model = {}
    dpll = DPLLRandom(cnf)
    dpll.remove_pure_unit(cnf, model)
    # Should return [], model: {1: True, 2: False, 3: True, 4: True, 5: True}
    assert len(cnf) == 0
    assert len(model) == 5


def test_backtrack1():
    formula = [[1, 2, 3, 4, 5], [1], [-2], [3], [4, -5]]
    cnf = CNFClauseSet(formula)
    dpll = DPLLRandom(cnf)
    model = {}
    result = dpll.backtrack(cnf, model)
    assert result[0] == True
    assert len(result[1]) == 5


def test_backtrack2():
    formula = [[2, 3, 4, 5], [1], [-2], [-3], [-4, -5]]
    cnf = CNFClauseSet(formula)
    model = {}
    dpll = DPLLRandom(cnf)
    result = dpll.backtrack(cnf, model)
    assert result[0] == True
    assert len(result[1]) == 5


def test_backtrack_invalid():
    formula = [[2, 3, 5], [1], [-2], [-3], [-5]]
    cnf = CNFClauseSet(formula)
    model = {}
    dpll = DPLLRandom(cnf)
    result = dpll.backtrack(cnf, model)
    assert result[0] == False


def main():
    tests = [
        test_remove_unit_clauses,
        test_remove_unit_clauses_invalid,
        test_remove_pure_literals,
        test_remove_pure_unit,
        test_backtrack1,
        test_backtrack2,
        test_backtrack_invalid,
    ]
    for test in tests:
        test()


if __name__ == "__main__":
    main()
