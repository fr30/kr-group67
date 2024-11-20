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

## Solving Sudoku
To solve sudoku you can use scripts `example_sudoku.py` and `solve_sudoku.py`

The function `example_sudoku.py` will visualize sudoku given in the script, attempt to solve it and visualize the solution. Usage:
```sh
python example_sudoku.py
```

For `solve_sudoku.py` you need to provide path to the file containing set of sudokus. Examples of such file can be found in `data/test-4x4.out` or `data/4x4.txt`.
Example usage:
```sh
python solve_sudoku.py data/4x4.txt random
```

## Running experiments
To run experiments and gather metrics you can run `run_experiments.py`. Make sure to edit the script to suit your needs - most important thing is to provide proper test sets filenames in the variable `test_sets` - they are expected to be in the directory `./data`. Also to speedup the computation you can change the constant `ENABLE_MULTIPROCESSING` to `True`.
## Solving SAT

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