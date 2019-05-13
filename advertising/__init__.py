from advertising.knapsack.knapsack import Knapsack

values = [[1,2,5,6], [7,1,4,0], [5,4,2,0], [5,10,0,0]]
algo = Knapsack(4,30,values)

result = algo.optimize()

x = 1