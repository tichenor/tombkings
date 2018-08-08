import libtcodpy as libtcod
from gui.messages import Messages
from loaders.constants import Constants


class RenderFunctions:

    fov_recompute = True

    @staticmethod
    def render_all(con, panel, world):
        consts = Constants.consts
        if RenderFunctions.fov_recompute:
            RenderFunctions.fov_recompute = False
        RenderFunctions.compute_fov(world)
        RenderFunctions.__render_tiles(con, world.tilemap, world.fov_map, world.debug)
        RenderFunctions.__render_effects(con, world.objects, world.player, world.tilemap, world.fov_map)
        RenderFunctions.__render_objects(con, world.objects, world.player, world.tilemap, world.fov_map, world.debug)
        libtcod.console_blit(con, 0, 0, consts['SCREEN_WIDTH'], consts['SCREEN_HEIGHT'], 0, 0, 0)
        libtcod.console_set_default_background(panel, libtcod.darker_gray) # panel color
        libtcod.console_clear(panel)
        RenderFunctions.__render_messages(panel)
        RenderFunctions.__render_bars(panel, world.player)
        RenderFunctions.__render_text(panel, world.dungeon_level)
        libtcod.console_blit(panel, 0, 0, consts['SCREEN_WIDTH'], consts['PANEL_HEIGHT'], 0, 0, consts['PANEL_Y'])

    @staticmethod
    def compute_fov(world):
        torch = RenderFunctions.__get_torch_radius(world.player.prof)
        libtcod.map_compute_fov(world.fov_map, world.player.x, world.player.y, torch,
                                Constants.consts['FOV_LIGHT_WALLS'], libtcod.FOV_BASIC)

    @staticmethod
    def __render_tiles(con, tilemap, fov_map, debug):
        consts = Constants.consts
        for y in range(consts['MAP_HEIGHT']):
            for x in range(consts['MAP_WIDTH']):
                if debug:
                    visible = True
                else:
                    visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = tilemap[x][y].block_sight

                if not visible:
                    if tilemap[x][y].explored:
                        if wall:
                            libtcod.console_put_char_ex(con, x, y, consts['wall_tile'], libtcod.grey, libtcod.black)
                        else:
                            libtcod.console_put_char_ex(con, x, y, consts['floor_tile'], libtcod.grey, libtcod.black)
                else:
                    if wall:
                        libtcod.console_put_char_ex(con, x, y, consts['wall_tile'], libtcod.white, libtcod.black)
                    else:
                        libtcod.console_put_char_ex(con, x, y, consts['floor_tile'], libtcod.white, libtcod.black)
                        tilemap[x][y].explored = True

    @staticmethod
    def __render_effects(con, objects, player, tilemap, fov_map):
        consts = Constants.consts
        for o in objects:
            if o.fighter:
                for b in o.fighter.buff:
                    if b.name == 'Hex Of Radiance':
                        for y in range(-consts['HEX_OF_RADIANCE_RADIUS'], consts['HEX_OF_RADIANCE_RADIUS'] + 1):
                            for x in range(-consts['HEX_OF_RADIANCE_RADIUS'], consts['HEX_OF_RADIANCE_RADIUS'] + 1):
                                if 0 <= o.x + x <= consts['MAP_WIDTH'] and \
                                   0 <= o.y + y <= consts['MAP_HEIGHT']:
                                    visible = libtcod.map_is_in_fov(fov_map, x, y)
                                    wall = tilemap[x][y].block_sight
                                    if not visible:
                                        if tilemap[x][y].explored:
                                            if wall:
                                                libtcod.console_put_char_ex(
                                                    con, x, y, consts['wall_tile'], libtcod.light_violet, libtcod.black)
                                            else:
                                                libtcod.console_put_char_ex(
                                                    con, x, y, consts['floor_tile'], libtcod.light_violet, libtcod.black)
                                    else:
                                        if wall:
                                            libtcod.console_put_char_ex(
                                                con, x, y, consts['wall_tile'], libtcod.lighter_violet, libtcod.black)
                                        else:
                                            libtcod.console_put_char_ex(
                                                    con, x, y, consts['floor_tile'], libtcod.lighter_violet, libtcod.black)
                                            tilemap[x][y].explored = True
        for b in player.fighter.buff:
            if b.name == 'White Light':
                for y in range(-consts['WHITE_LIGHT_RADIUS'], consts['WHITE_LIGHT_RADIUS']):
                    for x in range(-consts['WHITE_LIGHT_RADIUS'], consts['WHITE_LIGHT_RADIUS']):
                        if 0 <= player.x + x <= consts['MAP_WIDTH'] and \
                           0 <= player.y + y <= consts['MAP_HEIGHT']:
                            visible = libtcod.map_is_in_fov(fov_map, x, y)
                            wall = tilemap[x][y].block_sight
                            if not visible:
                                if tilemap[x][y].explored:
                                    if wall:
                                        libtcod.console_put_char_ex(
                                            con, x, y, consts['wall_tile'], libtcod.light_yellow, libtcod.black)
                                    else:
                                        libtcod.console_put_char_ex(
                                            con, x, y, consts['floor_tile'], libtcod.light_yellow, libtcod.black)
                            else:
                                if wall:
                                    libtcod.console_put_char_ex(
                                        con, x, y, consts['wall_tile'], libtcod.lighter_yellow, libtcod.black)
                                else:
                                    libtcod.console_put_char_ex(
                                            con, x, y, consts['floor_tile'], libtcod.lighter_yellow, libtcod.black)
                                    tilemap[x][y].explored = True

    @staticmethod
    def __render_objects(con, objects, player, tilemap, fov_map, debug):
        for o in objects:
            if o != player:
                if debug and o.always_visible is False:
                    o.always_visible = True
                o.draw(fov_map, tilemap, con)
        player.draw(fov_map, tilemap, con)

    @staticmethod
    def __render_messages(panel):
        y = 1
        for line, color in Messages.game_msgs:
            libtcod.console_set_default_foreground(panel, color)
            libtcod.console_print_ex(panel, Constants.consts['MSG_X'], y, libtcod.BKGND_NONE, libtcod.LEFT, line)
            y += 1

    @staticmethod
    def __render_bars(panel, player):
        consts = Constants.consts
        # hp bar
        RenderFunctions.__render_bar(panel, 1, 1, consts['BAR_WIDTH'], 'HP', player.fighter.hp,
                                     player.fighter.max_hp, libtcod.light_red, libtcod.darker_red)
        # mana bar
        RenderFunctions.__render_bar(panel, 1, 2, consts['BAR_WIDTH'], 'MP', player.fighter.mana,
                                     player.fighter.max_mana, libtcod.light_blue, libtcod.darker_blue)

    @staticmethod
    def __render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
        bar_width = int(float(value) / maximum * total_width)
        libtcod.console_set_default_background(panel, back_color)
        libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)
        libtcod.console_set_default_background(panel, bar_color)
        if bar_width > 0:
            libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)
        libtcod.console_set_default_foreground(panel, libtcod.white)
        libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                                 name + ': ' + str(value) + '/' + str(maximum))

    @staticmethod
    def __render_text(panel, dungeon_level):
        libtcod.console_print_ex(panel, 5, 3, libtcod.BKGND_NONE, libtcod.LEFT, 'Dungeon level ' + str(dungeon_level))
        #libtcod.console_set_default_foreground(panel, libtcod.light_gray)
        #libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse())
        #libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_player())

    @staticmethod
    def __get_torch_radius(prof):
        if prof == 'Green Elf':
            return 12
        return 8
