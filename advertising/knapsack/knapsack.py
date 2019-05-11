class Knapsack:
    def __init__(self, subcampaigns, budgets, values):
        self.subcampaigns = subcampaigns
        self.budgets = budgets

        # It is a matrix: values[subcamp_id][budget_id] = value
        self.values = values

    def optimize(self):
        results = [[0]*self.budgets]*(self.subcampaigns + 1)
        return self.knapsack_optimization(results, 1, 1, 1, self.budgets, self.budgets)

    def knapsack_optimization(self, results, ind_value_row, ind_value_col, ind_res_row, ind_res_col, ind_res_col_curr):
        # Base case 1
        if ind_res_row == self.subcampaigns + 1 and ind_res_col == 0:
            return results

        if ind_res_col_curr == 0:
            return self.knapsack_optimization(results, ind_value_row + 1, 0, ind_res_row + 1, ind_res_col - 1, ind_res_col - 1)

        composed_value = self.values[ind_value_row - 1][ind_value_col - 1] + results[ind_res_row - 1][ind_res_col_curr - 1]

        if composed_value > results[ind_res_row][ind_res_col - 1]:
            results[ind_res_row][ind_res_col - 1] = composed_value

        return self.knapsack_optimization(results, ind_value_row, ind_value_col + 1, ind_res_row,
                                   ind_res_col, ind_res_col_curr - 1)




