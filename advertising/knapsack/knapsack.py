class Knapsack:
    def __init__(self, subcampaigns, budgets, values):
        self.subcampaigns = subcampaigns
        self.budgets = budgets

        # It is a matrix: values[subcamp_id][budget_id] = value
        self.values = values
        self.results = [[]]

    def optimize(self):
        results = [[0]*len(self.budgets)]*len(self.subcampaigns + 1)
        return self.knapsack_optimization(results, 0, 0, 1, len(self.budgets), len(self.budgets))

    def knapsack_optimization(self, results, ind_value_row, ind_value_col, ind_res_row, ind_res_col, ind_res_col_curr):
        # Base case 1
        if ind_res_row == len(self.subcampaigns + 1) and ind_res_col == -1:
            return results

        if ind_res_col == -1:
            self.knapsack_optimization(results, ind_value_row + 1, 0, ind_res_row + 1, ind_res_col - 1, ind_res_col - 1)

        composed_value = sum(self.values[ind_value_row][ind_value_col], results[ind_res_row - 1][ind_res_col_curr])

        if composed_value > results[ind_res_row][ind_res_col]:
            results[ind_res_row][ind_res_col] = composed_value

        self.knapsack_optimization(results, ind_value_row, ind_value_col + 1, ind_res_col, ind_res_col_curr - 1)

        return results




