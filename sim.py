import queue
import random
import numpy as np


def variable_poisson(*kwargs) -> int :

    return np.random.poisson(1)
    # if len(kwargs) == 1:
    #     return np.random.poisson(kwargs[0])
    # else:
    #     raise ValueError("Poisson distribution takes only one parameter")

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
    
    def __init__(self, server_distributions, arrival_time_distribution, total_time):
        
        #time variable
        self.Time = 0
        self.TotalTime = total_time

        amount_of_servers = len(server_distributions)
        self.stateVariables = StateVariables(amount_of_servers)

        #Counter Variables
        self.NArrivals = 0 #Total number of arrivals at time t
        self.NDepartures = [0] * amount_of_servers #Total number of clients attended by server i

        #Distributions
        self.server_distributions = server_distributions
        self.arrival_time_distribution = arrival_time_distribution

        #Output Variables
        self.NextArrivalTime = arrival_time_distribution() #arrival time of client i
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
                self.NextArrivalTime = self.Time + self.arrival_time_distribution()

                print("Number of Arrivals: ", self.NArrivals)
                
                #Add the client that just arrived, the method on stateVariables handles the location of the client, returns -1 if theres no server available
                server_Number = self.stateVariables.AddClient()

                #If theres no server available, it returns -1, if there is one, we calculate the next departure from that server
                if server_Number != -1:
                    self.DepartureTime[server_Number] = self.Time + self.server_distributions[server_Number]()
                
                else:
                    pass
            
            #Case 2: A client leaves a server
            elif self.Time <= self.TotalTime:

                self.Time = next_event
                self.NDepartures[next_departure_index] += 1

                print("Client is leaving, number: " + str(self.stateVariables.Client_On_Server[next_departure_index]))
                self.stateVariables.RemoveClient(next_departure_index)

                #If theres someone waiting for be attended, we place it on the now free server
                if(self.stateVariables.Clients_On_Queue > 0):
                    
                    self.stateVariables.Place_From_Queue(next_departure_index)
                    self.DepartureTime[next_departure_index] = self.Time + self.server_distributions[next_departure_index]()

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
                    self.DepartureTime[next_departure_index] = self.Time + self.server_distributions[next_departure_index]()

                if self.stateVariables.NoMoreClients():
                    print(self.stateVariables.Client_On_Server)
                    break

            print("Clients on Queue: ", self.stateVariables.Clients_On_Queue)
            print(self.stateVariables.Client_On_Server)
            print()
            

def main():
    # Simulate the system 1000 times
    sim = Sim([variable_poisson, variable_poisson, variable_poisson], variable_poisson, total_time=10)
    sim.run()
    #sim.print_results()


main()