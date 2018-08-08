import sys

import libtcodpy as libtcod
from classes.world import World
from game.event_handler import EventHandler
from gui.menu import Menu
from inout.controls import Controls
from inout.render_functions import RenderFunctions

from loaders.initializer import Initializer

# senast arbetat på: place_objects, MapMaker
from loaders.map_maker import MapMaker
from logic.death_functions import DeathFunctions


def main():

    con, panel, mouse, key = Initializer.init_game()

    newgame = Menu.main_menu(con, key, mouse)

    if not newgame:
        sys.exit(0)

    race, prof = Menu.starting_menu(con, key, mouse)

    world = World(race, prof)

    # world.debug = True

    mapmaker = MapMaker()

    mapmaker.new_dungeon(world)

    world.fov_map = Initializer.init_fov_map(world.tilemap)

    DeathFunctions.world = world

    while not libtcod.console_is_window_closed():

        RenderFunctions.render_all(con, panel, world)
        libtcod.console_flush()

        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        action = Controls.handle_keys(key, world)

        world.update(action)


if __name__ == "__main__":
    main()
