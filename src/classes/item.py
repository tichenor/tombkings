import libtcodpy as libtcod
from game.event_handler import EventHandler

from gui.messages import Messages
from logic.player_actions import ActionType


class Item:

    def __init__(self, spellname=None, use_function=None, material=False):

        self.owner = None

        self.spellname = spellname
        self.use_function = use_function
        self.material = material
        self.description = ''

    def picked_up(self, entity_picker, objects):
        assert entity_picker.inventory is not None, 'cannot pick up items without an inventory'
        if len(entity_picker.inventory) >= 26:
            EventHandler.add_inventory_event(ActionType.PICK_UP_FAIL, (self.owner, entity_picker))
            return ActionType.PICK_UP_FAIL
        else:
            entity_picker.inventory.items.append(self.owner)
            objects.remove(self.owner)
            EventHandler.add_inventory_event(ActionType.PICK_UP_GAIN, (self.owner, entity_picker))
            return ActionType.PICK_UP_GAIN

    def use(self, player):
        if self.owner.equipment:
            if not self.owner.equipment.prof_restriction:
                self.owner.equipment.toggle_equip()
            elif player.prof not in self.owner.equipment.prof_restriction:
                Messages.new('You cannot make use of this item!', libtcod.red)
            else:
                self.owner.equipment.toggle_equip()
        elif self.use_function is None:
            Messages.new('The ' + self.owner.name + ' cannot be used.')
        elif self.use_function() != 'cancelled':
            self.owner.inventory.items.remove(self.owner)
        elif self.spellname is not None:
            raise NotImplementedError('append_spell(spellname) not implemented')

    def drop(self, player):
        self.owner.inventory.items.remove(self.owner)
        self.owner.x = player.x
        self.owner.y = player.y
        youdroppeda = 'You dropped a'
        if self.owner.name[0] in 'aeiouAEIOU':
            youdroppeda += 'n '
        else:
            youdroppeda += ' '
        if self.owner.equipment:
            self.owner.equipment.dequip()
        Messages.new(youdroppeda + self.owner.name + '.', libtcod.yellow)

    def inspect(self):
        if self.owner.equipment:
            item = self.owner.equipment
            stats_list = []
            if item.power_bonus != 0:
                stats_list.append(str(item.power_bonus) + ' Power')
            if item.defense_bonus != 0:
                stats_list.append(str(item.defense_bonus) + ' Defense')
            if item.armor_bonus != 0:
                stats_list.append(str(item.armor_bonus) + ' AC')
            if item.magic_bonus != 0:
                stats_list.append(str(item.magic_bonus) + ' Magic')
            if item.max_hp_bonus != 0:
                stats_list.append(str(item.max_hp_bonus) + ' Max HP')
            if item.max_mana_bonus != 0:
                stats_list.append(str(item.max_mana_bonus) + ' Max Mana')
            if item.fighting_bonus != 0:
                stats_list.append(str(item.fighting_bonus) + ' Fighting')
            if item.shielding_bonus != 0:
                stats_list.append(str(item.shielding_bonus) + ' Shielding')
            if item.conjuring_bonus != 0:
                stats_list.append(str(item.conjuring_bonus) + ' Conjuring')
            if item.archery_bonus != 0:
                stats_list.append(str(item.archery_bonus) + ' Archery')
            if item.hexes_bonus != 0:
                stats_list.append(str(item.hexes_bonus) + ' Hexes')
            if item.evasion_bonus != 0:
                stats_list.append(str(item.evasion_bonus) + ' Evasion')
            if item.accuracy_bonus != 0:
                stats_list.append(str(item.accuracy_bonus) + ' Accuracy')
            if item.speed_bonus != 0:
                stats_list.append(str(item.speed_bonus) + ' Speed')
            if item.dmg_reduction_bonus != 0:
                stats_list.append('all physical damage taken reduced by ' + str(item.dmg_reduction_bonus))
            if item.heal_kill_bonus != 0:
                stats_list.append('chance to restore health or mana on kill')
            if item.magic_resist_bonus != 0:
                stats_list.append(str(item.magic_resist_bonus*100) + ' %% magic Resistance')
            if item.lifesteal_bonus != 0:
                stats_list.append(str(item.lifesteal_bonus) + ' lifesteal')

            string = ', '.join(stats_list)
        else:
            string = ''

            youseea = 'You see a'
        if self.owner.name[0] in 'aeiouAEIOU':
            youseea += 'n '
        else:
            youseea += ' '
        if string != '':
            text = youseea + self.owner.name + '. ' + self.description + ' It yields ' + string + '.'
        else:
            text = youseea + self.owner.name + '. ' + self.description
            Messages.new(text, libtcod.light_gray)
