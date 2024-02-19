import queue
import random
import numpy as np

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
                self.NextArrivalTime = self.Time + self.arrival_dist()

                # print("Number of Arrivals: ", self.NArrivals)
                
                #Add the client that just arrived, the method on stateVariables handles the location of the client, returns -1 if theres no server available
                server_Number = self.stateVariables.AddClient()

                #If theres no server available, it returns -1, if there is one, we calculate the next departure from that server
                if server_Number != -1:
                    self.DepartureTime[server_Number] = self.Time + self.servers[server_Number]()
                
                else:
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
                    self.DepartureTime[next_departure_index] = self.Time + self.servers[next_departure_index]()

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
                    # print(self.stateVariables.Client_On_Server)
                    break

            # print("Clients on Queue: ", self.stateVariables.Clients_On_Queue)
            # print(self.stateVariables.Client_On_Server)
            # print()
            


def one_run():
    # Simulate the system 1000 times
    server1 = Normal(5,8)
    server2 = Uniform(4,3)
    server3 = Exponential(5)

    arrival = Poisson(1)

    sim = Sim([server1, server2, server3], arrival, total_time=60*8)
    sim.run()


for i in range(1000):
    one_run()