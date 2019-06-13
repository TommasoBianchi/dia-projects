import numpy as np

class Click_Function:

    #noise : Probability_Distribution
    def __init__(self, noise, max_height, offset, speed, id, calculateOffset = True):
        self.noise = noise
        self.max_height = max_height
        if calculateOffset:
            self.offset = max_height / np.exp(-speed * offset)
        else:
            self.offset = offset
        self.speed = speed
        self.samples = []
        self.id = id
        
    def sample(self, x, save_sample = True):
        sample = self.real_function_value(x) + self.noise.sample()
        if save_sample:
            self.samples.append((x, sample))
        return sample

    def real_function_value(self, x):
        return max(0, (self.max_height - (self.offset * np.exp(-self.speed*x)) ))

    def copy(self):
        cf = Click_Function(self.noise, self.max_height, self.offset, self.speed, self.id, calculateOffset = False)
        cf.samples = self.samples.copy()
        return cf