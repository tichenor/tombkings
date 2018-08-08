from enum import Enum, auto

import libtcodpy as libtcod
from game.slots import Slot


class Combat:

    @staticmethod
    def melee_attack(attacker, defender):
        # miss chance
        if Combat.melee_hit_roll(attacker, defender):
            if Combat.melee_block_roll(attacker, defender):
                # damage spread
                i, d = divmod(attacker.fighter.power / 3, 1)
                # raw damage
                attacker_power = attacker.fighter.power * (0.8 + 0.05 * attacker.fighter.power)
                raw_damage = attacker_power + libtcod.random_get_int(0, int(-i), int(i))
                # amplification sources
                amp = 0
                # armor reduction
                die = libtcod.random_get_int(0, 0, 20)
                if die + defender.fighter.fighting > 2 * attacker.fighter.power:
                    # target is strong defender
                    reduction = 0.6 * defender.fighter.armor + 0.03 * defender.fighter.shielding
                else:
                    reduction = 0.35 * defender.fighter.armor + 0.03 * defender.fighter.shielding
                # damage after modifiers
                damage = int(round(raw_damage - reduction) * (1 + amp))
                if damage > 0:
                    defender.fighter.take_damage(damage)
                    if attacker.fighter.lifesteal > 0:
                        attacker.fighter.heal(attacker.fighter.lifesteal)
                    return CombatResults.HIT
                else:
                    return CombatResults.ARMOR

            else:
                return CombatResults.BLOCK
        else:
            return CombatResults.MISS

    @staticmethod
    def ranged_attack(attacker, defender):
        if Combat.ranged_hit_roll(attacker, defender):
            if Combat.ranged_block_roll(attacker, defender):
                # damage spread
                i, d = divmod(attacker.fighter.power / 3, 1)
                # raw damage
                attacker_power = attacker.fighter.power * (0.7 + 0.07*attacker.fighter.archery) + \
                                 attacker.fighter.archery/2
                raw_damage = attacker_power + libtcod.random_get_int(0, -i, i)
                # amplification sources
                amp = sum(equipment.damage_amp_bonus for equipment in get_all_equipped(attacker))
                # armor reduction
                die = libtcod.random_get_int(0, 0, 20)
                if die + defender.fighter.shielding > attacker.fighter.archery + attacker.fighter.power:
                    # target is strong defender
                    reduction = 0.5 * defender.fighter.armor + 0.03 * defender.fighter.shielding
                else:
                    reduction = 0.2 * defender.fighter.armor + 0.03 * defender.fighter.shielding
                # damage after modifiers
                damage = int(round(raw_damage - reduction) * (1 + amp))
                if damage > 0:
                    defender.fighter.take_damage(damage)
                    return CombatResults.HIT
                else:
                    return CombatResults.ARMOR
            else:
                return CombatResults.BLOCK
        else:
            return CombatResults.MISS


    @staticmethod
    def melee_hit_roll(attacker, defender):
        base_chance = 8
        miss_mod = 0.5 * defender.fighter.fighting + (0.33 + 0.3*defender.fighter.shielding)*defender.fighter.defense +\
            defender.fighter.evasion
        attack_mod = attacker.fighter.fighting + attacker.fighter.accuracy
        chance = int(round(base_chance + miss_mod - attack_mod))
        die = libtcod.random_get_int(0, 0, 100)
        if die > chance:
            return True
        return False

    @staticmethod
    def melee_block_roll(attacker, defender):
        base_chance = 5
        if defender.isplayer:
            for e in defender.inventory.get_all_equipped():
                if e.is_equipped and e.slot == Slot.LEFT_HAND:
                    break
            else:
                # cannot block without a shield equipped
                return True
        if defender.prof == 'Fighter':
            shield_mod = 1.1 + 0.03 * defender.fighter.shielding
        elif defender.prof in ['Stalker, Alchemist']:
            shield_mod = 1.0 + 0.02 * defender.fighter.shielding
        else:
            shield_mod = 0.9 + 0.02 * defender.fighter.shielding

        block_mod = (defender.fighter.shielding + defender.fighter.defense*0.35)*shield_mod
        attack_mod = attacker.fighter.fighting
        chance = int(round(base_chance + block_mod - attack_mod))
        die = libtcod.random_get_int(0, 0, 100)
        if die > chance:
            return True
        # blocked attack
        return False

    @staticmethod
    def ranged_hit_roll(attacker, defender):
        base_chance = 17
        miss_mod = (0.55 + 0.03 * defender.fighter.shielding)*defender.fighter.defense + defender.fighter.evasion
        attack_mod = attacker.fighter.archery + attacker.fighter.accuracy
        chance = int(round(base_chance + miss_mod - attack_mod))
        die = libtcod.random_get_int(0, 0, 100)
        if die > chance:
            return True
        return False

    @staticmethod
    def ranged_block_roll(attacker, defender):
        base_chance = 5
        if defender.isplayer:
            for e in get_all_equipped(defender):
                if e.is_equipped and e.slot == 'left hand':
                    break
            else:
                return False
        if defender.prof == 'Fighter':
            shield_mod = 0.9 + 0.03 * defender.fighter.shielding
        elif defender.prof in ['Stalker', 'Alchemist']:
            shield_mod = 0.8 + 0.02 * defender.fighter.shielding
        else:
            shield_mod = 0.7 + 0.02 * defender.fighter.shielding

        block_mod = (defender.fighter.shielding + defender.fighter.defense * 0.35) * shield_mod
        attack_mod = attacker.fighter.archery

        chance = int(round(base_chance + block_mod - attack_mod))
        die = libtcod.random_get_int(0, 0, 100)
        if die > chance:
            return True
        return False
    

class CombatResults(Enum):

    MISS = auto()
    BLOCK = auto()
    HIT = auto()
    ARMOR = auto()
