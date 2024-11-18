# SAT Solver

This is a SAT solver that uses the DPLL algorithm to determine the satisfiability of a given CNF formula.

## DIMACS Format

The input file should be in DIMACS format, which is a standard format for specifying SAT problems. Each clause is represented by a line of integers, where each integer represents a literal. A positive integer represents a positive literal, and a negative integer represents a negative literal. Each clause is terminated by a `0`.

Example:

```
p cnf 3 2
1 -3 0
2 3 -1 0 
```

## Example Usage

To run the SAT solver with a CNF file:
```sh
python main.py test.cnf
```

To specify the method to use for DPLL (default is random):
```sh
python main.py test.cnf random
```

To get more information about parameters:
```sh
python main.py --help
```

##  Running tests
```sh
python test_dpll.py
```