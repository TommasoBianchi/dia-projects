from environment.click_function import Click_Function
from distributions.gaussian import Gaussian
from environment.subcampaign import Subcampaign
from environment.environment import Environment
from knapsack.knapsack import Knapsack
from experiment.subcampaign_algo import Subcampaign_algo
import matplotlib.pyplot as plt
import numpy as np

noise = Gaussian(0,1)
class_1 = Click_Function(noise, 10, 2, 1)
subcampaign_1 = Subcampaign([class_1])

class_2 = Click_Function(noise, 15, 15, 0.5)
subcampaign_2 = Subcampaign([class_2])

environment = Environment([class_1, class_2])

subcampaign_algo_1 = Subcampaign_algo(4,[0,10,20,30])
subcampaign_algo_2 = Subcampaign_algo(4,[0,10,20,30])
subcampaign_algos = [subcampaign_algo_1, subcampaign_algo_2]

rewards = []

for t in range(100):
    subcampaign_algo_1_values = [subcampaign_algo_1.sample_from_gp(arm) for arm in [0,10,20,30]]
    subcampaign_algo_2_values = [subcampaign_algo_2.sample_from_gp(arm) for arm in [0,10,20,30]]
    knapsack = Knapsack(3, 30, [subcampaign_algo_1_values, subcampaign_algo_2_values])
    super_arm = knapsack.optimize()
    super_arm = [(1,10 * (t % 4)), (0,20)]    ### TEST
    total_reward = 0
    for (subcampaign_id, budget_assigned) in super_arm:
        reward = environment.get_subcampaign(subcampaign_id).sample(budget_assigned)
        total_reward += reward
        subcampaign_algos[subcampaign_id].update(budget_assigned, reward)
    rewards.append(total_reward)

#print(rewards)

#plt.plot(np.cumsum(rewards))
#plt.show()

plt.plot([x for x in range(40)], [class_2.real_function_value(x) for x in range(40)])
plt.plot([x for x in range(40)], [subcampaign_algo_2.gaussian_process.gaussian_process.predict(np.atleast_2d(x).T)[0] for x in range(40)])
plt.show()