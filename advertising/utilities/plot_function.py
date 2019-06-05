import matplotlib.pyplot as plt

def plot_function(f, x_values):
	plt.plot(x_values, [f(x) for x in x_values])