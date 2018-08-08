import libtcodpy as libtcod
from classes.entity import Entity
from classes.fighter import Fighter
from classes.inventory import Inventory
from classes.tile import Tile
from loaders.constants import Constants
from logic.death_functions import DeathFunctions


class Initializer:

    @staticmethod
    def init_game():
        consts = Constants.consts
        libtcod.console_set_custom_font(
            consts['CUSTOM_FONT'], libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD, 32, 10)
        libtcod.console_init_root(
            consts['SCREEN_WIDTH'], consts['SCREEN_HEIGHT'], consts['GAME_TITLE'], False, libtcod.RENDERER_SDL)
        libtcod.sys_set_fps(consts['LIMIT_FPS'])
        con = libtcod.console_new(consts['SCREEN_WIDTH'], consts['SCREEN_HEIGHT'])
        panel = libtcod.console_new(consts['SCREEN_WIDTH'], consts['PANEL_HEIGHT'])
        mouse = libtcod.Mouse()
        key = libtcod.Key()
        Initializer.__load_custom_font()
        return con, panel, mouse, key

    @staticmethod
    def init_player(race, prof, name):
        consts = Constants.consts
        race_dict = consts[race]
        prof_dict = consts[prof]
        hp = race_dict['hp'] + prof_dict['hp_bonus']
        defense = race_dict['defense'] + prof_dict['def_bonus']
        power = race_dict['power'] + prof_dict['power_bonus']
        xp = 0
        armor = 0
        mana = race_dict['mana'] + prof_dict['mana_bonus']
        magic = race_dict['magic'] + prof_dict['magic_bonus']
        fighting = race_dict['fighting'] + prof_dict['fighting_bonus']
        shielding = race_dict['shielding'] + prof_dict['shielding_bonus']
        conjuring = race_dict['conjuring'] + prof_dict['conjuring_bonus']
        archery = race_dict['archery'] + prof_dict['archery_bonus']
        transmutations = race_dict['transmutations'] + prof_dict['transmutations_bonus']
        hexes = race_dict['hexes'] + prof_dict['hexes_bonus']
        speed = race_dict['speed']
        mana_regen = race_dict['mana_regen']

        fighter_component = Fighter(hp, defense, power, xp, armor, mana, magic,
                                    death_function=DeathFunctions.player_death,
                                    fighting=fighting, shielding=shielding, conjuring=conjuring,
                                    archery=archery, transmutations=transmutations, hexes=hexes,
                                    speed=speed, mana_regen=mana_regen)
        fighter_component.stealthiness = race_dict['stealthiness']

        inv_component = Inventory()

        player = Entity(0, 0, consts['player_tile'], name, libtcod.white, blocks=True, fighter=fighter_component,
                        race=race, prof=prof, inventory=inv_component)
        player.level = 1
        player.isplayer = True
        return player

    @staticmethod
    def init_tilemap():
        consts = Constants.consts
        tilemap = [[Tile(True) for y in range(consts['MAP_HEIGHT'])]
                   for x in range(consts['MAP_WIDTH'])]
        return tilemap

    @staticmethod
    def init_fov_map(tilemap):
        consts = Constants.consts
        fov_map = libtcod.map_new(consts['MAP_WIDTH'], consts['MAP_HEIGHT'])
        for y in range(consts['MAP_HEIGHT']):
            for x in range(consts['MAP_WIDTH']):
                libtcod.map_set_properties(fov_map, x, y, not tilemap[x][y].block_sight, not tilemap[x][y].blocked)
        return fov_map

    @staticmethod
    def __load_custom_font():
        a = 256
        for y in range(5, 6):
            libtcod.console_map_ascii_codes_to_font(a, 32, 0, y)
            a += 32
