import libtcodpy as libtcod
from game.game_states import GameState
from gui.messages import Messages


class DeathFunctions:

    world = None

    @staticmethod
    def player_death(player_entity):
        Messages.new('You have died!', libtcod.red)
        player_entity.char = 'X'
        player_entity.color = libtcod.dark_red
        DeathFunctions.world.game_state = GameState.PLAYER_DEAD

    @staticmethod
    def monster_death(monster_entity):

        Messages.new('You have slain the ' + monster_entity.name + '!', libtcod.orange)

        monster_entity.char = 'x'
        monster_entity.color = libtcod.dark_red
        monster_entity.blocks = False
        monster_entity.fighter = None
        monster_entity.ai = None
        monster_entity.name = 'remains of ' + monster_entity.name
        monster_entity.send_to_back(DeathFunctions.world.objects)

        try:
            monster_entity.timeobj.release()
        except AttributeError:
            print('Tried to release ' + monster_entity.name + ' but no time component found!')



