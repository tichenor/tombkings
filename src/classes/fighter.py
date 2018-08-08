from game.action_type import ActionType
from game.event_handler import EventHandler
from logic.combat import Combat


class Fighter:

    def __init__(self, hp, defense, power, xp, armor, mana, magic, death_function=None, buff=[], lifesteal=0,
                 hp_regen=0, magic_resist=0, fighting=0, shielding=0, conjuring=0, archery=0, transmutations=0,
                 hexes=0, speed=100, evasion=0, accuracy=0, dmg_reduction=0, heal_kill=0, prof_restriction=[],
                 stunned=0, mana_regen=0):

        self.owner = None

        self.base_max_hp = hp
        self.hp = hp
        self.base_max_mana = mana
        self.mana = mana

        self.base_defense = defense
        self.base_power = power
        self.base_armor = armor
        self.base_magic = magic

        self.xp = xp
        self.death_function = death_function
        self.buff = []

        self.base_hp_regen = hp_regen
        self.base_mana_regen = mana_regen

        self.base_magic_resist = magic_resist
        self.base_lifesteal = lifesteal
        self.base_evasion = evasion
        self.base_accuracy = accuracy

        self.base_fighting = fighting
        self.base_shielding = shielding
        self.base_conjuring = conjuring
        self.base_archery = archery
        self.base_transmutations = transmutations
        self.base_hexes = hexes

        self.base_speed = speed
        self.base_dmg_reduction = dmg_reduction
        self.base_heal_kill = heal_kill

        self.prof_restriction = prof_restriction
        self.stunned = stunned

        # for mana regen after recent kill
        self.mana_incrementer = 0
        self.recent_kill_window = 120

        self.stealthiness = 0

    @property
    def power(self):
        bonus = 0
        if self.owner.inventory:
            bonus += sum(equipment.power_bonus for equipment in self.owner.inventory.get_all_equipped())
        bonus += sum(buff.power_bonus for buff in self.buff)
        return self.base_power + bonus

    @property
    def defense(self):
        bonus = 0
        if self.owner.inventory:
            bonus += sum(equipment.defense_bonus for equipment in self.owner.inventory.get_all_equipped())
        bonus += sum(buff.defense_bonus for buff in self.buff)
        return self.base_defense + bonus

    @property
    def max_hp(self):
        bonus = 0
        if self.owner.inventory:
            bonus += sum(equipment.max_hp_bonus for equipment in self.owner.inventory.get_all_equipped())
        bonus += sum(buff.max_hp_bonus for buff in self.buff)
        return self.base_max_hp + self.base_fighting + bonus

    @property
    def armor(self):
        bonus = 0
        if self.owner.inventory:
            bonus += sum(equipment.armor_bonus for equipment in self.owner.inventory.get_all_equipped())
        bonus += sum(buff.armor_bonus for buff in self.buff)
        return self.base_armor + bonus

    @property
    def max_mana(self):
        bonus = 0
        if self.owner.inventory:
            bonus += sum(equipment.max_mana_bonus for equipment in self.owner.inventory.get_all_equipped())
        bonus += sum(buff.max_mana_bonus for buff in self.buff)
        return self.base_max_mana + bonus

    @property
    def magic(self):
        bonus = 0
        if self.owner.inventory:
            bonus += sum(equipment.magic_bonus for equipment in self.owner.inventory.get_all_equipped())
        bonus += sum(buff.magic_bonus for buff in self.buff)
        return self.base_magic + bonus

    @property
    def lifesteal(self):
        bonus = 0
        if self.owner.inventory:
            bonus += sum(equipment.lifesteal_bonus for equipment in self.owner.inventory.get_all_equipped())
        bonus += sum(buff.lifesteal_bonus for buff in self.buff)
        return self.base_lifesteal + bonus

    @property
    def hp_regen(self):
        bonus = 0
        if self.owner.inventory:
            bonus += sum(equipment.hp_regen_bonus for equipment in self.owner.inventory.get_all_equipped())
        bonus += sum(buff.hp_regen_bonus for buff in self.buff)
        return self.base_hp_regen + bonus

    @property
    def magic_resist(self):
        bonus = 0
        if self.owner.inventory:
            bonus += sum(equipment.magic_resist_bonus for equipment in self.owner.inventory.get_all_equipped())
        bonus += sum(buff.magic_resist_bonus for buff in self.buff)
        return self.base_magic_resist + bonus

    @property
    def shielding(self):
        bonus = 0
        if self.owner.inventory:
            bonus += sum(equipment.shielding_bonus for equipment in self.owner.inventory.get_all_equipped())
        bonus += sum(buff.shielding_bonus for buff in self.buff)
        return self.base_shielding + bonus

    @property
    def fighting(self):
        bonus = 0
        if self.owner.inventory:
            bonus += sum(equipment.fighting_bonus for equipment in self.owner.inventory.get_all_equipped())
        bonus += sum(buff.fighting_bonus for buff in self.buff)
        return self.base_fighting + bonus

    @property
    def conjuring(self):
        bonus = 0
        if self.owner.inventory:
            bonus += sum(equipment.conjuring_bonus for equipment in self.owner.inventory.get_all_equipped())
        bonus += sum(buff.conjuring_bonus for buff in self.buff)
        return self.base_conjuring + bonus

    @property
    def archery(self):
        bonus = 0
        if self.owner.inventory:
            bonus += sum(equipment.archery_bonus for equipment in self.owner.inventory.get_all_equipped())
        bonus += sum(buff.archery_bonus for buff in self.buff)
        return self.base_archery + bonus

    @property
    def transmutations(self):
        bonus = 0
        if self.owner.inventory:
            bonus += sum(equipment.transmutations_bonus for equipment in self.owner.inventory.get_all_equipped())
        bonus += sum(buff.transmutations_bonus for buff in self.buff)
        return self.base_transmutations + bonus

    @property
    def hexes(self):
        bonus = 0
        if self.owner.inventory:
            bonus += sum(equipment.hexes_bonus for equipment in self.owner.inventory.get_all_equipped())
        bonus += sum(buff.hexes_bonus for buff in self.buff)
        return self.base_hexes + bonus

    @property
    def speed(self):
        bonus = 0
        if self.owner.inventory:
            bonus += sum(equipment.speed_bonus for equipment in self.owner.inventory.get_all_equipped())
        bonus += sum(buff.speed_bonus for buff in self.buff)
        return self.base_speed + bonus

    @property
    def dmg_reduction(self):
        bonus = 0
        if self.owner.inventory:
            bonus += sum(equipment.dmg_reduction_bonus for equipment in self.owner.inventory.get_all_equipped())
        bonus += sum(buff.dmg_reduction_bonus for buff in self.buff)
        return self.base_dmg_reduction + bonus

    @property
    def evasion(self):
        bonus = 0
        if self.owner.inventory:
            bonus += sum(equipment.evasion_bonus for equipment in self.owner.inventory.get_all_equipped())
        bonus += sum(buff.evasion_bonus for buff in self.buff)
        return self.base_evasion + bonus

    @property
    def accuracy(self):
        bonus = 0
        if self.owner.inventory:
            bonus += sum(equipment.accuracy_bonus for equipment in self.owner.inventory.get_all_equipped())
        bonus += sum(buff.accuracy_bonus for buff in self.buff)
        return self.base_accuracy + bonus

    @property
    def heal_kill(self):
        bonus = 0
        if self.owner.inventory:
            bonus += sum(equipment.heal_kill_bonus for equipment in self.owner.inventory.get_all_equipped())
        bonus += sum(buff.heal_kill_bonus for buff in self.buff)
        return self.base_heal_kill + bonus

    def take_damage(self, val):
        if self.dmg_reduction > 0:
            val -= self.dmg_reduction
        if val > 0:
            self.hp -= val
            if self.hp <= 0:
                f = self.death_function
                if f is not None:
                    EventHandler.add_death_event('death', (f, self.owner))

    def heal(self, val):
        self.hp += val
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def restore_mana(self, val):
        self.mana += val
        if self.mana > self.max_mana:
            self.mana = self.max_mana

    def melee_attack(self, target):
        result = Combat.melee_attack(self.owner, target)
        EventHandler.add_combat_event(ActionType.MELEE_COMBAT, (self.owner, target, result))

    def reset_kill_window(self):
        self.recent_kill_window = 120

    def already_buffed(self, buffname):
        for b in self.buff:
            if b.name == buffname:
                return True
        return False
