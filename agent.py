import itertools
from agentState import AgentState
import numpy as np
import random

class Agent:
    id_count = itertools.count()
    visibility = 20
    congestion_radius = 5
    velocity = 1.42 # Walking speed

    def __init__(self, position:tuple, behaviour, group_size = 1) -> None:
        self.__id = next(self.id_count)
        self.__position = position
        self.__behaviour = behaviour     
        self.__state = AgentState.IN_PARK
        self.__group_size = group_size
        self.__visited = []

    def get_position(self):
        return self.__position

    def get_id(self):
        return self.__id

    def get_group_size(self):
        return self.__group_size
    
    def set_target(self, attraction):
        self.__target = attraction
        direction = attraction.get_position() - self.__position
        direction = direction / np.linalg.norm(direction)

    def set_state(self, state : AgentState):
        self.__state = state

    def add_visited(self, attraction):
        self.__visited.append(attraction)

    def update(self):
        if self.__state == AgentState.IN_PARK:
            if self.at_target(self):
                self.__behaviour.queue(self.__target)
            self.__behaviour.move()
                
        pass

    def at_target(self) -> bool:
        direction = self.__target.get_position() - self.__position
        return np.linalg.norm(direction) < self.velocity # in radius of max velocity to prevent overshoot
