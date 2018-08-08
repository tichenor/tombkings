from enum import Enum, auto


class GameState(Enum):

    PLAYING = auto()
    PLAYER_DEAD = auto()
    ENEMY_TURN = auto()
    SUBMENU = auto()
    MENU = auto()
