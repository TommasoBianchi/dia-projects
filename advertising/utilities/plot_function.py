import matplotlib.pyplot as plt

def plot_function(f, x_values, std_function = None, std_alpha = 0.05):
	plt.plot(x_values, [f(x) for x in x_values])

	if (std_function != None):
		lower_bounds = [f(x) - 1.96 * std_function(x) for x in x_values]
		upper_bounds = [f(x) + 1.96 * std_function(x) for x in x_values]
		plt.fill_between(x_values, lower_bounds, upper_bounds, alpha = std_alpha)