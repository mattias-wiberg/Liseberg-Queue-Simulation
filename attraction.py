from numpy.testing._private.utils import raises
from wagon import Wagon
import numpy as np
from agent import State
import copy

class Attraction:
    def __init__(self, name:str, position:tuple, wagon_size:int, wagon_ride_time:float, n_wagons:int, attraction_coeff:float = 1, 
                        check_back_limit:int = 5, delay:int = 0, extrapolate_pts:int = 2):        
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

        if extrapolate_pts < 2:
            raise Exception("__init__ in attraction.py: extrapolate_pts argument is less than 2. Cannot extrapolate from less than two points.")
        else:
            self.__extrapolate_pts = extrapolate_pts    # how many points to extrapolate from
        self.__extrapolated_queue_time_polynomial = np.polyfit(x=[1,2], y=[0,0], deg=1)
        self.__global_time = 1  # used in get_extrapolated_queue_time to calculate the future time

    def get_name(self):
        return self.__name

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

    def __extrapolate_queue_time(self, global_time):
        if len(self.__queue_time_history) == 1:
            # only one point (the initial zero), so cannot extrapolate from only one point
            return
        
        idx_start_pt = len(self.__queue_time_history) - self.__delay - self.__extrapolate_pts 
        idx_end_pt = len(self.__queue_time_history) - self.__delay

        if idx_start_pt < 0:
            pts = self.__queue_time_history
        else:
            pts = self.__queue_time_history[idx_start_pt:idx_end_pt]

        x_vals = list(range(global_time - len(pts) + 1, global_time + 1))
        self.__extrapolated_queue_time_polynomial = np.polyfit(x_vals, pts, deg=1)
        self.__global_time = global_time

    def get_extrapolated_queue_time(self, travel_time):
        future_time = self.__global_time + travel_time  # set by __extrapolate_queue_time
        future_queue_time = np.polyval(self.__extrapolated_queue_time_polynomial, future_time)
        if future_queue_time < 0:
            future_queue_time = 0
        return future_queue_time

    def calc_queue_time(self, global_time):
        if len(self.__queue) == 0:
            # there is no queue, so set the queue time to zero
            self.__queue_time_history.append(0)
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
            if len(fake_queue) != 0:
                fake_global_time += self.__wagon_arrival_time

        queue_time = fake_global_time - global_time
        self.__queue_time_history.append(queue_time)
        self.__extrapolate_queue_time(global_time)

    def get_queue_time(self):
        # 0: oldest queue time
        # -1: newest queue time (just appended)
        if len(self.__queue_time_history) - 1 - self.__delay < 0:
            # if history is not long enough yet, return the oldest value 
            return self.__queue_time_history[0]
        else:
            # newest - delay
            return self.__queue_time_history[len(self.__queue_time_history) - 1 - self.__delay]

    def get_avg_queue_time(self):
        return sum(self.__queue_time_history) / len(self.__queue_time_history)

    def get_queue_time_history(self):
        return self.__queue_time_history

    def get_num_agents(self):
        # for plotting purposes: count all the agents in the wagons and the queue
        agents_in_queue = 0
        for agent in self.__queue:
            agents_in_queue += agent.get_group_size()
        
        agents_in_wagons_count = 0
        for wagon in self.__wagons:
            for agent in wagon.agents_in_wagon:
                agents_in_wagons_count += agent.get_group_size()

        return (agents_in_queue + agents_in_wagons_count)
    
    def get_copied_wagons(self):
        new_wagons = []
        for iWagon in range(len(self.__wagons)):
            agents_in_wagon_list = []
            for jAgent in range(len(self.__wagons[iWagon].agents_in_wagon)):
                agents_in_wagon_list.append(copy.copy(self.__wagons[iWagon].agents_in_wagon[jAgent]))
            new_wagon = Wagon()
            new_wagon.agents_in_wagon = copy.copy(agents_in_wagon_list)
            new_wagons.append(new_wagon)
        return new_wagons

    def get_shallow_copy(self):
        copied_attraction = copy.copy(self)
        copied_attraction.__wagons = self.get_copied_wagons()
        copied_attraction.__queue = copy.copy(self.__queue)
        return copied_attraction

