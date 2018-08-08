import libtcodpy as libtcod
from classes.ai.ai_basic import BasicAi
from classes.entity import Entity
from classes.fighter import Fighter
from classes.rectangle import Rectangle
from classes.time_object import TimeObject

from loaders.constants import Constants
from logic.death_functions import DeathFunctions


class MapMaker:

    def __init__(self):
        self.consts = Constants.consts

    def new_dungeon(self, world):
        consts = Constants.consts
        rooms = []
        num_rooms = 0

        max_monsters = self.from_dungeon_level(self.consts['max_monsters'], world.dungeon_level)

        monster_chances = self.monster_chances_from_dlevel(world.dungeon_level)

        die = libtcod.random_get_int(0, 0, 100)
        if die < 10 + 2*world.dungeon_level:
            room_minsize = 1
            room_maxsize = 8
        elif die < 50:
            room_minsize = consts['ROOM_MIN_SIZE']
            room_maxsize = consts['ROOM_MAX_SIZE']
        else:
            room_minsize = 8
            room_maxsize = 12

        for r in range(consts['MAX_ROOMS']):
            w = libtcod.random_get_int(0, room_minsize, room_maxsize)
            h = libtcod.random_get_int(0, room_minsize, room_maxsize)
            x = libtcod.random_get_int(0, 0, consts['MAP_WIDTH'] - w - 1)
            y = libtcod.random_get_int(0, 0, consts['MAP_HEIGHT'] - h - 1)

            new_room = Rectangle(x, y, w, h)

            failed = False
            for other_room in rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break

            if not failed:
                MapMaker.create_room(new_room, world.tilemap)
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    world.player.x = new_x
                    world.player.y = new_y
                else:
                    (prev_x, prev_y) = rooms[num_rooms-1].center()
                    if libtcod.random_get_int(0, 0, 1) == 1:
                        MapMaker.create_h_tunnel(prev_x, new_x, prev_y, world.tilemap)
                        MapMaker.create_v_tunnel(prev_y, new_y, new_x, world.tilemap)
                    else:
                        MapMaker.create_v_tunnel(prev_y, new_y, prev_x, world.tilemap)
                        MapMaker.create_h_tunnel(prev_x, new_x, new_y, world.tilemap)

                self.place_objects(world, new_room, max_monsters, monster_chances)
                rooms.append(new_room)
                num_rooms += 1

    @staticmethod
    def create_room(room, tilemap):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                tilemap[x][y].blocked = False
                tilemap[x][y].block_sight = False

    @staticmethod
    def create_h_tunnel(x1, x2, y, tilemap, variance=False):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            tilemap[x][y].blocked = False
            tilemap[x][y].block_sight = False

    @staticmethod
    def create_v_tunnel(y1, y2, x, tilemap, variance=False):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            tilemap[x][y].blocked = False
            tilemap[x][y].block_sight = False

    @staticmethod
    def from_dungeon_level(table, dungeon_level):
        for (value, level) in reversed(table):
            if dungeon_level >= level:
                return value
        return 0

    @staticmethod
    def random_choice(chances_dict):
        chances = chances_dict.values()
        strings = list(chances_dict.keys())
        return strings[MapMaker.random_choice_index(chances)]

    @staticmethod
    def random_choice_index(chances):
        die = libtcod.random_get_int(0, 1, sum(chances))
        running_sum = 0
        choice = 0
        for w in chances:
            running_sum += w
            if die <= running_sum:
                return choice
            choice += 1

    def place_objects(self, world, room, max_monsters, monster_chances):

        consts = Constants.consts

        num_monsters = libtcod.random_get_int(0, 0, max_monsters)

        for i in range(num_monsters):
            x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
            y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)

            if not Entity.is_blocked(x, y, world.tilemap, world.objects):

                choice = self.random_choice(monster_chances)
                monster = None

                if choice == 'mchance_orc':

                    time_c = TimeObject()
                    ai_c = BasicAi(world)
                    fighter_c = Fighter(hp=10, defense=2, power=3, xp=5, armor=0, mana=0, magic=0,
                                        death_function=DeathFunctions.monster_death, fighting=0)
                    monster = Entity(x, y, consts['orc_tile'], 'orc', libtcod.white, blocks=True,
                                     fighter=fighter_c, ai=ai_c, timeobj=time_c)

                elif choice == 'mchance_snake':
                    pass

                else:
                    pass

                if monster is not None:
                    world.objects.append(monster)
                    monster.timeobj.register()

    def monster_chances_from_dlevel(self, dungeon_level):
        chances = dict()
        chances['mchance_orc'] = self.from_dungeon_level(self.consts['mchance_orc'], dungeon_level)
        chances['mchance_snake'] = self.from_dungeon_level(self.consts['mchance_snake'], dungeon_level)
        chances['mchance_troll'] = self.from_dungeon_level(self.consts['mchance_troll'], dungeon_level)
        chances['mchance_guard_dog'] = self.from_dungeon_level(self.consts['mchance_guard_dog'], dungeon_level)
        chances['mchance_orc_spearthrower'] = self.from_dungeon_level(self.consts['mchance_orc'], dungeon_level)
        chances['mchance_skeleton'] = self.from_dungeon_level(self.consts['mchance_skeleton'], dungeon_level)
        chances['mchance_orc_soldier'] = self.from_dungeon_level(self.consts['mchance_orc_soldier'], dungeon_level)
        chances['mchance_phantasm'] = self.from_dungeon_level(self.consts['mchance_phantasm'], dungeon_level)
        chances['mchance_ancient_troll'] = self.from_dungeon_level(self.consts['mchance_ancient_troll'], dungeon_level)
        chances['mchance_orc_warlock'] = self.from_dungeon_level(self.consts['mchance_orc_warlock'], dungeon_level)
        chances['mchance_vampire'] = self.from_dungeon_level(self.consts['mchance_vampire'], dungeon_level)
        chances['mchance_lich'] = self.from_dungeon_level(self.consts['mchance_lich'], dungeon_level)
        chances['mchance_demonspawn'] = self.from_dungeon_level(self.consts['mchance_demonspawn'], dungeon_level)
        chances['mchance_demon'] = self.from_dungeon_level(self.consts['mchance_demon'], dungeon_level)
        print(chances)
        return chances


