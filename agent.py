import itertools
import numpy as np
import random
from enum import Enum

class AgentState(Enum):
    IN_PARK = 1
    OUT_OF_PARK = 2
    IN_QUEUE = 3
    ON_RIDE = 4

class Type(Enum):
    NAIVE = 1 # Target lowest q time 
    RANDOM = 2 # Target max q time
    CRAZY = 3 # Target random
    GREEDY = 4 # Target closest
    SMART = 5 # Target in respect to distance and q time
    EXTRAPOLATE = 6 # Extrapolate q times and predic on travel time

class Agent:
    id_count = itertools.count()
    visibility = 20
    congestion_radius = 5
    velocity = 1.42 # Walking speed

    def __init__(self, position:tuple, attractions, group_size = 1, type=Type.NAIVE, queue_prob = 1) -> None:
        self.id = next(self.id_count)
        self.position = np.array(position, dtype=np.float64)
        self.state = AgentState.IN_PARK
        self.group_size = group_size
        self.visited = []
        self.queue_prob = queue_prob
        self.type = type
        self.direction = np.array([0,0], dtype=np.float64)
        self.update_target(attractions)

    def get_queue_prob(self) -> None:
        return self.queue_prob
        
    def get_position(self):
        return self.position

    def get_state(self):
        return self.state

    def get_id(self):
        return self.id

    def get_group_size(self):
        return self.group_size

    def set_state(self, state : AgentState):
        self.state = state

    def add_visited(self, attraction):
        self.visited.append(attraction)

    
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

    def update(self, attractions):
        if self.state == AgentState.IN_PARK:
            if self.at_target():
                self.queue()
            else:
                self.move(attractions)

    def queue(self) -> None:
        if random.random() < self.queue_prob:
            self.target.add_to_queue(self)
            self.state = AgentState.IN_QUEUE
        else:
            # TODO: Add what to do if not to queue
            pass
        
    def move(self, attractions) -> None:
        self.update_target(attractions)
        self.position += self.direction * self.velocity
        
         
    def update_target(self, attractions) -> None:
        if self.type == Type.NAIVE:
            self.target = self.get_lq_attraction(attractions)
        elif self.type == Type.CRAZY:
            self.target = self.get_mq_attraction(attractions)
        elif self.type == Type.RANDOM:
            self.target = random.choice(attractions)
        elif self.type == Type.GREEDY:
            # np.linalg.norm(b-a, axis=1) 
            # TODO pick closest attraction in attractions
            pass
        elif self.type == Type.SMART:
            # TODO pick attraction according to distance and qtime
            pass
        elif self.type == Type.EXTRAPOLATE:
            # TODO pick attraction with the lowest future q accoding to the history of the q:s
            pass
        
        direction = self.target.get_position() - self.position
        self.direction = direction / np.linalg.norm(direction)

    def at_target(self) -> bool:
        direction = self.target.get_position() - self.position
        return np.linalg.norm(direction) < self.velocity # in radius of max velocity to prevent overshoot
