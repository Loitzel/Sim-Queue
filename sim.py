import math
import queue
import random
import numpy as np
from tabulate import tabulate

def generate_statistical_data(k, acceptable_deviation):
    
    global_data = []
    for i in range(k):
        global_data.append(one_run())

    waiting_times = [x.average_waiting_time() for x in global_data]
    max_waiting_times = [x.max_waiting_time() for x in global_data]
    probabilities_of_waiting = [x.probability_of_waiting_in_queue() for x in global_data]
    num_clients_served = [x.num_clients_served for x in global_data]
    num_clients = [x.num_clients for x in global_data]

    # Usando la función para calcular las medias
    mean_waiting_times = calculate_mean(waiting_times)
    mean_max_waiting_times = calculate_mean(max_waiting_times)
    mean_probabilities_of_waiting = calculate_mean(probabilities_of_waiting)
    mean_num_clients_served = calculate_mean(num_clients_served)
    mean_num_clients = calculate_mean(num_clients)

    # Usando la función para calcular las varianzas
    variance_waiting_times = calculate_variance(waiting_times, mean_waiting_times)
    variance_max_waiting_times = calculate_variance(max_waiting_times, mean_max_waiting_times)
    variance_probabilities_of_waiting = calculate_variance(probabilities_of_waiting, mean_probabilities_of_waiting)
    variance_num_clients_served = calculate_variance(num_clients_served, mean_num_clients_served)
    variance_num_clients = calculate_variance(num_clients, mean_num_clients)

    # Calcular el error estándar
    standard_error_waiting_times = math.sqrt(variance_waiting_times / k)
    standard_error_max_waiting_times = math.sqrt(variance_max_waiting_times / k)
    standard_error_probabilities_of_waiting = math.sqrt(variance_probabilities_of_waiting / k)
    standard_error_num_clients_served = math.sqrt(variance_num_clients_served / k)
    standard_error_num_clients = math.sqrt(variance_num_clients / k)

    # Calcular el intervalo de confianza para 95% de confianza
    confidence_interval_waiting_times = (mean_waiting_times - 1.96 * standard_error_waiting_times, mean_waiting_times + 1.96 * standard_error_waiting_times)
    confidence_interval_max_waiting_times = (mean_max_waiting_times - 1.96 * standard_error_max_waiting_times, mean_max_waiting_times + 1.96 * standard_error_max_waiting_times)
    confidence_interval_probabilities_of_waiting = (mean_probabilities_of_waiting - 1.96 * standard_error_probabilities_of_waiting, mean_probabilities_of_waiting + 1.96 * standard_error_probabilities_of_waiting)
    confidence_interval_num_clients_served = (mean_num_clients_served - 1.96 * standard_error_num_clients_served, mean_num_clients_served + 1.96 * standard_error_num_clients_served)
    confidence_interval_num_clients = (mean_num_clients - 1.96 * standard_error_num_clients, mean_num_clients + 1.96 * standard_error_num_clients)

    # Calcular la amplitud del intervalo de confianza para cada estadística
    amplitude_waiting_times = confidence_interval_waiting_times[1] - confidence_interval_waiting_times[0]
    amplitude_max_waiting_times = confidence_interval_max_waiting_times[1] - confidence_interval_max_waiting_times[0]
    amplitude_probabilities_of_waiting = confidence_interval_probabilities_of_waiting[1] - confidence_interval_probabilities_of_waiting[0]
    amplitude_num_clients_served = confidence_interval_num_clients_served[1] - confidence_interval_num_clients_served[0]
    amplitude_num_clients = confidence_interval_num_clients[1] - confidence_interval_num_clients[0]
    
    # Definir los datos como una lista de tuplas
    data = [
        ("Waiting Times", mean_waiting_times, variance_waiting_times, standard_error_waiting_times, confidence_interval_waiting_times, amplitude_waiting_times),
        ("Max Waiting Times", mean_max_waiting_times, variance_max_waiting_times, standard_error_max_waiting_times, confidence_interval_max_waiting_times, amplitude_max_waiting_times),
        ("Probabilities of Waiting", mean_probabilities_of_waiting, variance_probabilities_of_waiting, standard_error_probabilities_of_waiting, confidence_interval_probabilities_of_waiting, amplitude_probabilities_of_waiting),
        ("Num Clients Served", mean_num_clients_served, variance_num_clients_served, standard_error_num_clients_served, confidence_interval_num_clients_served, amplitude_num_clients_served),
        ("Num Clients", mean_num_clients, variance_num_clients, standard_error_num_clients, confidence_interval_num_clients, amplitude_num_clients)
    ]

    # Definir los encabezados de la tabla
    headers = ["Variable", "Mean", "Variance", "Standard Error", "95% Confidence Interval", "Amplitude"]

    # Imprimir la tabla utilizando la función tabulate
    print(tabulate(data, headers=headers, tablefmt="grid"))

    
    

def calculate_mean(data):
    return sum(data) / len(data)

def calculate_variance(data, mean):
    sum_squared_diff = sum((x - mean) ** 2 for x in data)
    return sum_squared_diff / (len(data) - 1)

