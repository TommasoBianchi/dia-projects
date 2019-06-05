from environment.environment import Environment
from environment.click_function import Click_Function
from environment.subcampaign import Subcampaign

from distributions.gaussian import Gaussian

def build_environment(configuration):
	subcampaigns = []

	for subcampaign_data in configuration:
		click_functions = []

		for click_function_data in subcampaign_data:
			noise = Gaussian(click_function_data['noise_mean'], click_function_data['noise_variance'])
			click_function = Click_Function(noise, click_function_data['max_value'],
											click_function_data['offset'], click_function_data['speed'])
			click_functions.append(click_function)

		subcampaigns.append(Subcampaign(click_functions))

	return Environment(subcampaigns)