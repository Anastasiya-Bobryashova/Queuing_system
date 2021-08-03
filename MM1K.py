from queue import Queue
from random import expovariate
import matplotlib.pyplot as plt
import tabulate
import seaborn as sns

class Demand:

    def __init__(self, arrival_time = None):
        self.arrival_time = arrival_time

    def set_leaving_time(self, leaving_time):
        self.leaving_time = leaving_time

    def service_demand(self, demand):
        self.demand = demand

    def get_demand(self):
        return self.demand


class MM1:

    def __init__(self, mu, lambd):
        self.mu = mu
        self.lambd = lambd

        self.array_arrival_time  = []
        self.array_start_service_time = []
        
        self.que_limit = 150
        self.num_in_q = 0

        self.total_num_of_arrived_demands = 0
        self.num_serviced_demand = 0
        self.lost_customers = 0

        self.current_time = 0
        self.arrival_time = expovariate(lambd)
        self.service_start_time = float('inf')
        self.leaving_time = float('inf')
        
        self.idle = 'idle' 
        self.busy = 'busy'
        self.channel_status = self.idle
        
        self.num_of_demands_that_immediately_start_served = 0
        self.mathematical_expectation_duration_stay = 0
        self.probability_free_channel = 0
        self.average_time_in_q = 0
        self.service_time = 0 
        self.sum_service_time = 0
        
        self.list_of_system_characteristics_for_dif_num_demands = []
        self.list_mathematical_expectation_duration_stay = []
        self.list_required_number_of_served_demand= []
        self.list_of_system_characteristics = []
        
        self.queue = Queue()
        self.demand = Demand()

    def arrive(self):

        self.total_num_of_arrived_demands +=1
        demand = Demand(self.arrival_time)
        self.array_arrival_time.append(self.current_time)
      
        if self.num_in_q <= self.que_limit:
            self.num_serviced_demand += 1

            if self.channel_status == self.busy:
                self.num_in_q+=1
            else:
                self.num_of_demands_that_immediately_start_served +=1
                self.service_start_time = self.current_time
        else:
            self.lost_customers+=1

        self.queue.put(demand)
        self.arrival_time += expovariate(self.lambd)

    def service(self):

        self.channel_status = self.busy
        self.num_in_q += 1
        self.array_start_service_time.append(self.current_time) 

        self.demand.service_demand(self.queue.get())
        service_start_time = expovariate(self.mu)
        self.leaving_time = self.current_time + service_start_time

        self.service_start_time = float('inf')

    def leave(self):

        demand = self.demand.get_demand()
        self.channel_status = self.idle
        self.num_in_q -= 1

        demand.set_leaving_time(self.current_time)
        self.service_time = demand.leaving_time - demand.arrival_time
        self.sum_service_time +=  self.service_time

        if not self.queue.empty():
            self.service_start_time = self.current_time

        self.leaving_time = float('inf')

    def update(self):
        self.mathematical_expectation_duration_stay = self.sum_service_time / self.total_num_of_arrived_demands
        self.list_mathematical_expectation_duration_stay.append(self.mathematical_expectation_duration_stay)
        service_time_for_each_demand  = [a-b for a, b in zip(self.array_start_service_time, self.array_arrival_time )]
        self.average_time_in_q = sum(service_time_for_each_demand) / self.total_num_of_arrived_demands
        self.probability_free_channel = self.num_of_demands_that_immediately_start_served  / self.total_num_of_arrived_demands

        self.list_of_system_characteristics.extend((self.num_serviced_demand,self.mathematical_expectation_duration_stay, self.average_time_in_q, self.probability_free_channel, self.lost_customers))
        self.list_of_system_characteristics_for_dif_num_demands = [self.list_of_system_characteristics[x:x + 5] for x in range(0, len(self.list_of_system_characteristics), 5)]

    def table(self):
        print()
        headers = ['Число обслуженных заявок', 'М.о длительности пребывания', 'Среднее время заявки в очереди', 'Вероятность застать систему свободной', 'Число необслуженных заявок']
        data = self.list_of_system_characteristics_for_dif_num_demands 
        print(tabulate.tabulate(data, headers, tablefmt='presto'))

    def graph(self):
        sns.set_theme(style="darkgrid")
        x = self.list_required_number_of_served_demand
        y = self.list_mathematical_expectation_duration_stay
        ax = sns.lineplot(x, y)
        ax.set(xlabel ='Число обслуженных заявок', ylabel ='М.о длительности пребывания')
        plt.show()

    def launch(self, required_number_of_served_demand):
        self.list_required_number_of_served_demand.append(required_number_of_served_demand)
        while self.num_serviced_demand < required_number_of_served_demand:
            self.current_time = min(self.arrival_time, self.service_start_time, self.leaving_time)
            if self.current_time == self.arrival_time:
                self.arrive()
            if self.current_time == self.service_start_time:
                self.service()
            if self.current_time == self.leaving_time:
                self.leave()
        self.update() 

mm1 = MM1(5, 1)
for required_number_of_served_demand in range(500, 6501, 1000):
    mm1.launch(required_number_of_served_demand)
mm1.table()
mm1.graph()


