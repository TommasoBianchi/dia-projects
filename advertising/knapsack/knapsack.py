class Knapsack:
    def __init__(self, subcampaigns, budgets, values):
        self.subcampaigns = subcampaigns
        self.budgets = budgets

        # It is a matrix: values[subcamp_id][budget_id] = value
        self.values = values

    def optimize(self):
        results = [[0]*self.budgets for _ in range(self.subcampaigns + 1)]
        return self.knapsack_optimization(results, 1, 1, 1, self.budgets, self.budgets)

    def knapsack_optimization(self, results, ind_value_row, ind_value_col, ind_res_row, ind_res_col, ind_res_col_curr):
        # Base case: all the subcampaings have been evaluated
        if ind_res_row == self.subcampaigns and ind_res_col_curr == 0 and ind_res_col == 1:
            return results

        # Happens when the optimization step of the current subcampaing have been terminated
        elif ind_res_col_curr == 0 and ind_res_col == 1:
            return self.knapsack_optimization(results, ind_value_row + 1, 1, ind_res_row + 1,
                                              self.budgets, self.budgets)

        # Happens when we need to perform the optimization for the next budget in a given subcampaing
        elif ind_res_col_curr == 0:
            return self.knapsack_optimization(results, ind_value_row, 1, ind_res_row, ind_res_col - 1, ind_res_col - 1)

        # Perform the optimization for a given budget
        composed_value = self.values[ind_value_row - 1][ind_value_col - 1] + results[ind_res_row - 1][ind_res_col_curr - 1]

        results[ind_res_row][ind_res_col - 1] = max(composed_value, results[ind_res_row][ind_res_col - 1])

        return self.knapsack_optimization(results, ind_value_row, ind_value_col + 1, ind_res_row,
                                   ind_res_col, ind_res_col_curr - 1)




