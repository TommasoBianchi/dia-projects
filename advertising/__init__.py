from advertising.knapsack.knapsack import Knapsack

values = [[0,2,5,7], [0,1,6,2], [0,7,5,3]]
algo = Knapsack(4,30,values)

result = algo.optimize()

x = 1