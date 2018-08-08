import libtcodpy as libtcod
from loaders.constants import Constants


class Menu:

    @staticmethod
    def basic_menu(con, header, options, width, key, recomp=True):
        consts = Constants.consts
        if len(options) > 26:
            raise ValueError('Cannot have a menu with more than 26 options.')
        header_height = libtcod.console_get_height_rect(con, 0, 0, width, consts['SCREEN_HEIGHT'], header)
        if header == '':
            header_height = 0
        height = len(options) + header_height
        window = libtcod.console_new(width, height)

        libtcod.console_set_default_foreground(window, libtcod.white)
        libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

        y = header_height
        letter_index = ord('a')
        for opt_text in options:
            text = '(' + chr(letter_index) + ')' + opt_text
            libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
            y += 1
            letter_index += 1

        x = consts['SCREEN_WIDTH'] / 2 - width / 2
        y = consts['SCREEN_HEIGHT'] / 2 - height / 2
        libtcod.console_blit(window, 0, 0, width, height, 0, int(x), int(y), bfade=0.7)

        libtcod.console_flush()
        key = libtcod.console_wait_for_keypress(True)

        index = key.c - ord('a')
        if 0 <= index < len(options):
            return index
        return None

    @staticmethod
    def main_menu(con, key, mouse):
        consts = Constants.consts
        path = consts['MENU_BACKGROUND']
        img = libtcod.image_load(path)

        while not libtcod.console_is_window_closed():
            libtcod.image_blit_2x(img, 0, 0, 0)
            choice = Menu.basic_menu(con, '', ['New game', 'Quit'], 24, key)
            if choice == 0:
                return True
            elif choice == 1:
                return False

    @staticmethod
    def starting_menu(con, key, mouse):
        race_list = ['Human', 'Dwarf', 'Gnome', 'Green Elf']
        class_list = ['Fighter', 'Stalker', 'Conjurer', 'Alchemist', 'Hex Mage']
        c1 = None
        c2 = None
        while not libtcod.console_is_window_closed():
            c1 = Menu.basic_menu(con, 'Choose a race.', race_list, 24, 1)
            if c1 is not None:
                while not libtcod.console_is_window_closed():
                    c2 = Menu.basic_menu(con, 'Choose a profession.', class_list, 70, 1)
                    if c2 is not None:
                        return race_list[c1], class_list[c2]
