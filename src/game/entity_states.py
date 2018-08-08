from enum import Enum, auto


class EntityState(Enum):

    SLEEPING = auto()
    IDLE = auto()
    WANDERING = auto()
    CHASING = auto()
    RUNNING = auto()

