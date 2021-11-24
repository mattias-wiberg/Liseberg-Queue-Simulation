from wagon import Wagon
import numpy as np
from agent import State

class Attraction:
    def __init__(self, name:str, position:tuple, wagon_size:int, wagon_ride_time:float, n_wagons:int, attraction_coeff:float = 1, 
                        check_back_limit:int = 5, delay:int = 0):        
        self.__name = name

        self.__position = np.array(position, dtype=np.float64)

        self.__wagon_size = wagon_size
        self.__wagon_arrival_time = round(wagon_ride_time/n_wagons)
        self.__n_wagons = n_wagons
        self.__wagons = [Wagon() for i in range(n_wagons)]

        self.__attraction_coeff = attraction_coeff  # (not implemented)
        self.__check_back_limit = check_back_limit  # how far back to check in the q to fill up odd spots
        
        self.__queue = []
        self.__queue_time_history = [0]
        self.__delay = delay
        self.__queue_size = 0   # takes agent group size into account # TODO: remove later (shouldn't be used anywhere)

    def get_position(self):
        return self.__position

    def add_to_queue(self, *agents):
        for agent in agents:
            self.__queue.append(agent)
            self.__queue_size += agent.get_group_size()

    def get_queue_size(self):
        # TODO: remove later (shouldn't be used anywhere)
        return self.__queue_size

    def advance_queue(self, global_time):
        # this function modifies the internal variables
        if (global_time % self.__wagon_arrival_time) == 0:
            # let people off
            current_wagon_idx = int((global_time/self.__wagon_arrival_time) % self.__n_wagons)
            current_wagon = self.__wagons[current_wagon_idx]
            leaving_agents = current_wagon.clear()
            if len(leaving_agents) > 0:
                # update the states of the leaving agents
                for agent in leaving_agents:
                    agent.add_visited(self)
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
            self.__queue_size -= agent.get_group_size()
            current_wagon.add_agent(agent)
            agent.set_state(State.ON_RIDE)
            
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
                    self.__queue_size -= agent.get_group_size()
                    current_wagon.add_agent(agent)
                    agent.set_state(State.ON_RIDE)
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

    def __set_queue_time(self, time):
        if self.__delay > 0:
            if len(self.__queue_time_history) == self.__delay:
                self.__queue_time_history.pop(0)
            self.__queue_time_history.append(time)
        else:
            self.__queue_time_history = [time]


    def calc_queue_time(self, global_time):
        if len(self.__queue) == 0:
            # there is no queue, so set the queue time to zero
            self.__set_queue_time(0)
            return
        
        fake_queue = self.__queue.copy()
        fake_global_time = global_time

        # calculate nearest modulo time
        if (fake_global_time % self.__wagon_arrival_time) == 0:
            # queue has just been advanced and a wagon filled meaning that we need 
            # to wait for the next wagon to arrive before we can advance the queue 
            to_add = self.__wagon_arrival_time
        else:
            to_add = self.__wagon_arrival_time - (fake_global_time % self.__wagon_arrival_time)

        fake_global_time += to_add

        # advance the queue until it is empty
        while len(fake_queue) > 0:
            self.__fake_advance_queue(fake_global_time, fake_queue)
            fake_global_time += self.__wagon_arrival_time

        queue_time = fake_global_time - global_time
        self.__set_queue_time(queue_time)
        

    def get_queue_time(self):
        return self.__queue_time_history[0]
