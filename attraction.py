from wagon import Wagon
import math

class Attraction:
    __check_back_limit = 5    # how far back to check in the q to fill up odd spots
    """
    queue_history = list(int)  # length delay, time history calculate w.r.t. ride time and size
    """

    def __init__(self, name:str, attraction_coeff:float, wagon_size:int, wagon_ride_time:float, n_wagons:int, position:tuple):
        self.__name = name
        self.__attraction_coeff = attraction_coeff
        self.__position = position

        self.__wagon_arrival_time = round(wagon_ride_time/n_wagons)
        self.__wagon_size = wagon_size
        self.__n_wagons = n_wagons
        self.__wagons = [Wagon() for i in range(n_wagons)]
        
        self.__queue = []
        self.__currently_riding = []
        self.__queue_time = 0

    def add_to_queue(self, agent):
        self.__queue.append(agent)

    def remove_from_queue(self, idx=0):
        return self.__queue.pop(idx)

    def advance_queue(self, global_time):
        if global_time % self.__wagon_arrival_time == 0:
            # let people off
            current_wagon_idx = (global_time/self.__wagon_arrival_time) % self.__n_wagons
            leaving_agent = current_wagon_idx.clear()
            # TODO: update the leaving agent's state
        else:
            # no arriving wagon so nothing to update
            return

        if len(self.__queue) == 0:
            # q is empty
            return 
        
        places_left = self.__wagon_size
        while places_left > 0:
            # fill up a wagon
            next_in_line_size = self.__queue[0].get_group_size()
            
            if places_left > next_in_line_size:
                # next in line has enough space on the ride, let them through
                agent = self.remove_from_queue()
                places_left -= next_in_line_size
                current_wagon_idx.add_agent(agent)
            else:
                # next in line does not have enough space on the ride,
                # check if there is anyone else behind in the q that can fill up the spots (up to self.__check_back_limit)
                for i in range(1, self.__check_back_limit):
                    if len(self.__queue) > i and self.__queue[i].get_group_size() < places_left:
                        places_left -= self.__queue[i].get_group_size()
                        self.remove_from_queue(i)
                # if the people in the back can't get on, send the wagon away
                places_left = 0





    

        


