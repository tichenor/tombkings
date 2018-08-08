import libtcodpy as libtcod

from classes.ai.ai import MonsterAi
from game.entity_states import EntityState
from game.event_handler import EventHandler
from loaders.constants import Constants
from logic.rolls import Rolls


class BasicAi(MonsterAi):

    def __init__(self, world):
        super().__init__()
        self.world = world
        self.state = EntityState.IDLE
        self.target = None
        self.timer = 0
        self.target_coord = None, None
        self.sleep_cooldown = 20
        self.sleep_timer = 0

    def take_turn(self):
        entity = self.owner
        player = self.world.player
        cost = 0

        if self.state == EntityState.SLEEPING:
            if libtcod.map_is_in_fov(self.world.fov_map, entity.x, entity.y) or \
               entity.distance_to_entity(player) + player.fighter.stealthiness <= 10:
                if Rolls.wake_up_roll(entity, player):
                    self.state = EntityState.IDLE
                    if libtcod.map_is_in_fov(self.world.fov_map, entity.x, entity.y):
                        EventHandler.add_entity_event('wake_up', entity)
            cost = 100

        elif self.state == EntityState.IDLE:
            if libtcod.map_is_in_fov(self.world.fov_map, entity.x, entity.y):
                self.target = player
                self.timer = 10
                self.state = EntityState.CHASING
                self.target_coord = player.x, player.y
                EventHandler.add_entity_event('spotted', entity)
                cost = 50
            else:
                wander_chance = libtcod.random_get_int(0, 0, 100)
                if wander_chance <= 10:
                    self.state = EntityState.WANDERING
                elif wander_chance <= 20 and self.sleep_timer == 0:
                    self.state = EntityState.SLEEPING
                    self.sleep_timer += self.sleep_cooldown
                else:
                    cost = 100

        elif self.state == EntityState.CHASING:
            if libtcod.map_is_in_fov(self.world.fov_map, entity.x, entity.y):
                if entity.distance_to_entity(player) >= 2:
                    entity.move_astar(player, self.world.tilemap, self.world.objects)
                    self.target_coord = player.x, player.y
                    cost = 100
                elif self.target.fighter.hp > 0:
                    entity.fighter.melee_attack(self.target)
                    cost = 100
            elif self.target_coord != (None, None) and self.timer > 0:
                if entity.x == self.target_coord[0] and entity.y == self.target_coord[1]:
                    self.target_coord = (None, None)
                    self.state = EntityState.IDLE
                else:
                    entity.move_towards(self.target_coord[0], self.target_coord[1], self.world.tilemap, self.world.objects)
                    self.timer -= 1
                    cost = 100
            elif self.timer <= 0:
                self.timer = 0
                self.target_coord = (None, None)
                self.state = EntityState.IDLE

        elif self.state == EntityState.WANDERING:
            if libtcod.map_is_in_fov(self.world.fov_map, entity.x, entity.y):
                self.target = player
                self.timer = 10
                self.state = EntityState.CHASING
                self.target_coord = player.x, player.y
                EventHandler.add_entity_event('spotted', entity)
                cost = 50
            else:
                if self.target_coord != (None, None):
                    if entity.x == self.target_coord[0] and entity.y == self.target_coord[1]:
                        self.target_coord = (None, None)
                        self.state = EntityState.IDLE
                    else:
                        old_x, old_y = entity.x, entity.y
                        entity.move_towards(self.target_coord[0], self.target_coord[1], self.world.tilemap, self.world.objects)
                        if entity.x == old_x and entity.y == old_y:
                            self.target_coord = (None, None)
                            self.state = EntityState.IDLE
                    cost = 100
                else:
                    dx = libtcod.random_get_int(0, -8, 8)
                    dy = libtcod.random_get_int(0, -8, 8)
                    if 0 <= entity.x + dx < Constants.consts['MAP_WIDTH'] and \
                       0 <= entity.y + dy < Constants.consts['MAP_HEIGHT']:
                        if not self.world.tilemap[entity.x + dx][entity.y + dy].blocked:
                            self.target_coord = entity.x + dx, entity.y + dy

        if self.state != EntityState.SLEEPING and self.sleep_timer > 0:
            self.sleep_timer -= 1
        return cost




