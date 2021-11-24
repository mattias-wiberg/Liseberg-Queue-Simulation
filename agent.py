import itertools
from typing import List
import numpy as np
import random
from enum import Enum

class State(Enum):
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

    def __init__(self, position:tuple, attractions : List, group_size = 1, type=Type.NAIVE, queue_prob = 1) -> None:
        self.id = next(self.id_count)
        self.attractions = attractions
        self.position = np.array(position, dtype=np.float64)
        self.group_size = group_size
        self.visited = []
        self.queue_prob = queue_prob
        self.velocity = 1.42 * (11-group_size)/10 # Walking speed
        self.direction = np.array([0,0], dtype=np.float64)
        self.set_type(type)
        self.set_state(State.IN_PARK)

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

    def set_type(self, type : Type):
        if type == Type.RANDOM:
            self.commited = True
        else:
            self.commited = False

        self.type = type

    def set_state(self, state : State):
        if state == State.IN_PARK:
            to_visit = list(set(self.attractions) - set(self.visited))
            self.update_target(to_visit)

        self.state = state

    def add_visited(self, attraction):
        self.visited.append(attraction)
        if len(self.attractions) - len(self.visited) == 0: # Visited all
            self.set_state(State.OUT_OF_PARK)
        else:
            self.set_state(State.IN_PARK)

    
    # Returns the attraction with the lowest queue time.
    def get_lq_attractions(self, attractions) -> List:
        lq_attractions = [attractions[0]]
        for i in range(1,len(attractions)):
            if attractions[i].get_queue_time() < lq_attractions[0].get_queue_time():
                lq_attractions = [attractions[i]]
            elif attractions[i].get_queue_time() == lq_attractions[0].get_queue_time():
                lq_attractions.append(attractions[i])

        return lq_attractions

    # Returns the attraction with the max queue time.
    def get_mq_attractions(self, attractions) -> List:
        mq_attractions = [attractions[0]]
        for i in range(1,len(attractions)):
            if attractions[i].get_queue_time() > mq_attractions[0].get_queue_time():
                mq_attractions = [attractions[i]]
            elif attractions[i].get_queue_time() == mq_attractions[0].get_queue_time():
                mq_attractions.append(attractions[i])

    def update(self):
        if self.state == State.IN_PARK:
            if self.at_target():
                self.queue()
            else:
                self.move()

    def queue(self) -> None:
        if random.random() < self.queue_prob:
            self.target.add_to_queue(self)
            self.set_state(State.IN_QUEUE)
        else:
            # TODO: Add what to do if not to queue
            pass
        
    def move(self) -> None:
        to_visit = list(set(self.attractions) - set(self.visited))
        if len(to_visit) != 0:
            if not self.commited:
                self.update_target(to_visit)
            self.position += self.direction * self.velocity
        else:
            self.set_state(State.OUT_OF_PARK)
        
         
    def update_target(self, attractions : List) -> None:
        if self.type == Type.NAIVE:
            lq_attractions = self.get_lq_attractions(attractions)
            distances = self.get_distances(lq_attractions)
            self.target = lq_attractions[distances.index(min(distances))]
        elif self.type == Type.CRAZY:
            mq_attractions = self.get_mq_attractions(attractions)
            distances = self.get_distances(mq_attractions)
            self.target = mq_attractions[distances.index(min(distances))]
        elif self.type == Type.RANDOM:
            self.target = random.choice(attractions)
        elif self.type == Type.GREEDY:
            distances = self.get_distances(attractions)
            self.target = attractions[distances.index(min(distances))]
            pass
        elif self.type == Type.SMART:
            # TODO pick attraction according to distance and qtime
            pass
        elif self.type == Type.EXTRAPOLATE:
            # TODO pick attraction with the lowest future q accoding to the history of the q:s
            pass
        
        direction = self.target.get_position() - self.position
        self.direction = direction / np.linalg.norm(direction)

    def get_distances(self, attractions) -> List:
        distances = []
        for attraction in attractions:
            distances.append(np.linalg.norm(attraction.get_position() - self.position))
        return distances

    def at_target(self) -> bool:
        direction = self.target.get_position() - self.position
        return np.linalg.norm(direction) < self.velocity # in radius of max velocity to prevent overshoot
