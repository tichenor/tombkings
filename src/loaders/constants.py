import libtcodpy as libtcod


class Constants:

    consts = dict()
    # screen
    consts['SCREEN_WIDTH'] = 80
    consts['SCREEN_HEIGHT'] = 55
    consts['LIMIT_FPS'] = 20
    # map
    consts['MAP_WIDTH'] = 80
    consts['MAP_HEIGHT'] = 43
    consts['ROOM_MAX_SIZE'] = 6
    consts['ROOM_MIN_SIZE'] = 5
    consts['MAX_ROOMS'] = 33
    # bsp map
    consts['BSP_DEPTH'] = 10
    consts['BSP_MIN_SIZE'] = 7
    consts['BSP_FULL_ROOMS'] = False
    # tile indices
    consts['wall_tile'] = 256
    consts['floor_tile'] = 257
    consts['player_tile'] = 258
    consts['orc_tile'] = 259
    consts['troll_tile'] = 260
    consts['scroll_tile'] = 261
    consts['healingpotion_tile'] = 262
    consts['sword_tile'] = 263
    consts['shield_tile'] = 264
    consts['stairsdown_tile'] = 265
    consts['dagger_tile'] = 266
    consts['apple_tile'] = 267
    consts['healthpot_tile'] = 268
    consts['manapot_tile'] = 269
    consts['berserkpot_tile'] = 270
    consts['magicpot_tile'] = 271
    consts['scroll_tile'] = 272
    # field of vision
    consts['FOV_ALGO'] = 0
    consts['FOV_LIGHT_WALLS'] = True
    consts['TORCH_RADIUS'] = 10
    consts['color_light_wall'] = libtcod.Color(130, 110, 50)
    consts['color_light_ground'] = libtcod.Color(200, 180, 50)
    consts['color_dark_wall'] = libtcod.Color(0, 0, 100)
    consts['color_dark_ground'] = libtcod.Color(50, 50, 150)
    consts['color_light_wall_cave'] = libtcod.Color(135, 90, 40)
    consts['color_light_ground_cave'] = libtcod.Color(140, 130, 40)
    consts['color_dark_wall_cave'] = libtcod.Color(0, 0, 80)
    consts['color_dark_ground_cave'] = libtcod.Color(40, 45, 140)
    # interface
    consts['BAR_WIDTH'] = 20 # health/mana bars
    consts['PANEL_HEIGHT'] = 12 # height of space between bottom of screen and game map
    consts['PANEL_Y'] = consts['SCREEN_HEIGHT'] - consts['PANEL_HEIGHT']
    consts['MSG_X'] = consts['BAR_WIDTH'] + 2 # position of message log
    consts['MSG_WIDTH'] = consts['SCREEN_WIDTH'] - consts['BAR_WIDTH'] - 2 # width of message log
    consts['MSG_HEIGHT'] = consts['PANEL_HEIGHT'] - 1 # reserve 1 line of space between panel and game map
    consts['INVENTORY_WIDTH'] = 50
    consts['SPELLBOOK_WIDTH'] = 50
    consts['DEBUG_WIDTH'] = 40
    consts['LEVEL_SCREEN_WIDTH'] = 60
    consts['CHARACTER_SCREEN_WIDTH'] = 30
    # spells
    consts['HEAL_AMOUNT'] = 40 # probably not used
    consts['RESTORE_MANA_AMOUNT'] = 20 # probably not used
    consts['LIGHTNING_RANGE'] = 5
    consts['LIGHTNING_DAMAGE'] = 20 # probably not used
    consts['CHAIN_LIGHTNING_RANGE'] = 6
    consts['CHAIN_LIGHTNING_RADIUS'] = 4
    consts['CONFUSE_NUM_TURNS'] = 10
    consts['CONFUSE_RANGE'] = 5
    consts['FIREBALL_RADIUS'] = 3
    consts['FIREBALL_DAMAGE'] = 12 # probably not used
    consts['FIREBLAST_RADIUS'] = 2
    consts['MAGIC_DART_RANGE'] = 4
    consts['BOLT_OF_ICE_RANGE'] = 5
    consts['RAIN_OF_ICE_RADIUS'] = 6
    consts['IMMOLATE_RANGE'] = 6
    consts['HIBERNATION_RANGE'] = 5
    consts['HEX_OF_RADIANCE_RADIUS'] = 6
    consts['RITUAL_OF_PACING_RANGE'] = 6
    consts['SPECTRAL_GUSHES_RANGE'] = 5
    # player
    consts['LEVEL_UP_BASE'] = 40
    consts['LEVEL_UP_FACTOR'] = 35
    # file paths, game constants
    consts['CUSTOM_FONT'] = 'assets/TiledFont4.png'
    consts['MENU_BACKGROUND'] = 'assets/menu_background1.png'
    consts['GAME_TITLE'] = 'The Game'
    # race bonuses
    consts['Human'] = {'hp': 20,
                       'defense': 3,
                       'power': 3,
                       'mana': 4,
                       'magic': 1,
                       'fighting': 1,
                       'shielding': 1,
                       'conjuring': 1,
                       'archery': 1,
                       'transmutations': 1,
                       'hexes': 1,
                       'speed': 100,
                       'mana_regen': 0.025,
                       'stealthiness': 1}
    consts['Dwarf'] = {'hp': 25,
                       'defense': 2,
                       'power': 3,
                       'mana': 2,
                       'magic': 0,
                       'fighting': 1,
                       'shielding': 1,
                       'conjuring': 0,
                       'archery': 0,
                       'transmutations': 0,
                       'hexes': 0,
                       'speed': 95,
                       'mana_regen': 0.02,
                       'stealthiness': 1}
    consts['Gnome'] = {'hp': 15,
                       'defense': 5,
                       'power': 2,
                       'mana': 6,
                       'magic': 2,
                       'fighting': 0,
                       'shielding': 0,
                       'conjuring': 1,
                       'archery': 0,
                       'transmutations': 1,
                       'hexes': 1,
                       'speed': 100,
                       'mana_regen': 0.04,
                       'stealthiness': 1}
    consts['Green Elf'] = {'hp': 18,
                           'defense': 6,
                           'power': 2,
                           'mana': 4,
                           'magic': 1,
                           'fighting': 0,
                           'shielding': 0,
                           'conjuring': 1,
                           'archery': 1,
                           'transmutations': 1,
                           'hexes': 1,
                           'speed': 105,
                           'mana_regen': 0.03,
                           'stealthiness': 2}
    # profession bonuses
    consts['Fighter'] = {'hp_bonus': 10,
                         'power_bonus': 1,
                         'def_bonus': 2,
                         'mana_bonus': 0,
                         'magic_bonus': 0,
                         'fighting_bonus': 1,
                         'shielding_bonus': 0,
                         'conjuring_bonus': 0,
                         'archery_bonus': 0,
                         'transmutations_bonus': 0,
                         'hexes_bonus': 0}
    consts['Stalker'] = {'hp_bonus': 5,
                         'power_bonus': 0,
                         'def_bonus': 2,
                         'mana_bonus': 1,
                         'magic_bonus': 0,
                         'fighting_bonus': 0,
                         'shielding_bonus': 0,
                         'conjuring_bonus': 0,
                         'archery_bonus': 1,
                         'transmutations_bonus': 0,
                         'hexes_bonus': 0}
    consts['Conjurer'] = {'hp_bonus': 2,
                          'power_bonus': 0,
                          'def_bonus': 0,
                          'mana_bonus': 3,
                          'magic_bonus': 1,
                          'fighting_bonus': 0,
                          'shielding_bonus': 0,
                          'conjuring_bonus': 1,
                          'archery_bonus': 0,
                          'transmutations_bonus': 0,
                          'hexes_bonus': 0}
    consts['Alchemist'] = {'hp_bonus': 5,
                           'power_bonus': 0,
                           'def_bonus': 0,
                           'mana_bonus': 2,
                           'magic_bonus': 1,
                           'fighting_bonus': 0,
                           'shielding_bonus': 0,
                           'conjuring_bonus': 1,
                           'archery_bonus': 0,
                           'transmutations_bonus': 2,
                           'hexes_bonus': 0}
    consts['Hex Mage'] = {'hp_bonus': 2,
                          'power_bonus': 0,
                          'def_bonus': 0,
                          'mana_bonus': 3,
                          'magic_bonus': 1,
                          'fighting_bonus': 0,
                          'shielding_bonus': 0,
                          'conjuring_bonus': 1,
                          'archery_bonus': 0,
                          'transmutations_bonus': 0,
                          'hexes_bonus': 2}

    # item & monster generation chances
    consts['max_monsters'] = [[2, 1], [3, 4], [4, 6], [5, 7], [6, 9]]

    consts['mchance_orc'] = [[30, 1], [45, 2], [30, 3], [20, 4], [10, 6], [0, 7]]
    consts['mchance_snake'] = [[20, 1], [15, 3], [7, 5], [0, 7]]
    consts['mchance_troll'] = [[12, 3], [20, 4], [27, 5], [22, 6], [17, 7], [7, 8], [2, 9], [0, 10]]
    consts['mchance_guard_dog'] = [[2, 4], [7, 5], [7, 6], [10, 7], [15, 8], [10, 9], [5, 10], [0, 11]]
    consts['mchance_orc_spearthrower'] = [[5, 4], [8, 5], [20, 6], [10, 8], [5, 9], [0, 10]]
    consts['mchance_skeleton'] = [[3, 6], [6, 7], [10, 8], [8, 9], [9, 10], [7, 11], [5, 12]]
    consts['mchance_orc_soldier'] = [[2, 6], [4, 7], [6, 8], [8, 9], [5, 10], [3, 11], [0, 12]]
    consts['mchance_phantasm'] = [[1, 6], [2, 7], [3, 8], [4, 9], [5, 10], [6, 11], [5, 12], [4, 13]]
    consts['mchance_ancient_troll'] = [[1, 8], [2, 9], [3, 10], [5, 11]]
    consts['mchance_orc_warlock'] = [[2, 5], [4, 7], [3, 8], [2, 10], [0, 11]]
    consts['mchance_vampire'] = [[2, 8], [3, 9], [4, 10]]
    consts['mchance_lich'] = [[1, 9], [2, 10], [3, 12], [5, 13]]
    consts['mchance_demonspawn'] = [[1, 12], [2, 13], [3, 14]]
    consts['mchance_demon'] = [[1, 15], [2, 16], [5, 17]]

    consts['max_items'] = [[1, 1], [2, 3], [3, 10]]
    
    consts['ichance_nothing'] = [[30, 1], [27, 2], [24, 3], [21, 4], [18, 5]]
    consts['ichance_potion_healing'] = [[30, 1], [27, 3], [24, 5], [22, 7]]
    consts['ichance_potion_mana'] = [[24, 1], [22, 3], [20, 5]]
    consts['ichance_potion_berserker'] = [[4, 2], [6, 3], [4, 5]]
    consts['ichance_potion_magic'] = [[1, 1], [2, 3], [4, 5]]
    consts['ichance_scroll_lightning'] = [[4, 2], [6, 4], [5, 7]]
    consts['ichance_scroll_fireball'] = [[2, 3], [3, 5], [4, 6]]
    consts['ichance_scroll_confuse'] = [[3, 1], [5, 2], [4, 3], [3, 5]]
    consts['ichance_scroll_knowledge'] = [[1, 3]]
    consts['ichance_t1_sword'] = [[3, 1], [5, 2], [6, 3], [5, 4], [2, 6]]
    consts['ichance_t1_shield'] = [[3, 1], [7, 3], [6, 4], [4, 5], [2, 6], [0, 8]]
    consts['ichance_t1_dagger'] = [[4, 1], [7, 2], [6, 3], [4, 5], [0, 7]]
    consts['ichance_t1_physical_armor'] = [[3, 1], [6, 2], [5, 5], [0, 7]]
    consts['ichance_t1_mage_weapon'] = [[3, 1], [5, 2], [6, 4], [4, 5], [0, 6]]
    consts['ichance_t1_mace'] = [[2, 1], [4, 2], [5, 3], [4, 4], [3, 5], [2, 6], [1, 7], [0, 8]]
    consts['ichance_t1_axe'] = [[2, 1], [3, 2], [4, 3], [5, 4], [4, 5], [3, 6], [1, 7], [0, 9]]
    consts['ichance_t1_helm'] = [[3, 1], [4, 2], [3, 4], [2, 5], [1, 6], [0, 7]]
    consts['ichance_t1_mage_armor'] = [[2, 1], [3, 2], [4, 3], [5, 4], [4, 5], [2, 6], [0, 9]]

    consts['ichance_t2_ranged_weapon'] = [[2, 4], [4, 5], [5, 6], [4, 9], [2, 11]]
    consts['ichance_t2_helm'] = [[3, 2], [5, 3], [7, 4], [3, 5], [1, 10]]
    consts['ichance_t2_dagger'] = [[2, 4], [4, 5], [9, 7], [7, 9], [4, 10], [2, 11]]
    consts['ichance_t2_sword'] = [[3, 5], [5, 6], [7, 7], [6, 9], [4, 10], [1, 11]]
    consts['ichance_t2_shield'] = [[1, 2], [3, 3], [4, 4], [5, 6], [4, 10], [2, 11]]
    consts['ichance_t2_mage_armor'] = [[2, 3], [3, 4], [5, 5], [7, 6], [6, 8], [2, 10]]
    consts['ichance_t2_mage_weapon'] = [[2, 3], [3, 4], [5, 5], [7, 6], [6, 8], [3, 10]]
    consts['ichance_t2_physical_armor'] = [[1, 3], [3, 5], [5, 6], [4, 8], [3, 9], [2, 10], [0, 11]]
    consts['ichance_t2_axe'] = [[1, 4], [2, 5], [5, 6], [6, 7], [4, 8], [2, 9], [0, 11]]
    consts['ichance_t2_mace'] = [[1, 3], [2, 5], [5, 6], [6, 7], [4, 8], [2, 9], [0, 11]]


    # descriptions
    # misc
    consts['HEALING_POTION_DESCR'] = 'A vial of fizzling, purple liquid. It has a faint, sweet smell that evokes pleasant memories...'
    consts['MANA_POTION_DESCR'] = 'The liquid looks blue as the sky. That\'s weird---sky? This place is making me forget how the surface looks like...'
    consts['POTION_OF_BERSERK_DESCR'] = 'Even though its sealed up pretty well with a cork, this potion emits a sickening stench... Out of all the horrible experiences Ive had so far, this smell takes the cake...'
    consts['POTION_OF_MAGIC_DESCR'] = 'This potion contains concentrated arcane powers. If I drink this it should boost my spellcasting significantly...for a limited time.'

    consts['SCROLL_LIGHTNING_BOLT_DESCR'] = 'The markings on this scroll seems to depict an Orc getting fried by lightning. Hmm...'
    consts['SCROLL_CONFUSION_DESCR'] = 'A scroll with esoteric symbols and what appears to be drawings of gestures. Well, someone is definitely confused...'
    consts['SCROLL_FIREBALL_DESCR'] = 'A fire that can never be quenched...No single Orc can escape the eternal flames!'
    consts['SCROLL_KNOWLEDGE_DESCR'] = 'Everything has a theory... including knowledge itself. Why don\'t I indulge already?'

    consts['ROTTEN_APPLE_DESCR'] = 'This item is best described as: That last apple in the fruit bowl that nobody was interested in. Indeed, it doesnt look very appealing...'
    consts['APPLE_DESCR'] = 'A seemingly fresh apple. Since i conjured it from thin air, I cannot guarantee it was biologically produced. But it looks tasty...'
    consts['FRENCH_FRY_DESCR'] = 'Well, its fried potato all right. Somebody, somewhere out there may or may not have noticed they are lacking a french fry by now...'

    # tier 1 tiems
    consts['CAP_DESCR'] = 'It offers little but some light head protection and room for thoughts.'
    consts['CAPE_DESCR'] = 'Fashionable as it may seem, the cape offers little cover of the front. The fabric is velvet.'
    consts['ROBE_DESCR'] = 'A fine academic-looking regalia. It is loose-fitting and easy to move in.'

    consts['SWORD_E_DESCR'] = 'A fine-looking short sword that appears to have many stories to tell.'
    consts['SWORD_DESCR'] = 'A jagged short sword that appears to have many stories to tell.'

    consts['WOODEN_SHIELD_E_DESCR'] = 'A sturdy small shield made of hard wood. It doesn\'t seem overly reliable.'
    consts['WOODEN_SHIELD_DESCR'] = 'A small shield made of wood. It doesn\'t seem overly reliable.'

    consts['DAGGER_E_DESCR'] = 'A tiny dagger with a golden guard. It is quite sharp. You have to be really close to strike with this.'
    consts['DAGGER_DESCR'] = 'A tiny dagger, rusty but still quite sharp. You have to be really close to strike with this.'

    consts['MAGICAL_WAND_E_DESCR'] = 'A magical wand, emanating arcane power from its core.'
    consts['MAGICAL_WAND_DESCR'] = 'A magical wand that can be used to channel arcane energies.'

    consts['SMALL_AXE_DESCR'] = 'An ordinary axe, small enough to be swung efficiently by one arm.'
    consts['MACE_DESCR'] = 'A dented ironwood mace. This may be used to hit stuff hard.'

    # tier 2 items
    consts['CHAINED_HELMET_DESCR'] = 'Head protection with chains covering the neck. I wouldn\'t feel safe without it...'
    consts['LEATHER_ARMOR_DESCR'] = 'A sturdy piece of body armour, although it looks a couple of sizes too large. And it reeks hideously of orc sweat.'

    consts['SHARPENED_DAGGER_E_DESCR'] = 'The dagger is very sharp and light, but it will require me to get up close to make use of it. That doesn\'t make me super excited, but whatever...'
    consts['SHARPENED_DAGGER_DESCR'] = 'The dagger is sharp and light, but it will require me to get up close to make use of it.'

    consts['WAVE_PATTERNED_SWORD_DESCR'] = 'Upon closer inspection, this sword displays a fine craftsmanship. In other words: not orc-made. Several pieces of steel have been forged together to form an intriguing pattern. It feels quite tough for its weight.'

    consts['LARGE_AXE_E_DESCR'] = 'An axe designed for combat. It it quite lightweight, and the narrow blade is sharp. Suitable to use in one hand.'
    consts['LARGE_AXE_DESCR'] = 'An axe designed for combat. Suitable to use in one hand.'

    consts['SPIKED_MACE_DESCR'] = 'The head of this mace has been shaped with metal spikes to penetrate enemy armor.'
    consts['RONDACHE_DESCR'] = 'A shield made of plates of metal and sinews.'
    consts['SHORT_STAFF_DESCR'] = 'A small staff carved from wood---perhaps oak or hazel. '
    consts['QUILTED_ARMOR_DESCR'] = 'A breastplate made of linen. It is reinforced by a metal sheet around the waist. It seems easy to move around in.'

    consts['LONGBOW_DESCR'] = 'It is about the size of a human, traditional half-moon shaped with a straight grip.'

    # tier 3 items
    consts['CHAIN_MAIL_DESCR'] = 'A coat consisting of small metal rings linked together in a pattern. Offers great protection from slashing and thrusting attacks.'
    consts['VISORED_CLOSE_HELMET_DESCR'] = 'A fully enclosing helmet with a pivoting visor and integral bevor.'
    consts['LONG_SWORD_DESCR'] = 'A steel weapon. The crossguard is solid metal, looks like it could be used for punching if needed.'
    consts['CEREMONIAL_ROBES_DESCR'] = 'The sleeves are close-fitting with ruffles, and the neckline is trimmed by a beautiful fabric.'
    consts['LARGE_SHIELD_DESCR'] = 'A metal shield large enough to provide significant protection.'
    consts['AZURE_SHIV_DESCR'] = 'A roughly crafted knife, the metal used glows faintly of sky-blue. Perhaps it is not made through mundane means...'
    consts['RUNIC_WAND_DESCR'] = 'A light rod made of metal and wood. A fine tool for channeling arcane energies.'

    consts['WAR_MACE_E_DESCR'] = 'A solid blunt weapon with significant weight. Could probably dent or penetrate metal armor.'
    consts['WAR_MACE_DESCR'] = 'A solid blunt weapon with significant weight.'

    consts['BATTLE_AXE_E_DESCR'] = 'An axe designed for combat. Its trailing lower blade edge could be used to catch the edge of an opponent\'s shield and pull it down, leaving them vulnerable.'
    consts['BATTLE_AXE_DESCR'] = 'An axe designed for combat.'

    consts['HARD_LEATHER_DESCR'] = 'A protective body armor made of hardened leather.'
    consts['CROSSBOW_DESCR'] = 'Slower to reload then a normal bow, but may fire projectiles with a greater force.'

    # tier 4 items
    consts['FULL_HELM_DESCR'] = 'The top of the helmet is curved, allowing deflection and lessening of blows.'
    consts['NOBLE_MASK_DESCR'] = 'A highly stylized theatrical-looking mask. May hold magical powers.'
    consts['BREAST_PLATE_DESCR'] = 'A metal plate armor providing high protection against all kinds of physical harassment.'
    consts['TROLLWEAVE_DESCR'] = 'A piece of body armor made from troll leather. While the smell differs from that of orcs, it is certainely.. distinct.'
    consts['CLEAVER_DESCR'] = 'A butcher\'s axe with a wide, sharpened blade.'
    consts['FALCATA_DESCR'] = 'A single-edged blade, capable of delivering a blow with the momentum of an axe, while still able to be used for thrusting attacks.'
    consts['TRIDENT_DAGGER_DESCR'] = 'A dagger with three thin blades. Triple the efficiency, huh?'
    consts['GIANT_MAUL_DESCR'] = 'A massive hammer-like weapon, able to deliver the full force of a blow against hardened steel.'
    consts['LONG_STAFF_DESCR'] = 'A long staff imbued with arcane energies.'

    consts['TOWER_SHIELD_E_DESCR'] = 'A massive rectangular shield made of plate metal and wood. It is big enough to cover most of my body.'
    consts['TOWER_SHIELD_DESCR'] = 'A massive rectangular shield made of plate metal and wood.'

    consts['DOUBLE_BOW_DESCR'] = 'It has two sets of limbs instead of one. The argument is probably that it aims better, or something.'

    # tier 5 items
    consts['WINGED_HELMET_DESCR'] = 'A steel helmet decorated with wings. It provides excellent protection from blows.'
    consts['FULL_PLATE_MAIL_DESCR'] = 'A complete body armor made of plate metal and leather. It must\'ve taken a long time to make.'
    consts['PANABA_DESCR'] = 'A large, forward-curved battle axe. If you\'ve got some chopping to do, this is your best friend.'
    consts['GREAT_SWORD_DESCR'] = 'The size of the blade permits increased range and striking power of this massive sword.'
    consts['OAKWOOD_SPIRE_DESCR'] = 'A wand with a conical structure at its top. Reach out to the skies and invoke thunderous destruction on your foes.'
    consts['GREATSHIELD_DESCR'] = 'This shield probably belong to a very important person---it looks custom-made. Its huge size provides great protection from blows and projectiles.'
    consts['ARBALEST_DESCR'] = 'A more advanced version of the crossbow; larger, and with steel limbs, providing greater force.'

    # artifacts
    consts['IVORY_VISAGE_DESCR'] = 'A curious-looking headwear, crafted out of leather, ivory and metal. You feel a strange sensation as you touch it...'
    consts['CRYSTAL_RING_DESCR'] = 'A metal ring with a crystal stone mounting. It doesn\'t seem to belong here...'
    consts['WINDSONG_SILVER_BLADE_DESCR'] = 'The blade looks fresh as if just delivered from the smith. It must have lain here for a long, long time. Its enchanting to look at.'
    consts['COWL_DIVINE_SORROW_DESCR'] = 'A long, hooded garment with wide sleeves. Arcane energies permeate this item.'
    consts['BLOODCURSED_DESCR'] = 'A strange aura surrounds this crossbow. It feels deathly chill...'
    consts['WALL_OF_THE_WICKED_DESCR'] = 'A brutal and massive shield that provides great protection from blows and projectiles.'
    consts['ORNAMENT_OF_CLARITY_DESCR'] = 'A magically enchanted device that provides mental clarity for invocations.'
    consts['DAZZLING_TRICELLITE_RING_DESCR'] = 'Whomever it belonged to, they must have paid dearly to have this made. It has several crystal-like gemstones engraved on its top.'
    consts['MAPLE_BATTLE_STAFF_DESCR'] = 'A true force of nature.'

    # rings & amulets
    consts['AMULET_OF_MAGIC_PROTECTION_E_DESCR'] = 'A piece of jewellery that provides great protection against arcane forces.'
    consts['AMULET_OF_MAGIC_PROTECTION_DESCR'] = 'A piece of jewellery that provides some protection against arcane forces.'
    consts['AMULET_OF_SPEED_DESCR'] = 'A necklace that is enchanted to give the wearer lightning-reflexes.'
    consts['RING_OF_AMPLIFICATION_DESCR'] = 'A piece of jewellery that is enchanted to greatly increase damage dealt and taken.'
    consts['RING_OF_PROTECTION_DESCR'] = 'A piece of jewellery that is enchanted to protect the wearer from blows.'
    consts['ARCANE_RING_DESCR'] = 'A piece of jewellery that is enchanted to give the wearer arcane energies.'
    consts['RING_OF_AGILITY_E_DESCR'] = 'A piece of jewellery that is enchanted to give the wearer great speed in combat.'
    consts['RING_OF_AGILITY_DESCR'] = 'A piece of jewellery that is enchanted to heighten the wearers\' reflexes in combat.'
    consts['RING_OF_EVASION_DESCR'] = 'A piece of jewellery that is enchanted to help the wearer avoid blows and projectiles.'

    # spellbooks
    consts['BOOK_ICE_CONJ_DESCR'] = 'A mysterious book depicting various incantations related to ice and cold.'
    consts['BOOK_FIRE_CONJ_DESCR'] = 'A mysterious book depicting various incantations related to fire and flames.'
    consts['BOOK_TRANSM_DESCR'] = 'A mysterious book depicting various incantations related to alchemy and transmutations.'
    consts['BOOK_HEXES_DESCR'] = 'A mysterious book depicting various incantations related to malediction and witchcraft.'
    consts['BOOK_GUSTORS_DESCR'] = 'A strange-looking book depicting various incantations.'
