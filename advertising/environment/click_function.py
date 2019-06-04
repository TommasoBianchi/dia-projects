import numpy as np

class Click_Function:

    #noise : Probability_Distribution
    def __init__(self, noise, max_height, offset, speed):
        self.noise = noise
        self.max_height = max_height
        self.offset = max_height / np.exp(-speed * offset)
        self.speed = speed
        
    def sample(self, x):
        return self.real_function_value(x) + self.noise.sample()

    def real_function_value(self, x):
        return max(0, (self.max_height - (self.offset * np.exp(-self.speed*x)) ))
