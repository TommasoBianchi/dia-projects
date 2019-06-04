from knapsack.knapsack import Knapsack

values = [[0,2,5,7], [0,1,6,2], [0,7,5,3]]
values_ = [[0,0,0,0], [0,0,0,0], [0,0,0,0]]

algo = Knapsack(30,values)

result = algo.optimize()

x = 1

print(result)