import itertools
from agentState import AgentState

class Agent:
    id_count = itertools.count()
    visibility = 2
    congestion_radius = 5
    velocity = 1.42 # Walking speed

    def __init__(self, position:tuple, agent_type, group_size = 1) -> None:
        self.id = next(self.id_count)
        self.__position = position
        self.__agent_type = agent_type     
        self.__state = AgentState.OUT_OF_PARK
        self.__group_size = group_size

    def get_group_size(self):
        return self.__group_size

    def queue(self):
        pass
    
    def move(self):
        pass

    def get_direction(self, attractions):
        for attraction in attractions:
            queue_time = len(attraction.queue)
            pass

    def act(self, attractions):
        if self.state == AgentState.IN_PARK:
            pass
        elif self.state == AgentState.IN_QUEUE:
            pass
        elif self.state == AgentState.OUT_OF_PARK:
            pass
        elif self.state == AgentState.ON_RIDE:
            pass
    