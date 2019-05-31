import numpy as np


class Click_Function:

    def __init__(self, noise, max_height, offset, speed):
        self.noise = noise
        self.max_height = max_height
        self.offset = offset
        self.speed = speed
        
    def sample(self, x):
        return self.__real_function_value(x) + self.noise.sample()

    def __real_function_value(self, x):
        return max(0, (self.max_height - (self.offset * np.exp(-self.speed*x)) ))
