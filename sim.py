import math
import queue
import random
import numpy as np
from tabulate import tabulate

def generate_statistical_data(k, acceptable_deviation):
    
    global_data = []
    for i in range(k):
        global_data.append(one_run())

    # waiting_times = [x.average_waiting_time() for x in global_data]
    # max_waiting_times = [x.max_waiting_time() for x in global_data]
    probabilities_of_waiting = [x.probability_of_waiting_in_queue() for x in global_data]
    num_clients_served = [x.num_clients_served for x in global_data]
    num_clients = [x.num_clients for x in global_data]
    empty_times = [x.probability_of_empty() for x in global_data]
    queue_length = [x.avg_clients_in_queue() for x in global_data]
    avg_time_on_queue = [x.avg_time_on_queue() for x in global_data]
    avg_time_in_system = [x.avg_time_in_system() for x in global_data]

    variables = [ probabilities_of_waiting, num_clients_served, num_clients,
                 empty_times, queue_length, avg_time_on_queue, avg_time_in_system]

    means = [calculate_mean(x) for x in variables]
    variances = [calculate_variance(x, means[i]) for i, x in enumerate(variables)]
    standard_errors = [math.sqrt(x / k) for x in variances]
    confidence_intervals = [(means[i] - 1.96 * standard_errors[i], means[i] + 1.96 * standard_errors[i]) for i in range(len(means))]
    amplitudes = [confidence_intervals[i][1] - confidence_intervals[i][0] for i in range(len(confidence_intervals))]

    data = []

    case = [ "Probabilities of Waiting", "Num Clients Served", "Num Clients",
            "Probability of 0 clients in the system", "Avg Clients in Queue", "Avg Time on Queue", "Avg Time in System"]
    # Definir los datos como una lista de tuplas

    for i in range(len(case)):
        row =  means[i], variances[i], standard_errors[i], confidence_intervals[i], amplitudes[i]
        data.append(row)

    # Definir los encabezados de las filas
    for i in range(len(case)):
        data[i] = (case[i],) + data[i]

    # Definir los encabezados de la tabla
    headers = ["Variable", "Mean", "Variance", "Standard Error", "95% Confidence Interval", "Amplitude"]

    # Imprimir la tabla utilizando la función tabulate
    table = tabulate(data, headers=headers, tablefmt="grid")

    print(table)

    return table

def generate_mathematical_analysis(lambda_, c, mu, time):
    rho = lambda_ / (c *mu)

    def probability_of_queuing():
        #Erlang C Formula
        den = 1
        den_ = 1-rho
        den_ *= math.factorial(c) / (c * rho)**c
        den_ *= sum([ (c*rho)**i / math.factorial(i) for i in range(c)])
        den += den_
        return 1 / den

    def average_clients_in_system():
        return rho/(1-rho) * probability_of_queuing() + c*rho

    def p0():
        den = sum([(c*rho)**i / math.factorial(i) for i in range(c)])
        den += (c*rho)**c / (math.factorial(c) * (1-rho))
        return 1 / den

    def lq():
        return p0() * (c*rho)**c * rho / (math.factorial(c) * (1-rho)**2)

    def wq():
        return lq() / lambda_

    def w():
        return wq() + 1/mu

    def l():
        return lambda_ * w()

    print(f'Mathematical Results: \n\n☻ Probability of waiting in a queue: {probability_of_queuing()} '
          f'\n☻ Average number of clients in the system: {average_clients_in_system()*time}'
          f'\n☻ Probability of 0 clients in the system: {p0()}'
            f'\n☻ Average number of clients in the queue: {lq()*time}'
            f'\n☻ Average time a client spends in the queue: {wq()}'
            f'\n☻ Average time a client spends in the system: {w()}')



    

def calculate_mean(data):
    return sum(data) / len(data)

def calculate_variance(data, mean):
    sum_squared_diff = sum((x - mean) ** 2 for x in data)
    return sum_squared_diff / (len(data) - 1)

