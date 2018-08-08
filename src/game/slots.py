from enum import Enum, auto


class Slot(Enum):

    HEAD = auto()
    BODY = auto()
    RIGHT_HAND = auto()
    LEFT_HAND = auto()
    RANGED = auto()
    NECK = auto()
    FINGER = auto()

    HEAD_STR = 'head'
    BODY_STR = 'body'
    RIGHT_HAND_STR = 'right hand'
    LEFT_HAND_STR = 'left hand'
    RANGED_STR = 'ranged slot'
    NECK_STR = 'neck'
    FINGER_STR = 'finger'
