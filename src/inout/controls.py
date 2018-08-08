import libtcodpy as libtcod

from game.game_states import GameState
from inout.render_functions import RenderFunctions
from logic.player_actions import PlayerActions


class Controls:

    @staticmethod
    def handle_keys(key, world):
        if world.game_state == GameState.PLAYING:
            return Controls.handle_keys_playing(key, world)

    @staticmethod
    def handle_keys_playing(key, world):

        if key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
            return PlayerActions.move_or_attack(0, -1, world.objects, world.player, world.tilemap)
        elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
            return PlayerActions.move_or_attack(0, 1, world.objects, world.player, world.tilemap)
        elif key.vk == libtcod.KEY_LEFT or key.vk == libtcod.KEY_KP4:
            return PlayerActions.move_or_attack(-1, 0, world.objects, world.player, world.tilemap)
        elif key.vk == libtcod.KEY_RIGHT or key.vk == libtcod.KEY_KP6:
            return PlayerActions.move_or_attack(1, 0, world.objects, world.player, world.tilemap)
        elif key.vk == libtcod.KEY_HOME or key.vk == libtcod.KEY_KP7:
            return PlayerActions.move_or_attack(-1, -1, world.objects, world.player, world.tilemap)
        elif key.vk == libtcod.KEY_PAGEUP or key.vk == libtcod.KEY_KP9:
            return PlayerActions.move_or_attack(1, -1, world.objects, world.player, world.tilemap)
        elif key.vk == libtcod.KEY_END or key.vk == libtcod.KEY_KP1:
            return PlayerActions.move_or_attack(-1, 1, world.objects, world.player, world.tilemap)
        elif key.vk == libtcod.KEY_PAGEDOWN or key.vk == libtcod.KEY_KP3:
            return PlayerActions.move_or_attack(1, 1, world.objects, world.player, world.tilemap)

        elif key.vk == libtcod.KEY_KP5:
            return PlayerActions.wait()

        elif key.vk == libtcod.KEY_TAB:
            PlayerActions.attack_closest(world.objects, world.player, world.fov_map)

        else:
            key_char = chr(key.c)

            if key_char == 'g':
                return PlayerActions.pick_up(world.player, world.objects)

            return None