class StatisticsHolder:
    def __init__(self, T):
        self.waiting_times = []
        self.total_wait_time = 0
        self.max_wait_time = float('-inf')
        self.num_clients_served = 0
        self.num_clients = 0
        self.customers_in_queue_due_to_wait = 0
        self.empty_times = []
        self.T = T
        self.clients_in_queue = []
        self.queued = 0
        self.time_in_queue = {}
        self.time_in_system = {}

    def add_waiting_time(self, waiting_time):
        self.waiting_times.append(waiting_time)
        self.total_wait_time += waiting_time
        if waiting_time > self.max_wait_time:
            self.max_wait_time = waiting_time

    def client_unattended(self):
        return self.num_clients - self.num_clients_served

    def average_waiting_time(self):
        if self.num_clients_served == 0:
            return 0
        return self.total_wait_time / self.num_clients_served

    def max_waiting_time(self):
        if self.max_wait_time == float('-inf'):
            return 0
        return self.max_wait_time
    
    def probability_of_waiting_in_queue(self):
        return self.customers_in_queue_due_to_wait / self.num_clients

    def calc_empty_time(self):
        emp = 0
        for i in range(0, len(self.empty_times), 2):
            emp += self.empty_times[i + 1] - self.empty_times[i]
        return emp

    def probability_of_empty(self):
        return self.calc_empty_time() / self.T

    def avg_clients_in_queue(self):
        return self.queued

    def avg_time_on_queue(self):
        return sum(self.time_in_queue.values()) / len(self.time_in_queue)

    def avg_time_in_system(self):
        return sum(self.time_in_system.values()) / len(self.time_in_system)

    
    def print_stats(self):
        print("Total clients served:", self.num_clients_served)
        print("Total clients unattended:", self.client_unattended())
        print("Customers in queue due to wait:", self.customers_in_queue_due_to_wait)
        print("Probability of waiting in queue:", self.probability_of_waiting_in_queue())
        print("Average waiting time:", self.average_waiting_time())
        print("Max waiting time:", self.max_waiting_time())
        print("Empty time:", self.calc_empty_time())



    

class Distribution:
    def __init__(self, distribution, *args):
        self.distribution = distribution
        self.args = args

    def __call__(self):
        raise NotImplementedError("This method should be implemented in the subclass")

class Poisson(Distribution):
    def __init__(self, *args):
        super().__init__('variable_poisson', *args)

    def __call__(self):
        # times between events that distribute poisson, follow exponential distribution
        return np.log(1 - np.random.random()) / -self.args[0]

class Exponential(Distribution):
    def __init__(self, *args):
        super().__init__('variable_exponential', *args)

    def __call__(self):
        return np.random.exponential(self.args[0])


class Uniform(Distribution):
    def __init__(self, *args):
        super().__init__('variable_uniform', *args)

    def __call__(self):
        return np.random.uniform(self.args[0], self.args[1])

class Normal(Distribution):
    def __init__(self, *args):
        super().__init__('variable_normal', *args)

    def __call__(self):
        return np.random.normal(self.args[0], self.args[1])


class StateVariables:
    def __init__(self, array_size, stat):
        self.Clients_On_Queue = 0
        self.Client_On_Server = [0] * array_size
        self.queue = queue.Queue()
        self.last_client = 0
        self.queued = 0
        self.stats : StatisticsHolder = stat

    def AddClient(self, t):
        
        freeServer = self.FindFirstFreeServer()

        #add client to queue
        self.last_client += 1
        self.queue.put(self.last_client)
        self.Clients_On_Queue += 1
        self.stats.time_in_queue[self.last_client] = t
        self.stats.time_in_system[self.last_client] = t

        if freeServer != -1:
            self.Clients_On_Queue -= 1
            next_client = self.queue.get()
            self.Client_On_Server[freeServer] = next_client
            self.stats.time_in_queue[next_client] = t - self.stats.time_in_queue[next_client]

        else:
            self.queued += 1

        return freeServer

            
    def FindFirstFreeServer(self):
        for i in range(len(self.Client_On_Server)):
            if self.Client_On_Server[i] == 0:
                return i
        return -1
    
    def RemoveClient(self, server_number, t):
        cl = self.Client_On_Server[server_number]
        if cl != 0:
            self.stats.time_in_system[cl] = t - self.stats.time_in_system[cl]

        self.Client_On_Server[server_number] = 0


    def Place_From_Queue(self, server_number, t):
        if self.Clients_On_Queue > 0:
            self.Clients_On_Queue -= 1
            next_client = self.queue.get()
            self.Client_On_Server[server_number] = next_client
            self.stats.time_in_queue[next_client] = t - self.stats.time_in_queue[next_client]
            return True

        return False
    
    def NoMoreClients(self):

        ClientsOnServers = False
        for i in range(len(self.Client_On_Server)):
            if self.Client_On_Server[i] != 0:
                ClientsOnServers = True

        return self.Clients_On_Queue == 0 and not ClientsOnServers


