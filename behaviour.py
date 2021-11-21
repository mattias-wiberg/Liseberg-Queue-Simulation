from enum import Enum

class Type(Enum):
    NAIVE = 1

class Behaviour:
    def __init__(self, type : Type, queue_prob : float) -> None:
        self.__type = type
        pass
    
    def get_lowest_queue(self, attractions):
        min_index = 0
        for i in range(len(attractions)):
            if attractions[i].get_queue_time() < attractions[min_index].get_queue_time():
                min_index = i
                
        return attractions[min_index]

    def get_direction(self, agent, attractions):
        if self.type == Type.NAIVE:
            

    def move(self, direction):
        pass