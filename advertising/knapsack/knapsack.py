import math

class Knapsack:
    def __init__(self, subcampaigns, budget, values):
        self.subcampaigns_number = subcampaigns
        self.subcampaigns_list = list(range(subcampaigns))
        self.budgets = list(range(0, budget + 10, 10))
        self.budget_value = budget
        self.combinations = [[(ind, 0) for ind in range(len(self.budgets))]]

        # It is a matrix: values[subcamp_id][budget_id] = value
        self.values = values

    def optimize(self):
        results = [[0] * len(self.budgets) for _ in range(self.subcampaigns_number)]
        # self.values = self.make_values_feasibles(self.values)
        temp_l = []

        # Perform knapsack optimization
        self.knapsack_optimization(results, 1, 1, 1, len(self.budgets), len(self.budgets), (0, 0), temp_l)

        # Compute the assignment from the knapsack optimization results
        return self.compute_assignment(self.combinations[-1][-1], self.combinations.copy())

    def make_values_feasibles(self, values):
        for row in values:
            row[0] = -math.inf
        return values

    def knapsack_optimization(self, results, ind_value_row, ind_value_col, ind_res_row, ind_res_col, ind_res_col_curr,
                              best_budget_comb, temp_l):
        # Base case: all the subcampaings have been evaluated
        if ind_res_row == self.subcampaigns_number - 1 and ind_res_col_curr == 0 and ind_res_col == 1:
            return results

        # Happens when the optimization step of the current subcampaing have been terminated
        elif ind_res_col_curr == 0 and ind_res_col == 1:
            temp_l.append((0, 0))
            self.combinations.append(list(reversed(temp_l)))
            return self.knapsack_optimization(results, ind_value_row + 1, 1, ind_res_row + 1,
                                              len(self.budgets), len(self.budgets), (0, 0), [])

        # Happens when we need to perform the optimization for the next budget in a given subcampaing
        elif ind_res_col_curr == 0:
            temp_l.append(best_budget_comb)
            return self.knapsack_optimization(results, ind_value_row, 1, ind_res_row, ind_res_col - 1, ind_res_col - 1,
                                              (0, 0), temp_l)

        # Perform the optimization for a given budget
        composed_value = self.values[ind_value_row - 1][ind_value_col - 1] + results[ind_res_row - 1][
            ind_res_col_curr - 1]

        if composed_value > results[ind_res_row][ind_res_col - 1]:
            best_budget_comb = (ind_res_col_curr - 1, ind_value_col - 1)
        results[ind_res_row][ind_res_col - 1] = max(composed_value, results[ind_res_row][ind_res_col - 1])

        return self.knapsack_optimization(results, ind_value_row, ind_value_col + 1, ind_res_row,
                                          ind_res_col, ind_res_col_curr - 1, best_budget_comb, temp_l)

    '''
        Returns a list of tuple of the following kind: (index of the sub-campaing, budget to assign)
    '''
    def compute_assignment(self, last_sub, combinations, assignment=None):

        if assignment is None:
            assignment = []

        assignment.append((len(combinations) - 1, self.budgets[last_sub[0]]))
        combinations.pop()

        if len(combinations) == 0:
            return assignment

        last_sub = combinations[-1][last_sub[1]]

        return self.compute_assignment(last_sub, combinations, assignment)