class Sim:
    
    def __init__(self, servers, arrival_dist, total_time):
        
        self.stats : StatisticsHolder = StatisticsHolder(total_time)

        #time variable
        self.Time = 0
        self.TotalTime = total_time
        
        amount_of_servers = len(servers)
        self.stateVariables = StateVariables(amount_of_servers, self.stats)

        #Counter Variables
        self.NArrivals = 0 #Total number of arrivals at time t
        self.NDepartures = [0] * amount_of_servers #Total number of clients attended by server i

        #Distributions
        self.servers = servers
        self.arrival_dist = arrival_dist

        #Output Variables
        self.NextArrivalTime = arrival_dist()
        self.DepartureTime = [float('inf')]  * amount_of_servers #departure time of client i

        #Events
        self.nextArrival = 0
        self.nextDeparture = [0] * amount_of_servers

        self.used = False

    def run(self):
        while True:
            
            next_event = min(self.NextArrivalTime, min(self.DepartureTime))
            next_departure_index = self.DepartureTime.index(min(self.DepartureTime))
            
            #Case 1: A client arrives before someone else leaves
            if self.NextArrivalTime == next_event and self.Time <= self.TotalTime:

                if self.used is False:
                    self.stats.empty_times.append(self.Time)
                    self.stats.empty_times.append(self.NextArrivalTime)
                    self.used = True


                self.Time = self.NextArrivalTime
                self.NArrivals += 1
                self.stats.num_clients += 1
                self.NextArrivalTime = self.Time + self.arrival_dist()

                #Add the client that just arrived, the method on stateVariables handles the location of the client, returns -1 if theres no server available
                server_Number = self.stateVariables.AddClient(self.Time)

                #If theres no server available, it returns -1, if there is one, we calculate the next departure from that server
                if server_Number != -1:
                    self.stats.num_clients_served += 1
                    waiting_time = self.servers[server_Number]()

                    self.DepartureTime[server_Number] = self.Time + waiting_time
                    self.stats.add_waiting_time(waiting_time)

                
                else:
                    self.stats.customers_in_queue_due_to_wait += 1
                    pass

                self.stats.clients_in_queue.append(self.stateVariables.Clients_On_Queue)
            
            #Case 2: A client leaves a server
            elif self.Time <= self.TotalTime:

                self.Time = next_event
                self.NDepartures[next_departure_index] += 1
                self.stateVariables.RemoveClient(next_departure_index, self.Time)

                #If theres someone waiting for be attended, we place it on the now free server
                if(self.stateVariables.Clients_On_Queue > 0):
                    
                    self.stateVariables.Place_From_Queue(next_departure_index, self.Time)
                    waiting_time = self.servers[next_departure_index]()
                    self.DepartureTime[next_departure_index] = self.Time + waiting_time
                    
                    self.stats.add_waiting_time(waiting_time)
                    self.stats.num_clients_served += 1

                else:
                    self.DepartureTime[next_departure_index] = float('inf')

                if self.stateVariables.NoMoreClients():
                    self.used = False

                self.stats.clients_in_queue.append(self.stateVariables.Clients_On_Queue)

            #Case 3: Time is over, we attend the rest of the clients
            else:
                self.Time = next_event
                self.NDepartures[next_departure_index] += 1
                self.stateVariables.RemoveClient(next_departure_index, self.Time)
                self.DepartureTime[next_departure_index] = float('inf')

                if(self.stateVariables.Clients_On_Queue > 0):
                    self.stateVariables.Place_From_Queue(next_departure_index, self.Time)
                    self.DepartureTime[next_departure_index] = self.Time + self.servers[next_departure_index]()

                if self.stateVariables.NoMoreClients():
                    break

                self.stats.clients_in_queue.append(self.stateVariables.Clients_On_Queue)

        self.stats.queued = self.stateVariables.queued

def one_run():



    server1 = Exponential(mu)
    server2 = Exponential(mu)
    server3 = Exponential(mu)

    arrival = Poisson(lambda_)

    sim = Sim([server1, server2, server3], arrival, total_time=1000)
    sim.run()
    return sim.stats

lambda_ = 2
c = 3
mu = 1
k = 1000
acceptable_deviation = 0.05

table = generate_statistical_data(k, acceptable_deviation)

generate_mathematical_analysis(lambda_, c, mu, k)




