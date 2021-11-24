from wagon import Wagon
import numpy as np

class Attraction:
    __check_back_limit = 5    # how far back to check in the q to fill up odd spots

    def __init__(self, name:str, position:tuple, wagon_size:int, wagon_ride_time:float, n_wagons:int, attraction_coeff:float = 1):
        self.__name = name
        self.__attraction_coeff = attraction_coeff
        self.__position = np.array(position, dtype=np.float64)

        self.__wagon_arrival_time = round(wagon_ride_time/n_wagons)
        self.__wagon_size = wagon_size
        self.__n_wagons = n_wagons
        self.__wagons = [Wagon() for i in range(n_wagons)]
        
        self.__queue = []
        self.__queue_time = 0
        self.__queue_time_history = []

    def get_queue_time(self):
        return self.__queue_time

    def get_position(self):
        return self.__position

    def add_to_queue(self, *agents):
        for agent in agents:
            self.__queue.append(agent)

    def get_queue_size(self):
        size = 0
        for agent in self.__queue:
            size += agent.get_group_size()
        return size

    def advance_queue(self, global_time):
        # this function modifies the internal variables
        if (global_time % self.__wagon_arrival_time) == 0:
            # let people off
            current_wagon_idx = int((global_time/self.__wagon_arrival_time) % self.__n_wagons)
            current_wagon = self.__wagons[current_wagon_idx]
            leaving_agent = current_wagon.clear()
            # TODO: update the leaving agent's state
        else:
            # no arriving wagon so nothing to update
            return

        if len(self.__queue) == 0:
            # queue is empty
            return 
        
        places_left = self.__wagon_size
        next_in_line_size = self.__queue[0].get_group_size()
        while places_left >= next_in_line_size:
            # fill up the wagon
            agent = self.__queue.pop(0)
            places_left -= agent.get_group_size()
            current_wagon.add_agent(agent)
            # TODO: update agent state
            
            if len(self.__queue) == 0:
                return
            
            next_in_line_size = self.__queue[0].get_group_size()
            
        if places_left == 0:
            return
        else:
            # check if anyone in the back can still fit on the ride (up to self.__check_back_limit)
            for i in range(1, self.__check_back_limit):
                if len(self.__queue) > i and self.__queue[i].get_group_size() <= places_left:
                    agent = self.__queue.pop(i)
                    places_left -= agent.get_group_size()
                    current_wagon.add_agent(agent)
                    # TODO: update agent state
                    if places_left == 0:
                        return


    def __fake_advance_queue(self, fake_global_time, fake_queue):
        # very similar to advance_queue but no internal variables are modified
        if len(fake_queue) == 0 or (fake_global_time % self.__wagon_arrival_time != 0):
            # queue is empty
            return fake_queue
        
        places_left = self.__wagon_size
        next_in_line_size = fake_queue[0].get_group_size()
        while places_left >= next_in_line_size:
            # fill up the wagon
            places_left -= next_in_line_size
            fake_queue.pop(0)
            
            if len(fake_queue) == 0:
                return fake_queue
            
            next_in_line_size = fake_queue[0].get_group_size()
            
        if places_left == 0:
            return fake_queue
        else:
            # check if anyone in the back can fit on the ride (up to self.__check_back_limit)
            for i in range(1, self.__check_back_limit):
                if len(fake_queue) > i and fake_queue[i].get_group_size() <= places_left:
                    places_left -= fake_queue.pop(i).get_group_size()
                    if places_left == 0:
                        return fake_queue

        return fake_queue


    def calc_queue_time(self, global_time):
        fake_queue = self.__queue.copy()
        fake_global_time = global_time

        # calculate nearest modulo time
        if (fake_global_time % self.__wagon_arrival_time) == 0:
            to_add = 0
        else:
            to_add = self.__wagon_arrival_time - (fake_global_time % self.__wagon_arrival_time)

        fake_global_time += to_add

        while len(fake_queue) > 0:
            self.__fake_advance_queue(fake_global_time, fake_queue)
            fake_global_time += self.__wagon_arrival_time

        self.__queue_time = fake_global_time - global_time
        self.__queue_time_history.append(self.__queue_time)
        #return self.__queue_time
        return fake_global_time


