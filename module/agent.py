import itertools
from typing import List
import numpy as np
import random
from enum import Enum
import copy


class State(Enum):
    IN_PARK = 1
    OUT_OF_PARK = 2
    IN_QUEUE = 3
    ON_RIDE = 4


class Type(Enum):
    NAIVE = 1  # Target lowest q time
    RANDOM = 2  # Target max q time
    CRAZY = 3  # Target random
    GREEDY = 4  # Target closest
    SMART = 5  # Target in respect to distance and q time
    EXTRAPOLATE = 6  # Extrapolate q times and predic on travel time


class Agent:
    id_count = itertools.count()

    def __init__(self, position: tuple, attractions: List, queue_prob, commit_prob, view_range, group_size, type, visit_window) -> None:
        self.id = next(self.id_count)
        self.attractions = attractions
        self.position = np.array(position, dtype=np.float64)
        self.group_size = group_size
        self.visited = []
        self.recent_visits = []
        self.visit_window = visit_window
        self.proximity_decision = False
        self.queue_prob = queue_prob
        self.view_range = view_range
        self.commit_prob = commit_prob
        self.velocity = 1.42 * (11-group_size)/10  # Walking speed
        self.direction = np.array([0, 0], dtype=np.float64)
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

    def set_target(self, attraction):
        self.target = attraction
        self.expected_qtime = attraction.get_queue_time()

    def set_type(self, type: Type):
        if type == Type.RANDOM:
            self.commited = True
        else:
            self.commited = False

        self.type = type

    def set_state(self, state: State):
        if state == State.IN_PARK:
            attraction_picks = list(
                set(self.attractions) - set(self.recent_visits))
            self.update_target(attraction_picks)
        self.state = state

    def add_visited(self, attraction):  # Call when visited an attraction
        self.visited.append(attraction)
        if len(self.recent_visits) != self.visit_window:
            self.recent_visits.append(attraction)
        else:
            self.recent_visits.remove(self.recent_visits[0])
            self.recent_visits.append(attraction)

        self.set_state(State.IN_PARK)
        if self.type != Type.RANDOM:
            self.commited = False
        self.proximity_decision = False

    # Returns the attraction with the lowest queue time.

    def get_lq_attractions(self, attractions) -> List:
        lq_attractions = [attractions[0]]
        for i in range(1, len(attractions)):
            if attractions[i].get_queue_time() < lq_attractions[0].get_queue_time():
                lq_attractions = [attractions[i]]
            elif attractions[i].get_queue_time() == lq_attractions[0].get_queue_time():
                lq_attractions.append(attractions[i])

        return lq_attractions

    # Returns the attraction with the max queue time.
    def get_mq_attractions(self, attractions) -> List:
        mq_attractions = [attractions[0]]
        for i in range(1, len(attractions)):
            if attractions[i].get_queue_time() > mq_attractions[0].get_queue_time():
                mq_attractions = [attractions[i]]
            elif attractions[i].get_queue_time() == mq_attractions[0].get_queue_time():
                mq_attractions.append(attractions[i])

        return mq_attractions

    def update(self):
        if self.state == State.IN_PARK:
            if self.at_target():
                self.queue()
            elif not self.proximity_decision and self.target_in_view():
                if random.random() > self.queue_prob and self.target.get_queue_time_history()[-1] > self.expected_qtime*2:
                    attraction_picks = list(
                        (set(self.attractions) - set(self.recent_visits))-set([self.target]))
                    self.update_target(attraction_picks)  # Pick new target

                self.proximity_decision = True
            else:
                self.move()

    def queue(self) -> None:
        self.target.add_to_queue(self)
        self.set_state(State.IN_QUEUE)

    def move(self) -> None:
        attraction_picks = list(
            set(self.attractions) - set(self.recent_visits))
        if not self.commited:
            self.update_target(attraction_picks)
            if random.random() < self.commit_prob:
                self.commited = True
        self.position += self.direction * self.velocity

    def update_target(self, attractions: List) -> None:
        if len(attractions) == 1:
            self.set_target(attractions[0])
            direction = self.target.get_position() - self.position
            self.direction = direction / np.linalg.norm(direction)
            return

        if self.type == Type.NAIVE:
            lq_attractions = self.get_lq_attractions(attractions)
            distances = self.get_distances(lq_attractions)
            self.set_target(lq_attractions[distances.index(min(distances))])
        elif self.type == Type.CRAZY:
            mq_attractions = self.get_mq_attractions(attractions)
            distances = self.get_distances(mq_attractions)
            self.set_target(mq_attractions[distances.index(min(distances))])
        elif self.type == Type.RANDOM:
            self.set_target(random.choice(attractions))
        elif self.type == Type.GREEDY:
            distances = self.get_distances(attractions)
            self.set_target(attractions[distances.index(min(distances))])
        elif self.type == Type.SMART:
            # TODO pick attraction according to distance and qtime
            # ratio = 1/(a*travel_time + b*queue_time)
            a = 0.5
            b = 0.5
            distances = self.get_distances(attractions)
            travel_times = list(
                map(lambda distance: distance / self.velocity, distances))
            queue_times = list(
                map(lambda attraction: attraction.get_queue_time(), attractions))
            ratios = list(map(
                lambda element: 1/(a*element[0] + b*element[1]), zip(travel_times, queue_times)))
            self.set_target(attractions[ratios.index(max(ratios))])

        elif self.type == Type.EXTRAPOLATE:
            # picks attraction with the lowest future q according to the queue history
            distances = self.get_distances(attractions)
            expected_future_queue_times = [0]*len(distances)
            for i in range(len(distances)):
                travel_time = distances[i] / self.velocity
                expected_future_queue_times[i] = attractions[i].get_extrapolated_queue_time(
                    travel_time)

            shortest_idx = 0
            for i in range(1, len(attractions)):
                if expected_future_queue_times[i] < expected_future_queue_times[shortest_idx]:
                    shortest_idx = i
                elif expected_future_queue_times[i] == expected_future_queue_times[shortest_idx]:
                    # if they are equal, only set to i if i is closer
                    if distances[i] < distances[shortest_idx]:
                        shortest_idx = i

            self.set_target(attractions[shortest_idx])

        direction = self.target.get_position() - self.position
        self.direction = direction / np.linalg.norm(direction)

    def get_distances(self, attractions) -> List:
        distances = []
        for attraction in attractions:
            distances.append(np.linalg.norm(
                attraction.get_position() - self.position))
        return distances

    def at_target(self) -> bool:
        direction = self.target.get_position() - self.position
        # in radius of max velocity to prevent overshoot
        return np.linalg.norm(direction) < self.velocity

    def target_in_view(self) -> bool:
        direction = self.target.get_position() - self.position
        return np.linalg.norm(direction) < self.view_range

    def shallow_copy(self):
        copied_agent = copy.copy(self)
        del copied_agent.attractions
        del copied_agent.recent_visits
        del copied_agent.visit_window
        del copied_agent.proximity_decision
        del copied_agent.queue_prob
        del copied_agent.view_range
        del copied_agent.commit_prob
        del copied_agent.velocity
        del copied_agent.direction
        del copied_agent.expected_qtime
        del copied_agent.commited
        del copied_agent.target
        copied_agent.position = copy.copy(self.position)
        copied_agent.visited = copy.copy(self.visited)
        return copied_agent
