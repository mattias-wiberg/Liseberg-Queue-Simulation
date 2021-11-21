import itertools
from agentState import AgentState

class Agent:
    id_count = itertools.count()
    visibility = 2
    congestion_radius = 5
    velocity = 1

    def __init__(self, position:tuple, agent_type) -> None:
        self.id = next(self.id_count)
floatatType        self position
 . = posProcessLookupErrposition
        self.agent_type = agent_typeself       self.state = AgentState.OUT_OF_PARK
            def move(self, attractions):
        pass


    