from enum import Enum
import numpy as np
import random

class Type(Enum):
    NAIVE = 1 # Target lowest q time 
    RANDOM = 2 # Target max q time
    CRAZY = 3 # Target random
    GREEDY = 4 # Target closest
    SMART = 5 # Target 
    EXTRAPOLATE = 6

class Behaviour:
    def __init__(self, type : Type, queue_prob : float) -> None:
        self.__type = type
        self.__queue_prob = queue_prob
        pass
    
    def get_queue_prob(self) -> None:
        return self.__queue_prob
        
    # Returns the attraction with the lowest queue time.
    def get_lq_attraction(self, attractions) -> None:
        min_index = 0
        for i in range(len(attractions)):
            if attractions[i].get_queue_time() < attractions[min_index].get_queue_time():
                min_index = i
                
        return attractions[min_index]

    # Returns the attraction with the max queue time.
    def get_mq_attraction(self, attractions) -> None:
        max_index = 0
        for i in range(len(attractions)):
            if attractions[i].get_queue_time() > attractions[max_index].get_queue_time():
                max_index = i
                
        return attractions[max_index]

    def new_target(self, agent, attractions) -> None:
        if self.__type == Type.NAIVE:
            agent.set_target(self.get_lq_attraction(attractions))
        elif self.__type == Type.CRAZY:
            agent.set_target(self.get_mq_attraction(attractions))
        elif self.__type == Type.RANDOM:
            agent.set_target(random.choice(attractions))
        elif self.__type == Type.GREEDY:
            # np.linalg.norm(b-a, axis=1) 
            # TODO pick closest attraction in attractions
            pass
        elif self.__type == Type.SMART:
            # TODO pick attraction according to distance and qtime
            pass
        elif self.__type == Type.EXTRAPOLATE:
            # TODO pick attraction with the lowest future q accoding to the history of the q:s
            pass

    def queue(self, attraction) -> None:
        if random.random() < self.__type.get_queue_prob():
            self.__target.add_to_queue(self)
        else:
            # TODO: Add what to do if the 
            pass

    def move(self, direction) -> None:
        pass