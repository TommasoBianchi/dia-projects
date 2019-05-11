from advertising.knapsack.knapsack import Knapsack

values = [[1,2,5,7], [7,15,4,7], [5,4,2,12]]
algo = Knapsack(3,3,values)

result = algo.optimize()

x = 1