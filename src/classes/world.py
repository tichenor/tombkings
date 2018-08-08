import libtcodpy as libtcod
from game.event_handler import EventHandler
from game.game_states import GameState
from gui.messages import Messages
from inout.render_functions import RenderFunctions
from loaders.initializer import Initializer
from game.action_type import ActionType
from loaders.map_maker import MapMaker


class World:

    def __init__(self, race, prof):
        self.player = Initializer.init_player(race, prof, 'player')
        self.objects = [self.player]
        self.tilemap = Initializer.init_tilemap()
        self.fov_map = None
        self.__game_time = 0
        self.dungeon_level = 1
        self.fov_recompute = True
        self.debug = False
        self.game_state = GameState.PLAYING

    def update(self, action):

        if action in (ActionType.MELEE_COMBAT, ActionType.RANGED_COMBAT):
            self.game_state = GameState.ENEMY_TURN

        elif action == ActionType.PICK_UP_GAIN:
            self.game_state = GameState.ENEMY_TURN

        elif action == ActionType.MOVE:
            self.game_state = GameState.ENEMY_TURN
            RenderFunctions.compute_fov(self)

        # event updates and messages

        EventHandler.update()

        # enemy turn

        if self.game_state == GameState.ENEMY_TURN:
            for o in self.objects:
                if o.fighter and o.ai and o.timeobj:
                    o.timeobj.tick()
            self.__game_time += 1
            self.game_state = GameState.PLAYING

