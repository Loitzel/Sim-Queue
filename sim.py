import queue
import random
import numpy as np


def variable_poisson(*kwargs) -> int :
    if len(kwargs) == 1:
        return np.random.poisson(kwargs[0])
    else:
        raise ValueError("Poisson distribution takes only one parameter")

def variable_exponential(*kwargs) -> float:
    if len(kwargs) == 1:
        return np.random.exponential(kwargs[0])
    else:
        raise ValueError("Exponential distribution takes only one parameter")

def variable_uniform(*kwargs) -> float:
    if len(kwargs) == 2:
        return np.random.uniform(kwargs[0], kwargs[1])
    else:
        raise ValueError("Uniform distribution takes only two parameters")

def variable_normal(*kwargs):
    if len(kwargs) == 2:
        return np.random.normal(kwargs[0], kwargs[1])
    else:
        raise ValueError("Normal distribution takes only two parameters")


#dictionary so I can send the distribution as a lambda
distributions = {
    "poisson": variable_poisson,
    "exponential": variable_exponential,
    "uniform": variable_uniform,
    "normal": variable_normal
}

class Sim:
    def __init__(self, arrival_dist, *args, total_time):
        
        #time variable
        self.t = 0

        #counting variables
        self.NA = self.ND = 0
        self.n = 0

        #state variables
        self.n1 = self.n2 = 0

        #out variables
        self.A1 = dict()
        self.A2 = dict()
        self.D = dict()

        #event variables
        self.t1 = self.t2 = float('inf')

        #distribution
        self.arrival_dist = arrival_dist
        self.arrival_args = args

        #total time
        self.total_time = total_time

        self.T0 = distributions[self.arrival_dist](*self.arrival_args)
        self.ta = self.T0
    
    def run(self):
        
        while self.t < self.total_time:

            if self.ta == min(self.ta, self.t1, self.t2) and self.ta <= self.total_time:
                self.t = self.ta #Update current time
                self.NA += 1 #Updates arrivals
                self.n1 += 1
                Tt = distributions[self.arrival_dist](*self.arrival_args)
                self.ta = self.t + Tt
                if self.n1 == 1:
                    y1 = distributions["exponential"](1)
                    self.t1 = self.t + y1
                self.A1[self.NA] = self.t
            
            if self.t1 < self.ta and self.t1 <= self.t2 and self.t1< self.total_time:
                self.t = self.t1
                self.n1 -= 1
                self.n2 += 1
                if self.n1 == 0:
                    self.t1 = 1
                else:
                    y1 = distributions["exponential"](1)
                    self.t1 = self.t + y1
                if self.n2 == 1:
                    y2 = distributions["exponential"](1)
                    self.t2 = self.t + y2
                self.A2[self.NA - self.n1] = self.t

            if self.t2 < self.ta and self.t2 < self.t1 and self.t2 < self.total_time:
                self.t = self.t2
                self.ND += 1
                self.n2 -= 1
                if self.n2 == 0:
                    self.t2 = 1
                else:
                    y2 = distributions["exponential"](1)
                    self.t2 = self.t + y2
                self.D[self.ND] = self.t


    def print_results(self):
        print("A1: ", self.A1)
        print("A2: ", self.A2)
        print("D: ", self.D)

        #means
        print("Mean A1: ", sum(self.A1.values())/len(self.A1))
        print("Mean A2: ", sum(self.A2.values())/len(self.A2))
        print("Mean D: ", sum(self.D.values())/len(self.D))


def main():
    # Simulate the system 1000 times
    sim = Sim("poisson", 1, total_time=10)
    sim.run()
    sim.print_results()


main()