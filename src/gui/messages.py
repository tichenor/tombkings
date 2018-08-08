import textwrap

import libtcodpy as libtcod
from loaders.constants import Constants
from logic.combat import CombatResults
from game.action_type import ActionType


class Messages:

    game_msgs = []

    @staticmethod
    def new(text, color=libtcod.white):
        new_lines = textwrap.wrap(text, Constants.consts['MSG_WIDTH'])
        for line in new_lines:
            if len(Messages.game_msgs) == Constants.consts['MSG_HEIGHT']:
                del Messages.game_msgs[0]
            Messages.game_msgs.append((line, color))

    @staticmethod
    def new_combat_msg(action, attacker, defender, result):

        if attacker.isplayer:
            a_name = 'you'
        else:
            a_name = 'the ' + attacker.name

        if defender.isplayer:
            d_name = 'you'
        else:
            d_name = 'the ' + defender.name

        r_text = ''
        col = libtcod.white

        if action == ActionType.MELEE_COMBAT:

            if result == CombatResults.HIT:

                if attacker.isplayer:
                    r_text = a_name.capitalize() + ' attack and hit ' + d_name + '.'
                else:
                    r_text = a_name.capitalize() + ' attacks and hits ' + d_name + '.'

            elif result == CombatResults.MISS:

                suffix = ''
                if libtcod.random_get_int(0, 0, 100) < 20:
                    suffix = ' closely'
                if attacker.isplayer:
                    r_text = a_name.capitalize() + ' attack but miss ' + d_name + suffix + '.'
                else:
                    r_text = a_name.capitalize() + ' attacks but misses ' + d_name + suffix + '.'

            elif result == CombatResults.BLOCK:

                if attacker.isplayer:
                    r_text = a_name.capitalize() + ' attack but ' + d_name + ' blocks.'
                elif defender.isplayer:
                    r_text = a_name.capitalize() + ' attacks but ' + d_name + ' block.'
                else:
                    r_text = a_name.capitalize() + ' attacks but ' + d_name + ' blocks.'

            elif result == CombatResults.ARMOR:

                if attacker.isplayer:
                    r_text = a_name.capitalize() + ' attack ' + d_name + ' but do no damage.'
                else:
                    r_text = a_name.capitalize() + ' attacks ' + d_name + ' but does no damage.'

        elif action == ActionType.RANGED_COMBAT:

            if result == CombatResults.HIT:

                if attacker.isplayer:
                    r_text = a_name.capitalize() + ' shoot and hit ' + d_name + '.'
                else:
                    r_text = a_name.capitalize() + ' shoots and hits ' + d_name + '.'

            elif result == CombatResults.MISS:

                suffix = ''
                if libtcod.random_get_int(0, 0, 100) < 20:
                    suffix = ' closely'
                if attacker.isplayer:
                    r_text = a_name.capitalize() + ' shoot but miss ' + d_name + suffix + '.'
                else:
                    r_text = a_name.capitalize() + ' shoots but misses ' + d_name + suffix + '.'

            elif result == CombatResults.BLOCK:

                if attacker.isplayer:
                    r_text = a_name.capitalize() + ' shoot but ' + d_name + ' blocks the projectile.'
                elif defender.isplayer:
                    r_text = a_name.capitalize() + ' shoots but ' + d_name + ' block.'
                else:
                    r_text = a_name.capitalize() + ' shoots but ' + d_name + ' blocks.'

            elif result == CombatResults.ARMOR:

                if attacker.isplayer:
                    r_text = a_name.capitalize() + ' shoot and hit ' + d_name + ' but do no damage.'
                else:
                    r_text = a_name.capitalize() + ' shoots and hits ' + d_name + ' but does no damage.'

        if r_text != '':
            Messages.new(r_text, col)

    @staticmethod
    def new_item_msg(action, player, item_entity):
        r_text = ''
        col = libtcod.white
        if action == ActionType.PICK_UP_FAIL:
            r_text = 'Inventory is full, unable to pick up ' + item_entity.name + '.'
            col = libtcod.yellow
        elif action == ActionType.PICK_UP_GAIN:
            r_text = 'You picked up a ' + item_entity.name + '.'
            col = libtcod.green
        if r_text != '':
            Messages.new(r_text, col)
