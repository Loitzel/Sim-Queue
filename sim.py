import queue
import random
import numpy as np


class Server:
    """
    A server (till) that has a service time distribution
    """
    def __init__(self, service_time_dist, index):
        self.service_time_dist = service_time_dist
        self.busy = False
        self.time_remaining = 0
        self.index = index

    def start_service(self, instance_time):
        """
        Start service
        """
        self.busy = True
        self.time_remaining = self.service_time_dist[instance_time]
        print(f"Server {self.index} started service at time {instance_time} with time remaining {self.time_remaining}")

    def service_one_time_unit(self, instance_time):
        """
        Service one time unit
        """
        if self.busy:
            self.time_remaining -= 1
            if self.time_remaining < 0:
                self.busy = False
                print(f"Server {self.index} finished service at time {instance_time}")


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
    def __init__(self, arrivals_dist: list[int], service_time_dist, simulation_time, num_servers=2):
        self.queue = queue.Queue()
        self.servers = []
        self.arrivals_dist = arrivals_dist

        for i in service_time_dist:
            print(f'Service: {i}')
            self.servers.append(Server(i, len(self.servers) + 1))
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
        print("Simulation finished")

    def handle_arrivals(self, instance_time):
        """
        Handle arrivals
        """
        if self.arrivals_dist[instance_time] > 0:
            for i in range(self.arrivals_dist[instance_time]):
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

        print("Simulation stats")
        print(f"Customers arrived: {self.cust_arrived}")
        print(f"Customers served: {self.cust_served}")
        print(f"Customers left in queue: {self.queue.qsize()}")
        print(f"Average waiting time: {self.waiting_time/self.cust_served}")




# Test
#arrivals distributes Poisson(5)
arrivals = np.random.poisson(5, 100)

#2 servers
#service time distributes Exponential(1) only integers
service_time_1 = np.random.exponential(1, 100).astype(int)
#service time distributes Exponential(2)
service_time_2 = np.random.exponential(2, 100).astype(int)


services = [service_time_1, service_time_2]



sim = Simulation(arrivals, services, 100, 2)


sim.run()
sim.Stats()








