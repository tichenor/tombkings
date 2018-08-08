import math

import libtcodpy as libtcod
from loaders.constants import Constants


class Entity:

    def __init__(self, x, y, char, name, color, blocks=False, always_visible=False, fighter=None, ai=None,
                 item=None, use_function=None, equipment=None, race=None, prof=None, trap=None, timeobj=None,
                 loot=None, inventory=None):

        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.blocks = blocks
        self.always_visible = always_visible
        self.race = race
        self.prof = prof

        self.item = item
        if self.item:
            self.item.owner = self

        self.fighter = fighter
        if self.fighter:
            self.fighter.owner = self

        self.ai = ai
        if self.ai:
            self.ai.owner = self

        self.equipment = equipment
        if self.equipment:
            self.equipment.owner = self
            if not self.item:
                self.item = Item()
                self.item.owner = self

        self.trap = trap
        if self.trap:
            self.trap.owner = self

        self.timeobj = timeobj
        if self.timeobj:
            self.timeobj.owner = self

        self.loot = loot
        if self.loot:
            self.loot.owner = self

        self.inventory = inventory
        if self.inventory:
            self.inventory.owner = self

        self.isplayer = False

    def draw(self, fov_map, tilemap, con):
        if (libtcod.map_is_in_fov(fov_map, self.x, self.y) or
           (self.always_visible and tilemap[self.x][self.y].explored)):
            libtcod.console_set_default_foreground(con, self.color)
            libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)
        elif not libtcod.map_is_in_fov(fov_map, self.x, self.y) and tilemap[self.x][self.y].explored:
            libtcod.console_put_char_ex(con, self.x, self.y, Constants.consts['floor_tile'], libtcod.gray, libtcod.black)

    def clear(self, fov_map, tilemap, con):
        if libtcod.map_is_in_fov(fov_map, self.x, self.y):
            libtcod.console_put_char_ex(con, self.x, self.y, Constants.consts['floor_tile'], libtcod.white, libtcod.black)
        elif tilemap[self.x][self.y].explored:
            libtcod.console_put_char_ex(con, self.x, self.y, Constants.consts['floor_tile'], libtcod.gray, libtcod.black)

    def move(self, dx, dy, tilemap, objects):
        if tilemap[self.x + dx][self.y + dy]:
            if not self.is_blocked(self.x + dx, self.y + dy, tilemap, objects):
                self.x += dx
                self.y += dy

    def move_towards(self, target_x, target_y, tilemap, objects):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        dx = int(round(dx / dist))
        dy = int(round(dy / dist))
        self.move(dx, dy, tilemap, objects)

    def move_from(self, target_x, target_y, tilemap, objects):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        dx = int(round(dx / dist))
        dy = int(round(dy / dist))
        self.move(-dx, -dy, tilemap, objects)

    def move_astar(self, target, tilemap, objects):
        map_w = Constants.consts['MAP_WIDTH']
        map_h = Constants.consts['MAP_HEIGHT']
        fov = libtcod.map_new(map_w, map_h)
        for y1 in range(map_h):
            for x1 in range(map_w):
                libtcod.map_set_properties(fov, x1, y1, not tilemap[x1][y1].block_sight, not tilemap[x1][y1].blocked)
        for o in objects:
            if o.blocks and o != self and o != target:
                libtcod.map_set_properties(fov, o.x, o.y, True, False)
        my_path = libtcod.path_new_using_map(fov, 1.41)
        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                self.x = x
                self.y = y
        else:
            self.move_towards(target.x, target.y, tilemap, objects)
        libtcod.path_delete(my_path)

    def distance_to_entity(self, other):
        # RENAMED FROM: distance_to
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def distance_to_coord(self, x, y):
        # RENAMED FROM: distance
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def send_to_back(self, objects):
        objects.remove(self)
        objects.insert(0, self)

    @staticmethod
    def is_blocked(x, y, tilemap, objects):
        if tilemap[x][y].blocked:
            return True
        for o in objects:
            if o.blocks and o.x == x and o.y == y:
                return True
        return False


