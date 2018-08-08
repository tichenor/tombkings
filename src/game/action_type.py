from enum import Enum, auto


class ActionType(Enum):

    MOVE = auto()
    WAIT = auto()
    MELEE_COMBAT = auto()
    RANGED_COMBAT = auto()

    PICK_UP_FAIL = auto()
    PICK_UP_GAIN = auto()
