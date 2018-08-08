import libtcodpy as libtcod
from game.action_type import ActionType
from game.event_handler import EventHandler

from game.slots import Slot
from inout.render_functions import RenderFunctions
from logic.combat import Combat


class PlayerActions:

    @staticmethod
    def move_or_attack(dx, dy, objects, player, tilemap):
        x = player.x + dx
        y = player.y + dy
        target = None
        for o in objects:
            if o.fighter and o.x == x and o.y == y:
                target = o
                break
        if target is not None:
            results = Combat.melee_attack(player, target)
            EventHandler.add_combat_event(ActionType.MELEE_COMBAT, (player, target, results))
            return ActionType.MELEE_COMBAT
        else:
            player.move(dx, dy, tilemap, objects)
            RenderFunctions.fov_recompute = True
            EventHandler.add_move_event(ActionType.MOVE, None)
            return ActionType.MOVE

    @staticmethod
    def attack_closest(objects, player, fov_map, max_range=10):
        closest = None
        closest_dist = max_range + 1

        for o in objects:
            if o.fighter and o != player and libtcod.map_is_in_fov(fov_map, o.x, o.y):
                dist = player.distance_to_entity(o)
                if dist < closest_dist:
                    closest = o
                    closest_dist = dist

        if closest is not None and libtcod.map_is_in_fov(fov_map, closest.x, closest.y):
            if player.distance_to_entity(closest) >= 2:
                if player.inventory.get_equipped_in_slot(Slot.RANGED) is None:
                    player.move_astar(closest)
                    RenderFunctions.fov_recompute = True
                    EventHandler.add_move_event(ActionType.MOVE, None)
                    return ActionType.MOVE
                else:
                    if player.distance_to_entity(closest) <= player.fighter.firing_range:
                        result = Combat.ranged_attack(player, closest)
                        RenderFunctions.fov_recompute = True
                        EventHandler.add_combat_event(ActionType.RANGED_COMBAT, (player, closest, result))
                        return ActionType.RANGED_COMBAT
                    else:
                        player.move_astar(closest)
                        RenderFunctions.fov_recompute = True
                        EventHandler.add_move_event(ActionType.MOVE, None)
                        return ActionType.MOVE
            elif closest.fighter.hp > 0:
                result = Combat.melee_attack(player, closest)
                EventHandler.add_combat_event(ActionType.MELEE_COMBAT, (player, closest, result))
                return ActionType.MELEE_COMBAT

    @staticmethod
    def wait():
        return ActionType.WAIT

    @staticmethod
    def pick_up(player, objects):
        for o in objects:
            if o.x == player.x and o.y == player.y and o.item:
                return o.item.picked_up(player, objects)

