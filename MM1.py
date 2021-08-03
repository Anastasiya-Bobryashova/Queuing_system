from queue import Queue
from random import expovariate
import matplotlib.pyplot as plt


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

        self.number_demand = 0
        self.num_serviced_demand = 0
        self.num_in_q = 0

        self.demand_not_serviced = []
        self.service_time_array = []
        self.received_demand = []
        self.gone_demand = []

        self.average_time = 0
        self.service_time = 0 
        self.sum_service_times = 0
        
        self.current_time = 0
        self.arrival_time = expovariate(lambd)
        self.service_start_time = float('inf')
        self.leaving_time = float('inf')

        self.idle = 'idle' 
        self.busy = 'busy'
        self.channel_status = self.idle
        
        self.queue = Queue()
        self.demand = Demand()


    def arrive(self):
        
        self.num_serviced_demand += 1
        self.number_demand += 1
        self.received_demand.append(self.number_demand)
        demand = Demand(self.arrival_time)

        print("Требование", "'", self.number_demand,"'", "поступило в", self.current_time)

        if self.queue.empty() and self.channel_status == self.idle:
            self.service_start_time = self.current_time

        self.queue.put(demand)
        self.arrival_time += expovariate(self.lambd)

    def service(self):
        self.channel_status = self.busy
        self.demand.service_demand(self.queue.get())
        service_start_time = expovariate(self.mu)
        self.leaving_time = self.current_time + service_start_time
        self.num_in_q += 1

        print("Количество требований в очереди", self.num_in_q)
        print("Требование", "'", self.number_demand, "'",  "начало обслуживаться в", self.current_time)

        self.demand.demand.service_start_time = self.current_time
        self.service_start_time = float('inf')

    def leave(self):
        
        
        demand = self.demand.get_demand()
        self.gone_demand.append(self.number_demand)
        self.channel_status = self.idle
        self.num_in_q -= 1

        print("Требование","'", self.number_demand,"'", "покинуло систему в", self.current_time)
        print("Обслужено", self.num_serviced_demand, "треб.")

        demand.set_leaving_time(self.current_time)
        self.sum_service_times += demand.leaving_time - demand.arrival_time
        self.service_times = demand.leaving_time - demand.arrival_time
        self.service_time_array.append(self.service_times)

        print("Требование","'", self.number_demand,"'", "обслуживалось",self.service_times, "секунд")
        
        if not self.queue.empty():
            self.service_start_time = self.current_time
        self.leaving_time = float('inf')

    def show(self):
        plt.plot(self.gone_demand, self.service_time_array)
        plt.title('Связь между требованием и временем обслуживания')
        plt.xlabel('Число обслуженных требований')
        plt.ylabel('Время обслуживания')
        plt.grid()
        plt.show()

    def update(self):
        self.average_time = self.sum_service_times / self.num_serviced_demand

    def report(self):
        print()
        print("Время завершения моделирования: ", self.current_time)        
        print("Среднее время обслуживания: ", self.average_time)
        print('Самое длительное обслуживание длилось', max(self.service_time_array ))
        print('Мат.ожидание длительности пребывания', self.average_time)

    def main(self, required_number_of_served_demand):
        while self.num_serviced_demand < required_number_of_served_demand:
            self.current_time = min(self.arrival_time, self.service_start_time, self.leaving_time)
            if self.current_time == self.arrival_time:
                self.arrive()
            if self.current_time == self.service_start_time:
                self.service()
            if self.current_time == self.leaving_time:
                self.leave()
        self.update() 
        self.report()
   
mm1 = MM1(2,1)
for required_number_of_served_demand in range(500, 6501, 1000):
    mm1.main(required_number_of_served_demand)
mm1.show()
