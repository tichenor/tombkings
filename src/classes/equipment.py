import libtcodpy as libtcod

from gui.messages import Messages


class Equipment:

    def __init__(self, slot, slot_str, max_hp_bonus=0, max_mana_bonus=0, power_bonus=0, defense_bonus=0, armor_bonus=0,
                 magic_bonus=0, lifesteal_bonus=0, damage_amp_bonus=0, magic_resist_bonus=0, fighting_bonus=0,
                 shielding_bonus=0, conjuring_bonus=0, archery_bonus=0, transmutations_bonus=0, hexes_bonus=0,
                 evasion_bonus=0, accuracy_bonus=0, speed_bonus=0, dmg_reduction_bonus=0, heal_kill_bonus=0,
                 prof_restriction=None, is_equipped=False):

        self.owner = None

        self.slot = slot
        self.slot_str = slot_str
        self.max_hp_bonus = max_hp_bonus
        self.max_mana_bonus = max_mana_bonus
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.armor_bonus = armor_bonus
        self.magic_bonus = magic_bonus
        self.lifesteal_bonus = lifesteal_bonus
        self.damage_amp_bonus = damage_amp_bonus
        self.magic_resist_bonus = magic_resist_bonus
        self.fighting_bonus = fighting_bonus
        self.shielding_bonus = shielding_bonus
        self.conjuring_bonus = conjuring_bonus
        self.archery_bonus = archery_bonus
        self.transmutations_bonus = transmutations_bonus
        self.hexes_bonus = hexes_bonus
        self.evasion_bonus = evasion_bonus
        self.accuracy_bonus = accuracy_bonus
        self.speed_bonus = speed_bonus
        self.dmg_reduction_bonus = dmg_reduction_bonus
        self.heal_kill_bonus = heal_kill_bonus
        if prof_restriction is None:
            prof_restriction = []
        self.prof_restriction = prof_restriction
        self.is_equipped = is_equipped

    def toggle_equip(self):
        if self.is_equipped:
            self.dequip()
        else:
            self.equip()

    def equip(self):
        assert self.owner.inventory is not None, 'cannot equip item without an inventory!'
        old_equip = self.owner.inventory.get_equipped_in_slot(self.slot)
        if old_equip is not None:
            old_equip.dequip()
        self.is_equipped = True
        Messages.new('Equipped ' + self.owner.name + ' on ' + self.slot_str + '.', libtcod.light_green)

    def dequip(self):
        if not self.is_equipped:
            return
        self.is_equipped = False
        Messages.new('Dequipped ' + self.owner.name + ' from ' + self.slot_str + '.', libtcod.light_yellow)
