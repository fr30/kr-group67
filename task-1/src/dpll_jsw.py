from src.cnf import CNFClauseSet
from src.dpll import DPLL
from src.utils import Model


class DPLLDLJW(DPLL):
    def __init__(self, init_cnf: CNFClauseSet):
        super(DPLLDLJW, self).__init__(init_cnf)
        jw_dict = dict()

        for clause in init_cnf.clauses:
            for literal in clause:
                var = abs(literal)
                weight = 2 ** -len(clause)
                jw_dict[var] = jw_dict.get(var, 0) + weight

        self.jw_dict = jw_dict

    def choose_literal(self, cnf: CNFClauseSet, model: Model) -> int:
        """
        Chooses the best literal based on the Jeroslow-Wang heuristic.
        """
        # calculate the weighted sum for each variable
        available_vars = {var: weight for var, weight in self.jw_dict.items(
        ) if var not in model and -var not in model}

        if not available_vars:
            raise ValueError("No available literals to choose from.")

        # select the variable with the highest weighted sum
        best_var = max(available_vars, key=available_vars.get)
        return best_var if best_var not in model else -best_var
