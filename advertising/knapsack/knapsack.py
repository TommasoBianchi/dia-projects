import math

import numpy as np


class Knapsack:
    def __init__(self, subcampaigns, budget, values):
        self.subcampaigns_number = subcampaigns
        self.subcampaigns_list = list(range(subcampaigns))
        self.budgets = list(range(0,budget + 10, 10))
        self.budget_value = budget

        # It is a matrix: values[subcamp_id][budget_id] = value
        self.values = values

    def optimize(self):
        results = [[0] * len(self.budgets) for _ in range(self.subcampaigns_number + 1)]
        self.values = self.make_values_feasibles(self.values)
        results = self.knapsack_optimization(results, 1, 1, 1, len(self.budgets), len(self.budgets))

        return self.compute_assignment(results[1:])

    def make_values_feasibles(self, values):
        for row in values:
            row[0] = -math.inf
        return values

    def knapsack_optimization(self, results, ind_value_row, ind_value_col, ind_res_row, ind_res_col, ind_res_col_curr):
        # Base case: all the subcampaings have been evaluated
        if ind_res_row == self.subcampaigns_number and ind_res_col_curr == 0 and ind_res_col == 1:
            return results

        # Happens when the optimization step of the current subcampaing have been terminated
        elif ind_res_col_curr == 0 and ind_res_col == 1:
            return self.knapsack_optimization(results, ind_value_row + 1, 1, ind_res_row + 1,
                                              len(self.budgets), len(self.budgets))

        # Happens when we need to perform the optimization for the next budget in a given subcampaing
        elif ind_res_col_curr == 0:
            return self.knapsack_optimization(results, ind_value_row, 1, ind_res_row, ind_res_col - 1, ind_res_col - 1)

        # Perform the optimization for a given budget
        composed_value = self.values[ind_value_row - 1][ind_value_col - 1] + results[ind_res_row - 1][ind_res_col_curr - 1]

        results[ind_res_row][ind_res_col - 1] = max(composed_value, results[ind_res_row][ind_res_col - 1])

        return self.knapsack_optimization(results, ind_value_row, ind_value_col + 1, ind_res_row,
                                   ind_res_col, ind_res_col_curr - 1)


    def compute_assignment(self, results):

        budget_values = self.budgets
        assignments = []
        max_value_index = int(np.argmax(np.asarray(np.copy(results[-1]))))
        assignments.append((self.subcampaigns_list[-1], budget_values[max_value_index]))
        remaining_budget = self.budget_value - budget_values[max_value_index]

        results = results[:-1]
        results.reverse()

        current_subcampaign = len(self.subcampaigns_list) - 2
        for _ in results:
            if remaining_budget == 0:
                assignments = list(reversed(assignments))
                return assignments

            curr_assignment = len(self.budgets) - assignments[-1][0] - 1
            budget_assigned = budget_values[curr_assignment]
            remaining_budget -= budget_assigned
            assignments.append((current_subcampaign, budget_assigned))
            current_subcampaign -= 1

        return list(reversed(assignments))

