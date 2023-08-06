import random

class System:
    def __init__(self, a, b, y0=0, noise=False):
        self.y = y0
        self.noise = noise
        self.f = lambda y, u: a * y + b * u
        self.iteration = 0
        
    def sense(self):
        if self.noise:
            y = self.y + random.random() / 10
            self.y = y if y > 0 else 0 
        return self.y
    
    def apply(self, u):
        self.y = self.f(self.y, u)
        self.iteration += 1
        return self
        
    def get_time(self):
        return self.iteration
        
class IntroSystem(System):
    def __init__(self):
        System.__init__(self, 0.8, 0.5, y0=0, noise=False)

class NoisySystem(System):
    def __init__(self):
        System.__init__(self, 0.8, 0.5, y0=0, noise=True)
        
class UnknownSystem(System):
    def __init__(self):
        System.__init__(self, 0.628, 0.314, y0=0, noise=True)
