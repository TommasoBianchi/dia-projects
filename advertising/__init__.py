from knapsack.knapsack import Knapsack

values_ = [[0,2,5,7,6], [0,1,6,2,5], [0,7,5,3,5]]
values = [[0,0,0,0], [0,0,0,0], [0,0,0,0]]

algo = Knapsack(30,values)

result = algo.optimize()

x = 1

print(result)