from enum import Enum
class AgentState(Enum):
    IN_PARK = 1
    OUT_OF_PARK = 2
    IN_QUEUE = 3
    ON_RIDE = 4