from advertising.knapsack.knapsack import Knapsack

values = [[1,2,5], [7,88,4], [5,4,2]]
algo = Knapsack(3,3,values)

result = algo.optimize()

x = 1