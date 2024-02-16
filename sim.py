import queue
import random
import numpy as np


def variable_poisson(*kwargs) -> int :
    if len(kwargs) == 1:
        return np.random.poisson(kwargs[0])[0]
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

class Server:
    """
    A server (till) that has a service time distribution
    """
    def __init__(self, distribution, index, *args):
        self.busy = False
        self.time_remaining = 0
        self.index = index
        self.service_time_dist = distribution
        self.args = args

    def start_service(self, instance_time):
        """
        Start service
        """
        self.busy = True
        self.time_remaining = int(distributions[self.service_time_dist](*self.args))
        #print(f"Server {self.index} started service at time {instance_time} with time remaining {self.time_remaining}")

    def service_one_time_unit(self, instance_time):
        """
        Service one time unit
        """
        if self.busy:
            self.time_remaining -= 1
            if self.time_remaining < 0:
                self.busy = False
                #print(f"Server {self.index} finished service at time {instance_time}")


class Customer:
    """
    A customer that has an arrival time
    """
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time

class Simulation:
    """
    A simulation of a M/M/c queuing system
    """
    def __init__(self, arrivals_dist, *args, servers, simulation_time):
        self.queue = queue.Queue()
        self.servers = []
        self.arrivals_dist = arrivals_dist

        for i in servers:
            self.servers.append(i)

        self.arr_args = args

        self.clock = 0
        self.simulation_time = simulation_time
        self.cust_served = 0
        self.cust_arrived = 0
        self.waiting_time = 0

    def run(self):
        """
        Run the simulation
        """
        while self.clock < self.simulation_time:
            self.handle_arrivals(self.clock)
            self.service(self.clock)
            self.clock += 1
        #print("Simulation finished")

    def handle_arrivals(self, instance_time):
        """
        Handle arrivals
        """
        #call the lambda arrival_dist function
        arr = distributions[self.arrivals_dist](self.arr_args)
        if arr > 0:
            for i in range(arr):
                self.queue.put(Customer(instance_time))
                self.cust_arrived += 1

    def service(self, instance_time):
        """
        Service
        """
        for server in self.servers:
            if server.busy:
                self.waiting_time += 1
            if not server.busy and not self.queue.empty():
                customer = self.queue.get()
                server.start_service(instance_time)
                self.cust_served += 1
            server.service_one_time_unit(instance_time)


    def Stats(self):
        """
        Print stats
        """

        # print("Simulation stats")
        # print(f"Customers arrived: {self.cust_arrived}")
        # print(f"Customers served: {self.cust_served}")
        # print(f"Customers left in queue: {self.queue.qsize()}")
        # print(f"Average waiting time: {self.waiting_time/self.cust_served}")

        return self.cust_arrived, self.cust_served, self.queue.qsize(), self.waiting_time/self.cust_served




def Test():
    arrival_dist = "poisson"
    lambda_arrival = 2

    server_1 = Server("exponential", 1, 1)
    server_2 = Server("uniform", 2, 1, 3)
    server_3 = Server("normal", 3, 5, 2)

    servers = [server_1, server_2, server_3]

    #run simulation
    sim = Simulation(arrival_dist, lambda_arrival, servers=servers, simulation_time=60*8)
    sim.run()
    return sim.Stats()


def Totals():
    results = []
    for i in range(100):
        results.append(Test())
    results = np.array(results)
    print(f"Average customers arrived: {np.mean(results[:,0])}")
    print(f"Average customers served: {np.mean(results[:,1])}")
    print(f"Average customers left in queue: {np.mean(results[:,2])}")
    print(f"Average waiting time: {np.mean(results[:,3])} \n")

    print(f"Standard deviation customers arrived: {np.std(results[:,0])}")
    print(f"Standard deviation customers served: {np.std(results[:,1])}")
    print(f"Standard deviation customers left in queue: {np.std(results[:,2])}")
    print(f"Standard deviation waiting time: {np.std(results[:,3])}\n")

    print(f"Max customers arrived: {np.max(results[:,0])}")
    print(f"Max customers served: {np.max(results[:,1])}")
    print(f"Max customers left in queue: {np.max(results[:,2])}")
    print(f"Max waiting time: {np.max(results[:,3])}\n")

    print(f"Min customers arrived: {np.min(results[:,0])}")
    print(f"Min customers served: {np.min(results[:,1])}")
    print(f"Min customers left in queue: {np.min(results[:,2])}")
    print(f"Min waiting time: {np.min(results[:,3])}\n")

    print(f"75% confidence interval customers arrived: {np.percentile(results[:,0], [25, 75])}")
    print(f"75% confidence interval customers served: {np.percentile(results[:,1], [25, 75])}")
    print(f"75% confidence interval customers left in queue: {np.percentile(results[:,2], [25, 75])}")
    print(f"75% confidence interval waiting time: {np.percentile(results[:,3], [25, 75])}\n")


if __name__ == "__main__":
    Totals()