class StatisticsHolder:
    def __init__(self):
        self.waiting_times = []
        self.total_wait_time = 0
        self.max_wait_time = float('-inf')
        self.num_clients_served = 0
        self.num_clients = 0
        self.customers_in_queue_due_to_wait = 0

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
    
    def print_stats(self):
        print("Total clients served:", self.num_clients_served)
        print("Total clients unattended:", self.client_unattended())
        print("Customers in queue due to wait:", self.customers_in_queue_due_to_wait)
        print("Probability of waiting in queue:", self.probability_of_waiting_in_queue())
        print("Average waiting time:", self.average_waiting_time())
        print("Max waiting time:", self.max_waiting_time())


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
        return np.random.poisson(self.args[0])

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
    def __init__(self, array_size):
        self.Clients_On_Queue = 0
        self.Client_On_Server = [0] * array_size
        self.queue = queue.Queue()
        self.last_client = 0

    def AddClient(self):
        
        freeServer = self.FindFirstFreeServer()

        #add client to queue
        self.last_client += 1
        self.queue.put(self.last_client)
        self.Clients_On_Queue += 1

        if freeServer != -1:
            self.Clients_On_Queue -= 1
            next_client = self.queue.get()
            self.Client_On_Server[freeServer] = next_client

        return freeServer

            
    def FindFirstFreeServer(self):
        for i in range(len(self.Client_On_Server)):
            if self.Client_On_Server[i] == 0:
                return i
        return -1
    
    def RemoveClient(self, server_number):

        self.Client_On_Server[server_number] = 0


    def Place_From_Queue(self, server_number):
        if self.Clients_On_Queue > 0:
            self.Clients_On_Queue -= 1
            next_client = self.queue.get()
            self.Client_On_Server[server_number] = next_client
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
        
        self.stats : StatisticsHolder = StatisticsHolder()

        #time variable
        self.Time = 0
        self.TotalTime = total_time
        
        amount_of_servers = len(servers)
        self.stateVariables = StateVariables(amount_of_servers)

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

    def run(self):

        while True:
            
            next_event = min(self.NextArrivalTime, min(self.DepartureTime))
            next_departure_index = self.DepartureTime.index(min(self.DepartureTime))
            
            #Case 1: A client arrives before someone else leaves
            if self.NextArrivalTime == next_event and self.Time <= self.TotalTime:
                

                self.Time = self.NextArrivalTime
                self.NArrivals += 1
                self.stats.num_clients += 1
                self.NextArrivalTime = self.Time + self.arrival_dist()

                # print("Number of Arrivals: ", self.NArrivals)
                
                #Add the client that just arrived, the method on stateVariables handles the location of the client, returns -1 if theres no server available
                server_Number = self.stateVariables.AddClient()

                #If theres no server available, it returns -1, if there is one, we calculate the next departure from that server
                if server_Number != -1:
                    self.stats.num_clients_served += 1
                    waiting_time = self.servers[server_Number]()

                    self.DepartureTime[server_Number] = self.Time + waiting_time
                    self.stats.add_waiting_time(waiting_time)
                
                else:
                    self.stats.customers_in_queue_due_to_wait += 1
                    pass
            
            #Case 2: A client leaves a server
            elif self.Time <= self.TotalTime:

                self.Time = next_event
                self.NDepartures[next_departure_index] += 1

                # print("Client is leaving, number: " + str(self.stateVariables.Client_On_Server[next_departure_index]))
                self.stateVariables.RemoveClient(next_departure_index)

                #If theres someone waiting for be attended, we place it on the now free server
                if(self.stateVariables.Clients_On_Queue > 0):
                    
                    self.stateVariables.Place_From_Queue(next_departure_index)
                    waiting_time = self.servers[next_departure_index]()
                    self.DepartureTime[next_departure_index] = self.Time + waiting_time
                    
                    self.stats.add_waiting_time(waiting_time)
                    self.stats.num_clients_served += 1

                else:
                    self.DepartureTime[next_departure_index] = float('inf')

            #Case 3: Time is over, we attend the rest of the clients
            else:
                self.Time = next_event
                self.NDepartures[next_departure_index] += 1
                self.stateVariables.RemoveClient(next_departure_index)
                self.DepartureTime[next_departure_index] = float('inf')

                if(self.stateVariables.Clients_On_Queue > 0):
                    self.stateVariables.Place_From_Queue(next_departure_index)
                    self.DepartureTime[next_departure_index] = self.Time + self.servers[next_departure_index]()

                if self.stateVariables.NoMoreClients():
                    break

            # print("Clients on Queue: ", self.stateVariables.Clients_On_Queue)
            # print(self.stateVariables.Client_On_Server)
            # print()
            


def one_run():
    server1 = Exponential(5)
    server2 = Exponential(6)
    server3 = Exponential(3)

    arrival = Poisson(1)

    sim = Sim([server1, server2, server3], arrival, total_time=100)
    sim.run()
    return sim.stats

k = 100
acceptable_deviation = 0.05

generate_statistical_data(k, acceptable_deviation)



