import libtcodpy as libtcod
import math
import textwrap
import shelve
import random
import time
from collections import deque

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 55
LIMIT_FPS = 20
LEVEL_SCREEN_WIDTH = 60
CHARACTER_SCREEN_WIDTH = 30

#---THE MAP---#

MAP_WIDTH = 80
MAP_HEIGHT = 43

ROOM_MAX_SIZE = 5
ROOM_MIN_SIZE = 6
MAX_ROOMS = 33

#---BSP MAP---#
DEPTH = 10
MIN_SIZE = 7
FULL_ROOMS = False

#---TILE INDEX---#
wall_tile = 256 
floor_tile = 257
player_tile = 258
orc_tile = 259
troll_tile = 260
scroll_tile = 261
healingpotion_tile = 262
sword_tile = 263
shield_tile = 264
stairsdown_tile = 265
dagger_tile = 266
apple_tile = 267
healthpot_tile = 268
manapot_tile = 269
berserkpot_tile = 270
magicpot_tile = 271
scroll_tile = 272

#---FOV---#

FOV_ALGO = 0
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10
color_light_wall = libtcod.Color(130, 110, 50)
color_light_ground = libtcod.Color(200, 180, 50)
color_dark_wall = libtcod.Color(0, 0, 100)
color_dark_ground = libtcod.Color(50, 50, 150)

color_light_wall_cave = libtcod.Color(135, 90, 40)
color_light_ground_cave = libtcod.Color(140, 130, 40)
color_dark_wall_cave = libtcod.Color(0, 0, 80)
color_dark_ground_cave = libtcod.Color(40, 45, 140)

#---INTERFACE---#

BAR_WIDTH = 20
PANEL_HEIGHT = 12
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT

MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1

INVENTORY_WIDTH = 50
SPELLBOOK_WIDTH = 50
DEBUG_WIDTH = 40

#---SPELLS---#
HEAL_AMOUNT = 40
RESTORE_MANA_AMOUNT = 20

LIGHTNING_RANGE = 5
LIGHTNING_DAMAGE = 20

CHAIN_LIGHTNING_RANGE = 6
CHAIN_LIGHTNING_RADIUS = 4

CONFUSE_NUM_TURNS = 10
CONFUSE_RANGE = 5

FIREBALL_RADIUS = 3
FIREBALL_DAMAGE = 12

FIREBLAST_RADIUS = 2

MAGIC_DART_RANGE = 4

BOLT_OF_ICE_RANGE = 5

RAIN_OF_ICE_RADIUS = 6

IMMOLATE_RANGE = 6

HIBERNATION_RANGE = 5

HEX_OF_RADIANCE_RANGE = 6

RITUAL_OF_PACING_RANGE = 6

SPECTRAL_GUSHES_RANGE = 5

#---PLAYER---#
LEVEL_UP_BASE = 40
LEVEL_UP_FACTOR = 35

#---DESCRIPTIONS---#
HEALING_POTION_DESCR = 'A vial of fizzling, purple liquid. It has a faint, sweet smell that evokes pleasant memories...'
MANA_POTION_DESCR = 'The liquid looks blue as the sky. That\'s weird---sky? This place is making me forget how the surface looks like...'
POTION_OF_BERSERK_DESCR = 'Even though its sealed up pretty well with a cork, this potion emits a sickening stench... Out of all the horrible experiences Ive had so far, this smell takes the cake...'
POTION_OF_MAGIC_DESCR = 'This potion contains concentrated arcane powers. If I drink this it should boost my spellcasting significantly...for a limited time.'

SCROLL_LIGHTNING_BOLT_DESCR = 'The markings on this scroll seems to depict an Orc getting fried by lightning. Hmm...'
SCROLL_CONFUSION_DESCR = 'A scroll with esoteric symbols and what appears to be drawings of gestures. Well, someone is definitely confused...'
SCROLL_FIREBALL_DESCR = 'A fire that can never be quenched...No single Orc can escape the eternal flames!'
SCROLL_KNOWLEDGE_DESCR = 'Everything has a theory... including knowledge itself. Why don\'t I indulge already?'

ROTTEN_APPLE_DESCR = 'This item is best described as: That last apple in the fruit bowl that nobody was interested in. Indeed, it doesnt look very appealing...'
APPLE_DESCR = 'A seemingly fresh apple. Since i conjured it from thin air, I cannot guarantee it was biologically produced. But it looks tasty...'
FRENCH_FRY_DESCR = 'Well, its fried potato all right. Somebody, somewhere out there may or may not have noticed they are lacking a french fry by now...'

#---TIER 1 ITEMS---#
CAP_DESCR = 'An ordinary cap. It offers little but some light head protection and room for thoughts.'
CAPE_DESCR = 'Fashionable as it may seem, the cape offers little cover of the front. The fabric is velvet.'
ROBE_DESCR = 'A fine academic-looking regalia. It is loose-fitting and easy to move in.'

SWORD_E_DESCR = 'A fine-looking short sword that appears to have many stories to tell.'
SWORD_DESCR = 'A jagged short sword that appears to have many stories to tell.'

WOODEN_SHIELD_E_DESCR = 'A sturdy small shield made of hard wood. It doesn\'t seem overly reliable.'
WOODEN_SHIELD_DESCR = 'A small shield made of wood. It doesn\'t seem overly reliable.'

DAGGER_E_DESCR = 'A tiny dagger with a golden guard. It is quite sharp. You have to be really close to strike with this.'
DAGGER_DESCR = 'A tiny dagger, rusty but still quite sharp. You have to be really close to strike with this.'

MAGICAL_WAND_E_DESCR = 'A magical wand, emanating arcane power from its core.'
MAGICAL_WAND_DESCR = 'A magical wand that can be used to channel arcane energies.'

SMALL_AXE_DESCR = 'An ordinary axe, small enough to be swung efficiently by one arm.'
MACE_DESCR = 'A dented ironwood mace. This may be used to hit stuff hard.'

#---TIER 2 ITEMS---#
CHAINED_HELMET_DESCR = 'Head protection with chains covering the neck. I wouldn\'t feel safe without it...'
LEATHER_ARMOR_DESCR = 'A sturdy piece of body armour, although it looks a couple of sizes too large. And it reeks hideously of orc sweat.'

SHARPENED_DAGGER_E_DESCR = 'The dagger is very sharp and light, but it will require me to get up close to make use of it. That doesn\'t make me super excited, but whatever...'
SHARPENED_DAGGER_DESCR = 'The dagger is sharp and light, but it will require me to get up close to make use of it.'

WAVE_PATTERNED_SWORD_DESCR = 'Upon closer inspection, this sword displays a fine craftsmanship. In other words: not orc-made. Several pieces of steel have been forged together to form an intriguing pattern. It feels quite tough for its weight.'

LARGE_AXE_E_DESCR = 'An axe designed for combat. It it quite lightweight, and the narrow blade is sharp. Suitable to use in one hand.'
LARGE_AXE_DESCR = 'An axe designed for combat. Suitable to use in one hand.'

SPIKED_MACE_DESCR = 'The head of this mace has been shaped with metal spikes to penetrate enemy armor.'
RONDACHE_DESCR = 'A shield made of plates of metal and sinews.'
SHORT_STAFF_DESCR = 'A small staff carved from wood---perhaps oak or hazel. '
QUILTED_ARMOR_DESCR = 'A breastplate made of linen. It is reinforced by a metal sheet around the waist. It seems easy to move around in.'

LONGBOW_DESCR = 'It is about the size of a human, traditional half-moon shaped with a straight grip.'

#---TIER 3 ITEMS---#
CHAIN_MAIL_DESCR = 'A coat consisting of small metal rings linked together in a pattern. Offers great protection from slashing and thrusting attacks.'
VISORED_CLOSE_HELMET_DESCR = 'A fully enclosing helmet with a pivoting visor and integral bevor.'
LONG_SWORD_DESCR = 'A steel weapon. The crossguard is solid metal, looks like it could be used for punching if needed.'
CEREMONIAL_ROBES_DESCR = 'The sleeves are close-fitting with ruffles, and the neckline is trimmed by a beautiful fabric.'
LARGE_SHIELD_DESCR = 'A metal shield large enough to provide significant protection.'
AZURE_SHIV_DESCR = 'A roughly crafted knife, the metal used glows faintly of sky-blue. Perhaps it is not made through mundane means...'
RUNIC_WAND_DESCR = 'A light rod made of metal and wood. A fine tool for channeling arcane energies.'

WAR_MACE_E_DESCR = 'A solid blunt weapon with significant weight. Could probably dent or penetrate metal armor.'
WAR_MACE_DESCR = 'A solid blunt weapon with significant weight.'

BATTLE_AXE_E_DESCR = 'An axe designed for combat. Its trailing lower blade edge could be used to catch the edge of an opponent\'s shield and pull it down, leaving them vulnerable.'
BATTLE_AXE_DESCR = 'An axe designed for combat.'

HARD_LEATHER_DESCR = 'A protective body armor made of hardened leather.'
CROSSBOW_DESCR = 'Slower to reload then a normal bow, but may fire projectiles with a greater force.'

#---TIER 4 ITEMS---#
FULL_HELM_DESCR = 'The top of the helmet is curved, allowing deflection and lessening of blows.'
NOBLE_MASK_DESCR = 'A highly stylized theatrical-looking mask. May hold magical powers.'
BREAST_PLATE_DESCR = 'A metal plate armor providing high protection against all kinds of physical harassment.'
TROLLWEAVE_DESCR = 'A piece of body armor made from troll leather. While the smell differs from that of orcs, it is certainely.. distinct.'
CLEAVER_DESCR = 'A butcher\'s axe with a wide, sharpened blade.'
FALCATA_DESCR = 'A single-edged blade, capable of delivering a blow with the momentum of an axe, while still able to be used for thrusting attacks.'
TRIDENT_DAGGER_DESCR = 'A dagger with three thin blades. Triple the efficiency, huh?'
GIANT_MAUL_DESCR = 'A massive hammer-like weapon, able to deliver the full force of a blow against hardened steel.'
LONG_STAFF_DESCR = 'A long staff imbued with arcane energies.'

TOWER_SHIELD_E_DESCR = 'A massive rectangular shield made of plate metal and wood. It is big enough to cover most of my body.'
TOWER_SHIELD_DESCR = 'A massive rectangular shield made of plate metal and wood.'

DOUBLE_BOW_DESCR = 'It has two sets of limbs instead of one. The argument is probably that it aims better, or something.'

#---TIER 5 ITEMS---#
WINGED_HELMET_DESCR = 'A steel helmet decorated with wings. It provides excellent protection from blows.'
FULL_PLATE_MAIL_DESCR = 'A complete body armor made of plate metal and leather. It must\'ve taken a long time to make.'
PANABA_DESCR = 'A large, forward-curved battle axe. If you\'ve got some chopping to do, this is your best friend.'
GREAT_SWORD_DESCR = 'The size of the blade permits increased range and striking power of this massive sword.'
OAKWOOD_SPIRE_DESCR = 'A wand with a conical structure at its top. Reach out to the skies and invoke thunderous destruction on your foes.'
GREATSHIELD_DESCR = 'This shield probably belong to a very important person---it looks custom-made. Its huge size provides great protection from blows and projectiles.'
ARBALEST_DESCR = 'A more advanced version of the crossbow; larger, and with steel limbs, providing greater force.'

#---ARTIFACTS---#
IVORY_VISAGE_DESCR = 'A curious-looking headwear, crafted out of leather, ivory and metal. You feel a strange sensation as you touch it...'
CRYSTAL_RING_DESCR = 'A metal ring with a crystal stone mounting. It doesn\'t seem to belong here...'
WINDSONG_SILVER_BLADE_DESCR = 'The blade looks fresh as if just delivered from the smith. It must have lain here for a long, long time. Its enchanting to look at.'
COWL_DIVINE_SORROW_DESCR = 'A long, hooded garment with wide sleeves. Arcane energies permeate this item.'
BLOODCURSED_DESCR = 'A strange aura surrounds this crossbow. It feels deathly chill...'
WALL_OF_THE_WICKED_DESCR = 'A brutal and massive shield that provides great protection from blows and projectiles.'
ORNAMENT_OF_CLARITY_DESCR = 'A magically enchanted device that provides mental clarity for invocations.'
DAZZLING_TRICELLITE_RING_DESCR = 'Whomever it belonged to, they must have paid dearly to have this made. It has several crystal-like gemstones engraved on its top.'
MAPLE_BATTLE_STAFF_DESCR = 'A true force of nature.'

#---RINGS & AMULETS---#
AMULET_OF_MAGIC_PROTECTION_E_DESCR = 'A piece of jewellery that provides great protection against arcane forces.'
AMULET_OF_MAGIC_PROTECTION_DESCR = 'A piece of jewellery that provides some protection against arcane forces.'
AMULET_OF_SPEED_DESCR = 'A necklace that is enchanted to give the wearer lightning-reflexes.'
RING_OF_AMPLIFICATION_DESCR = 'A piece of jewellery that is enchanted to greatly increase damage dealt and taken.'
RING_OF_PROTECTION_DESCR = 'A piece of jewellery that is enchanted to protect the wearer from blows.'
ARCANE_RING_DESCR = 'A piece of jewellery that is enchanted to give the wearer arcane energies.'
RING_OF_AGILITY_E_DESCR = 'A piece of jewellery that is enchanted to give the wearer great speed in combat.'
RING_OF_AGILITY_DESCR = 'A piece of jewellery that is enchanted to heighten the wearers\' reflexes in combat.'
RING_OF_EVASION_DESCR = 'A piece of jewellery that is enchanted to help the wearer avoid blows and projectiles.'

#---SPELLBOOKS---#
BOOK_ICE_CONJ_DESCR = 'A mysterious book depicting various incantations related to ice and cold.'
BOOK_FIRE_CONJ_DESCR = 'A mysterious book depicting various incantations related to fire and flames.'
BOOK_TRANSM_DESCR = 'A mysterious book depicting various incantations related to alchemy and transmutations.'
BOOK_HEXES_DESCR = 'A mysterious book depicting various incantations related to malediction and witchcraft.'
BOOK_GUSTORS_DESCR = 'A strange-looking book depicting various incantations.'


		# #TIER 2 EQ
		# elif name == 'wave-patterned sword':
		# 	message('Upon closer inspection, this sword displays a fine craftsmanship. In other words: not orc-made. Several pieces of steel have been forged together to form an intriguing pattern. It feels quite tough for its weight. It gives +2 Power, +4 Defense, +4 MAX HP.', libtcod.light_gray)
		# elif name == 'rondache':
		# 	message('A board of wood with pieces of metal attached to it. Small, but tough. It doesnt weigh that much either... It gives +1 AC, +5 Defense, +6 MAX HP.', libtcod.light_gray)
		# elif name == 'sharpened dagger':
		# 	message('The dagger is sharp and light, but it will require me to get up close to make use of it. That doesnt make me super excited, but whatever... It gives +3 Power, +2 Defense, -5 MAX HP.', libtcod.light_gray)
		# elif name == 'chain mail':
		# 	message('This looks like a high quality mail. Its dense weave of iron rings should allow for good protection against edged and piercing weapons. Its not exactly feather-light, though... It gives +2 AC, -1 Defense, +8 MAX HP, -3 MAX MANA.', libtcod.light_gray)
		# elif name == 'visored close helmet':
		# 	message('The helmet is fully enclosing, and has an additional piece of plate armour to cover the neck. Sweet. I wonder if I can move my head around in this thing... It gives +2 AC, +7 MAX HP.', libtcod.light_gray)
		# elif name == 'ceremonial robes':
		# 	message('The garment is colorful with patterns resembling some kind of ancient ritual. Its material seems warm... It gives +4 Defense, +2 Magic, +4 MAX MANA', libtcod.light_gray)
		# elif name == 'ornamented short staff':
		# 	message('A wooden staff with helical patterns carved into it. It gives +3 Magic, +3 MAX MANA', libtcod.light_gray)
		# #TIER 3 EQ
		# elif name == 'vampiric long sword':
		# 	message('Dark forces emerges from this item. They are telling me to slay... It gives +2 Power, +3 Defense, +8 MAX HP, +1 Lifesteal.', libtcod.light_gray)
		# elif name == 'tower shield':
		# 	message('Its considerable size and shape should allow effective protection against both melee and ranged attacks. It gives +2 AC, +6 Defense, +9 MAX HP.', libtcod.light_gray)
		# elif name == 'azure shiv':
		# 	message('Offense is the best defense, they say... It gives +4 Power, +5 Defense, +7 MAX HP.', libtcod.light_gray)
		# elif name == 'plate mail':
		# 	message('Full body armour with steel plates. Ive seen more comfortable things, but this should provide more than enough protection for any number of orcs. It gives +3 AC, -4 Defense, +11 MAX HP, -5 MAX MANA.', libtcod.light_gray)
		# elif name == 'arcane-imbued royal tunic':
		# 	message('The arcane forces within this tunic are like no other I have ever experienced. I cant tell if thats good or bad. It gives +1 AC, +6 Defense, +3 Magic, +6 MAX MANA.', libtcod.light_gray)
		# elif name == 'long-staff of conjuring':
		# 	message('This staff has been used to perform dark Magicic. I wonder if its still safe to use it... It gives +4 Magic, +1 Power, +2 Conjuring.', libtcod.light_gray)
		# elif name == 'spiked war-mace':
		# 	message('A huge, grotesque blunt weapon that is heavy to wield. If I can muster up enough strength and swing it, it should do fine as an orc-smasher. It gives +5 Power, -2 Defense, -4 MAX HP.', libtcod.light_gray)
		# elif name == 'winged helmet':
		# 	message('The helmet of Kings. It gives +2 AC, +5 Defense, +13 MAX HP.', libtcod.light_gray)
		# #RINGS
		# elif name == 'ring of amplification':
		# 	message('You feel an immediate sensation of pain as you lay the ring in your palm to examine it. Your first instinct is to drop it, but you begin to notice pain wasnt the only thing you felt... It increases damage done and taken by its wearer by +25%', libtcod.light_gray)
		# elif name == 'ring of protection':
		# 	message('There seems to be nothing special about this ring. As you touch it however, your skin tingles and goes numb... It gives +1 AC.', libtcod.light_gray)
		# elif name == 'arcane ring':
		# 	message('You can tell this ring contains arcane power. You feel its forces propagate in the musty, thick air around you. It gives +1 Magic.', libtcod.light_gray)
		# elif name == 'ring of vigor':
		# 	message('As soon as you pick it up from the ground, you feel refreshed and extremely alert. What was that faint noise?... It gives +7 Defense, +5 MAX HP.', libtcod.light_gray)
		# #SCROLLS
		# elif name == 'a tome of Magic Dart (spell)':
		# 	message('Instruction manual on how to conjure up Magicic darts and fire them. I just touched the cover and I already feel like I have done this before...', libtcod.light_gray)
		# #ARTIFACTS
		# elif name == 'crystal ring (artifact)':
		# 	message('Whomever it belonged to, they must have paid dearly to have this made. It has several crystal-like gemstones engraved on its top. It gives +3 Power, +3 Magic, +2 Conjuring.', libtcod.white)
		# elif name == 'windsong silver blade (artifact)':
		# 	message('The blade looks fresh as if just delivered from the smith himself. It must have lain here for a long, long time. Its enchanting to look at... It gives +4 Power, +4 Defense, +2 Fighting, +10 %% resist Magic.')


#---TIME---#

time_travelers = deque()

#---CLASSES---#

class Object:
	def __init__(self, x, y, char, name, color, blocks=False, always_visible=False, fighter=None, ai=None, item=None, use_function=None, equipment=None, race=None, prof=None, trap=None, timeobj=None, loot=None):
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

	def move(self, dx, dy):
		if tilemap[self.x + dx][self.y + dy]:
			if not is_blocked(self.x + dx, self.y + dy):
				self.x += dx
				self.y += dy

	def draw(self):
		if (libtcod.map_is_in_fov(fov_map, self.x, self.y) or 
			(self.always_visible and tilemap[self.x][self.y].explored)):

			libtcod.console_set_default_foreground(con, self.color)
			libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

		elif not libtcod.map_is_in_fov(fov_map, self.x, self.y) and tilemap[self.x][self.y].explored:

			libtcod.console_put_char_ex(con, self.x, self.y, floor_tile, libtcod.grey, libtcod.black)


	def clear(self):
		if libtcod.map_is_in_fov(fov_map, self.x, self.y):
			libtcod.console_put_char_ex(con, self.x, self.y, floor_tile, libtcod.white, libtcod.black)
		elif tilemap[self.x][self.y].explored:
			libtcod.console_put_char_ex(con, self.x, self.y, floor_tile, libtcod.gray, libtcod.black)

	def move_towards(self, target_x, target_y):
		dx = target_x - self.x
		dy = target_y - self.y
		distance = math.sqrt(dx ** 2 + dy ** 2)

		dx = int(round(dx / distance))
		dy = int(round(dy / distance))
		self.move(dx, dy)

	def distance_to(self, other):
		dx = other.x - self.x
		dy = other.y - self.y
		return math.sqrt(dx ** 2 + dy ** 2)

	def send_to_back(self):
		global objects
		objects.remove(self)
		objects.insert(0, self)

	def distance(self, x, y):
		return math.sqrt((x - self.x) ** 2 + (y - self.y) **2)

	def move_astar(self, target):
		fov = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)

		for y1 in range(MAP_HEIGHT):
			for x1 in range(MAP_WIDTH):
				libtcod.map_set_properties(fov, x1, y1, not tilemap[x1][y1].block_sight, not tilemap[x1][y1].blocked)

		for obj in objects:
			if obj.blocks and obj != self and obj != target:
				libtcod.map_set_properties(fov, obj.x, obj.y, True, False)

		my_path = libtcod.path_new_using_map(fov, 1.41)

		libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)

		if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
			x, y = libtcod.path_walk(my_path, True)
			if x or y:
				self.x = x
				self.y = y
		else:
			self.move_towards(target.x, target.y)

		libtcod.path_delete(my_path)

	def move_from(self, target_x, target_y):
	#vector from object to target with distance
		dx = target_x - self.x
		dy = target_y - self.y
		distance = math.sqrt(dx ** 2 + dy ** 2)

		#normalize it to unit length then round it and convert to integer
		dx = int(round(dx / distance))
		dy = int(round(dy / distance))
		self.move(-dx, -dy)

class Tile:
	def __init__(self, blocked, block_sight = None):
		self.blocked = blocked
		self.explored = False	
		if block_sight is None: block_sight = blocked
		self.block_sight = block_sight

class Rectangle:
	def __init__(self, x, y, w, h):
		self.x1 = x
		self.y1 = y
		self.x2 = x + w
		self.y2 = y + h

	def center(self):
		center_x = (self.x1 + self.x2) / 2
		center_y = (self.y1 + self.y2) / 2
		return (center_x, center_y)

	def intersect(self, other):
		return (self.x1 <= other.x2 and self.x2 >= other.x1 and
				self.y1 <= other.y2 and self.y2 >= other.y1)

	def inner_edges(self):
		edges = []

		for x in range(self.x1+1, self.x2):
			for y in range(self.y1+1, self.y2):
				edges.append((x, y))

		for x in range(self.x1+2, self.x2-1):
			for y in range(self.y1+2, self.y2-1):
				edges.remove((x, y))

		
		for x in range(self.x1, self.x2):
			y = (self.y1+self.y2)/2
			if (x, y) in edges:
				edges.remove((x, y))

		
		for y in range(self.y1, self.y2):
			x = (self.x1+self.x2)/2
			if (x, y) in edges:
				edges.remove((x, y))

		return edges

class Fighter:
	def __init__(self, hp, defense, power, xp, armor, mana, magic, death_function=None, buff=[], lifesteal=0,
				 hp_regen=0, magic_resist=0, shielding=0, fighting=0, conjuring=0, archery=0, transmutations=0,
				 hexes=0, speed=100, evasion=0, accuracy=0, dmg_reduction=0, heal_kill=0, prof_restriction=[],
				 stunned=0, mana_regen=0):
		self.base_max_hp = hp
		self.hp = hp
		self.base_defense = defense
		self.base_power = power
		self.xp = xp
		self.base_armor = armor
		self.mana = mana
		self.base_max_mana = mana
		self.base_magic = magic

		self.death_function = death_function
		self.buff = []

		self.base_hp_regen = hp_regen
		self.base_magic_resist = magic_resist
		self.base_lifesteal = lifesteal
		self.base_evasion = evasion
		self.base_accuracy = accuracy

		self.base_shielding = shielding
		self.base_fighting = fighting
		self.base_conjuring = conjuring
		self.base_archery = archery
		self.base_transmutations = transmutations
		self.base_hexes = hexes

		self.base_speed = speed
		self.base_dmg_reduction = dmg_reduction
		self.base_heal_kill = heal_kill

		self.prof_restriction = prof_restriction
		self.stunned = stunned

		self.base_mana_regen = mana_regen
		self.mana_incrementer = 0
		self.recent_kill_window = 120

		self.stealthiness = 0

	@property
	def power(self):
		bonus = sum(equipment.power_bonus for equipment in get_all_equipped(self.owner)) + sum(buff.power_bonus for buff in get_all_buffs(self.owner))
		return self.base_power + bonus

	@property
	def defense(self):
		bonus = sum(equipment.defense_bonus for equipment in get_all_equipped(self.owner)) + sum(buff.defense_bonus for buff in get_all_buffs(self.owner))
		return self.base_defense + bonus

	@property
	def max_hp(self):
		bonus = sum(equipment.max_hp_bonus for equipment in get_all_equipped(self.owner)) + sum(buff.max_hp_bonus for buff in get_all_buffs(self.owner))
		return self.base_max_hp + self.base_fighting + bonus

	@property
	def armor(self):
		bonus = sum(equipment.armor_bonus for equipment in get_all_equipped(self.owner)) + sum(buff.armor_bonus for buff in get_all_buffs(self.owner))
		return self.base_armor + bonus

	@property
	def max_mana(self):
		bonus = sum(equipment.max_mana_bonus for equipment in get_all_equipped(self.owner)) + sum(buff.max_mana_bonus for buff in get_all_buffs(self.owner))
		return self.base_max_mana + bonus

	@property
	def magic(self):
		bonus = sum(equipment.magic_bonus for equipment in get_all_equipped(self.owner)) + sum(buff.magic_bonus for buff in get_all_buffs(self.owner))
		return self.base_magic + bonus
	
	@property
	def lifesteal(self):
		bonus = sum(equipment.lifesteal_bonus for equipment in get_all_equipped(self.owner)) + sum(buff.lifesteal_bonus for buff in get_all_buffs(self.owner))
		return self.base_lifesteal + bonus

	@property
	def hp_regen(self):
		bonus = sum(equipment.hp_regen_bonus for equipment in get_all_equipped(self.owner)) + sum(buff.hp_regen_bonus for buff in get_all_buffs(self.owner))
		return self.base_hp_regen + bonus

	@property
	def magic_resist(self):
		bonus = sum(equipment.magic_resist_bonus for equipment in get_all_equipped(self.owner)) + sum(buff.magic_resist_bonus for buff in get_all_buffs(self.owner))
		return self.base_magic_resist + bonus

	@property
	def shielding(self):
		bonus = sum(equipment.shielding_bonus for equipment in get_all_equipped(self.owner)) + sum(buff.shielding_bonus for buff in get_all_buffs(self.owner))
		return self.base_shielding + bonus

	@property
	def fighting(self):
		bonus = sum(equipment.fighting_bonus for equipment in get_all_equipped(self.owner)) + sum(buff.fighting_bonus for buff in get_all_buffs(self.owner))
		return self.base_fighting + bonus

	@property
	def conjuring(self):
		bonus = sum(equipment.conjuring_bonus for equipment in get_all_equipped(self.owner)) + sum(buff.conjuring_bonus for buff in get_all_buffs(self.owner))
		return self.base_conjuring + bonus

	@property
	def archery(self):
		bonus = sum(equipment.archery_bonus for equipment in get_all_equipped(self.owner)) + sum(buff.archery_bonus for buff in get_all_buffs(self.owner))
		return self.base_archery + bonus

	@property
	def transmutations(self):
		bonus = sum(equipment.transmutations_bonus for equipment in get_all_equipped(self.owner)) + sum(buff.transmutations_bonus for buff in get_all_buffs(self.owner))
		return self.base_transmutations + bonus

	@property
	def hexes(self):
		bonus = sum(equipment.hexes_bonus for equipment in get_all_equipped(self.owner)) + sum(buff.hexes_bonus for buff in get_all_buffs(self.owner))
		return self.base_hexes + bonus

	@property
	def speed(self):
		bonus = sum(equipment.speed_bonus for equipment in get_all_equipped(self.owner)) + sum(buff.speed_bonus for buff in get_all_buffs(self.owner))
		return self.base_speed + bonus

	@property
	def dmg_reduction(self):
		bonus = sum(equipment.dmg_reduction_bonus for equipment in get_all_equipped(self.owner)) + sum(buff.dmg_reduction_bonus for buff in get_all_buffs(self.owner))
		return self.base_dmg_reduction + bonus

	@property
	def evasion(self):
		bonus = sum(equipment.evasion_bonus for equipment in get_all_equipped(self.owner)) + sum(buff.evasion_bonus for buff in get_all_buffs(self.owner))
		return self.base_evasion + bonus

	@property
	def accuracy(self):
		bonus = sum(equipment.accuracy_bonus for equipment in get_all_equipped(self.owner)) + sum(buff.accuracy_bonus for buff in get_all_buffs(self.owner))
		return self.base_accuracy + bonus

	@property
	def heal_kill(self):
		bonus = sum(equipment.heal_kill_bonus for equipment in get_all_equipped(self.owner)) + sum(buff.heal_kill_bonus for buff in get_all_buffs(self.owner))
		return self.base_heal_kill + bonus


	def take_damage(self, damage):
		if self.dmg_reduction > 0:
				damage -= self.dmg_reduction

		if damage > 0:
			self.hp -= damage
			if self.hp <= 0:
				function = self.death_function
				if function is not None:
					function(self.owner)
					if self.owner != player:
						if player.race == 'Human':
							player.fighter.xp += int(round(self.xp * 1.33))
						else:
							player.fighter.xp += self.xp

	def attack(self, target):
		#damage spread
		i, d = divmod(self.power / 3, 1)
		#fighting bonus
		fighter_power = self.power * (0.8 + 0.05*self.fighting)

		raw_damage = fighter_power + libtcod.random_get_int(0, -i, i)

		#amplification sources
		amp_damage = sum(equipment.damage_amp_bonus for equipment in get_all_equipped(self.owner))

		#armor reduction
		dice = libtcod.random_get_int(0, 0, 20)

		if dice + target.fighter.fighting > 2 * self.power:
			#target is strong defender
			armor_reduction = 0.60 * target.fighter.armor + 0.03 * target.fighter.shielding

		else:
			#self is strong attacker
			armor_reduction = 0.35 * target.fighter.armor + 0.03 * target.fighter.shielding

		#damage equation
		red_damage = int(round((raw_damage - armor_reduction) * (1 + amp_damage)))

		if red_damage > 0:
			#missed attack depends on self.fighting and target.defense
			if target.fighter.miss_chance(self) or target.fighter.already_buffed('Asleep') is True:
				#blocking attack 		
				if target.fighter.block_chance(self) or target.fighter.already_buffed('Asleep') is True:


					message(self.owner.name.capitalize() + ' attacks ' + target.name + ': ' + str(red_damage) + ' hit points.')
					target.fighter.take_damage(red_damage)
					if target.fighter:
						for buff in target.fighter.buff:
							if buff.name == 'Asleep':
								assert isinstance(target.ai, AsleepMonster), 'Monster with Asleep buff was not AsleepMonster().'
								target.ai.take_turn(turns=2)
					
					if self.lifesteal > 0:
						self.heal(self.lifesteal)
						if self.owner.name == 'player':
							message('You lifesteal ' + str(self.lifesteal) + ' hit point(s)!')
						else:
							message(self.owner.name + ' steals ' + str(self.lifesteal) + ' hit points!', libtcod.dark_red)
				else:
					message(self.owner.name.capitalize() + ' attacks ' + target.name + ': ' + target.name + ' blocks the attack!')
			else:			
				message(self.owner.name.capitalize() + ' attacks ' + target.name + ': ' + target.name + ' dodges!')
		else:
			message(self.owner.name.capitalize() + ' attacks but it is completely ineffective!')

		#auxiliary attacks
		for buff in self.buff:
			if buff.name == 'Beastly Talons' and target.fighter:
				#perform auxiliary talon attack
				talon_mod = 0.40 + 0.08*self.transmutations
				talon_proc = libtcod.random_get_int(0, 0, 100)

				if talon_proc > (75 - 2.86*self.transmutations):

					#damage spread
					i, d = divmod(self.power / 3, 1)
					#fighting bonus
					fighter_power = self.power * (0.8 + 0.05*self.fighting)

					raw_damage = fighter_power + libtcod.random_get_int(0, -i, i)

					#amplification sources
					amp_damage = sum(equipment.damage_amp_bonus for equipment in get_all_equipped(self.owner))

					#armor reduction
					dice = libtcod.random_get_int(0, 0, 20)

					if dice + target.fighter.fighting > 1.7 * self.power + self.transmutations:
						#target is strong defender
						armor_reduction = 0.65 * target.fighter.armor + 0.03 * target.fighter.shielding

					else:
						#self is strong attacker
						armor_reduction = 0.30 * target.fighter.armor + 0.03 * target.fighter.shielding

					#damage equation
					red_damage = int(round((raw_damage - armor_reduction) * (1 + amp_damage) * talon_mod)) 

					if red_damage > 0:
						#missed attack depends on self.fighting and target.defense
						if target.fighter.miss_chance(self) or target.fighter.already_buffed('Asleep') is True:
							#blocking attack
							if target.fighter.block_chance(self) or target.fighter.already_buffed('Asleep') is True:

								message(self.owner.name.capitalize() + ' attacks ' + target.name + ' with their talons: ' + str(red_damage) + ' hit points.', libtcod.light_orange)
								target.fighter.take_damage(red_damage)
		
								if self.lifesteal > 0:
									self.heal(self.lifesteal)
									if self.owner.name == 'player':
										message('You lifesteal ' + str(self.lifesteal) + ' hit point(s)!')
									else:
										message(self.owner.name + ' steals ' + str(self.lifesteal) + ' hit points!', libtcod.light_orange)
							else:
								message(self.owner.name.capitalize() + ' attacks ' + target.name + ' with their talons: ' + target.name + ' blocks the attack!', libtcod.light_orange)
						else:			
							message(self.owner.name.capitalize() + ' attacks ' + target.name + ' with their talons: ' + target.name + ' dodges!', libtcod.light_orange)
					else:
						message(self.owner.name.capitalize() + ' attacks with their talons, but it has no effect!', libtcod.light_orange)

			elif buff.name == 'Felid Form' and target.fighter:

				claw_mod = 0.30 + 0.07*self.transmutations
				claw_proc = libtcod.random_get_int(0, 0, 100)

				bite_mod = 1.20 + 0.12*self.transmutations
				bite_proc = libtcod.random_get_int(0, 0, 100)

				if claw_proc > (65 - 1.6*self.transmutations):

					#damage spread
					i, d = divmod(self.power / 3, 1)
					#fighting bonus
					fighter_power = self.power * (0.8 + 0.05*self.fighting)

					raw_damage = fighter_power + libtcod.random_get_int(0, -i, i)

					#amplification sources
					amp_damage = sum(equipment.damage_amp_bonus for equipment in get_all_equipped(self.owner))

					#armor reduction
					dice = libtcod.random_get_int(0, 0, 20)

					if dice + target.fighter.fighting > 1.7 * self.power + self.transmutations:
						#target is strong defender
						armor_reduction = 0.70 * target.fighter.armor + 0.03 * target.fighter.shielding

					else:
						#self is strong attacker
						armor_reduction = 0.40 * target.fighter.armor + 0.03 * target.fighter.shielding

					#damage equation
					red_damage = int(round((raw_damage - armor_reduction) * (1 + amp_damage) * claw_mod)) 

					if red_damage > 0:
						#missed attack depends on self.fighting and target.defense
						if target.fighter.miss_chance(self) or target.fighter.already_buffed('Asleep') is True:
							#blocking attack					
							if target.fighter.block_chance(self) or target.fighter.already_buffed('Asleep') is True:

								message(self.owner.name.capitalize() + ' attacks ' + target.name + ' with their claws: ' + str(red_damage) + ' hit points.', libtcod.light_orange)
								target.fighter.take_damage(red_damage)
		
								if self.lifesteal > 0:
									self.heal(self.lifesteal)
									if self.owner.name == 'player':
										message('You lifesteal ' + str(self.lifesteal) + ' hit point(s)!')
									else:
										message(self.owner.name + ' steals ' + str(self.lifesteal) + ' hit points!', libtcod.dark_red)
							else:
								message(self.owner.name.capitalize() + ' attacks ' + target.name + ' with their claws: ' + target.name + ' blocks the attack!')
						else:			
							message(self.owner.name.capitalize() + ' attacks ' + target.name + ' with their claws: ' + target.name + ' dodges!')
					else:
						message(self.owner.name.capitalize() + ' attacks with their claws, but it has no effect!')

				elif bite_proc > (85 - 1.4*self.transmutations) and target.fighter:

					#damage spread
					i, d = divmod(self.power / 3, 1)
					#fighting bonus
					fighter_power = self.power * (0.8 + 0.05*self.fighting)

					raw_damage = fighter_power + libtcod.random_get_int(0, -i, i)

					#amplification sources
					amp_damage = sum(equipment.damage_amp_bonus for equipment in get_all_equipped(self.owner))

					#armor reduction
					dice = libtcod.random_get_int(0, 0, 20)

					if dice + target.fighter.fighting > 1.7 * self.power + self.transmutations:
						#target is strong defender
						armor_reduction = 0.65 * target.fighter.armor + 0.03 * target.fighter.shielding

					else:
						#self is strong attacker
						armor_reduction = 0.30 * target.fighter.armor + 0.03 * target.fighter.shielding

					#damage equation
					red_damage = int(round((raw_damage - armor_reduction) * (1 + amp_damage) * bite_mod)) 
			
					if red_damage > 0:
						#missed attack depends on self.fighting and target.defense
						if target.fighter.miss_chance(self) or target.fighter.already_buffed('Asleep') is True:
							#blocking attack depends on target.shielding and target.defense
							
							if target.fighter.block_chance(self) or target.fighter.already_buffed('Asleep') is True:

								message(self.owner.name.capitalize() + ' bites ' + target.name + ' for ' + str(red_damage) + ' hit points.', libtcod.light_orange)
								target.fighter.take_damage(red_damage)
		
								if self.lifesteal > 0:
									self.heal(self.lifesteal)
									if self.owner.name == 'player':
										message('You lifesteal ' + str(self.lifesteal) + ' hit point(s)!')
									else:
										message(self.owner.name + ' steals ' + str(self.lifesteal) + ' hit points!', libtcod.dark_red)
							else:
								message(self.owner.name.capitalize() + ' bites ' + target.name + ': ' + target.name + ' blocks the attack!')
						else:			
							message(self.owner.name.capitalize() + ' bites ' + target.name + ': ' + target.name + ' dodges!')
					else:
						message(self.owner.name.capitalize() + ' attempts to bite ' + target.name + ', but it has no effect!')

	def ranged_attack(self, target):

		#damage spread
		i, d = divmod(self.power / 3, 1)
		#fighting bonus
		fighter_power = self.power * (0.7 + 0.07*self.archery) + self.archery/2

		raw_damage = fighter_power + libtcod.random_get_int(0, -i, i)

		#amplification sources
		amp_damage = sum(equipment.damage_amp_bonus for equipment in get_all_equipped(self.owner))

		#armor reduction
		dice = libtcod.random_get_int(0, 0, 20)

		if dice + target.fighter.shielding > 2 * self.archery + self.power:
			#target is strong defender
			armor_reduction = 0.50 * target.fighter.armor + 0.03 * target.fighter.shielding

		else:
			#self is strong attacker
			armor_reduction = 0.20 * target.fighter.armor + 0.03 * target.fighter.shielding

		#damage equation
		red_damage = int(round((raw_damage - armor_reduction) * (1 + amp_damage)))
		
		miss_chance = libtcod.random_get_int(0, 0, 100)

		if red_damage > 0:
			if target.fighter.miss_chance_ranged(self):
				if target.fighter.block_chance_ranged(self):

					message(self.owner.name.capitalize() + ' fires a projectile at ' + target.name + ': ' + str(red_damage) + ' hit points.')
					target.fighter.take_damage(red_damage)
					
				else:
					message(self.owner.name.capitalize() + ' fires a projectile at ' + target.name + ': ' + target.name + ' blocks it!')	
			else:			
				message(self.owner.name.capitalize() + ' fires a projectile at ' + target.name + ' but it misses!')	
		else:
			message(self.owner.name.capitalize() + ' fires a projectile but it is completely ineffective!')

	def heal(self, amount):
		self.hp += amount
		if self.hp > self.max_hp:
			self.hp = self.max_hp

	def restore_mana(self, amount):
		self.mana += amount
		if self.mana > self.max_mana:
			self.mana = self.max_mana

	def check_buffs(self):
		global game_time
		for buff in self.buff:
			if game_time >= buff.end_time:
				self.buff.remove(buff)
				if buff.displays == True:
					message(buff.name + ' has faded.', libtcod.violet)

	def apply_buff_effects(self):

		for buff in self.buff:

			if buff.name == 'Spectral Gushes':

				if player.distance_to(self.owner) <= 5:
					amt = int(round(player.fighter.max_mana/(player.distance_to(self.owner)*2.25 + 1)))
					if amt > 0:
						player.fighter.mana += amt
						message('You extract ' + str(amt) + ' mana from the surrounding energies!', libtcod.light_blue)

			if buff.name == 'Immolate':

				message('The ' + str(self.owner.name) + ' burns for ' + str(-buff.hp_regen_bonus) + ' hit points!', libtcod.orange)
				self.take_damage(-buff.hp_regen_bonus) # equivalent to self.heal(buff.hp_regen_bonus)
				message('The ' + self.owner.name + ' has ' + str(self.hp) + ' hp.')

			if buff.name == 'Hex Of Radiance':

				for monster in objects:
					if monster.fighter and monster.distance_to(self.owner) <= 5 and monster != player:
						chance = libtcod.random_get_int(0, 0, 100) + player.fighter.hexes*2
						if chance > 14 + monster.fighter.magic_resist*100:
							dmg = int(round((libtcod.random_get_int(0, 1, 3) + int(round(player.fighter.magic*0.3 + player.fighter.hexes*0.5))) * (1 - monster.fighter.magic_resist)))
							monster.fighter.take_damage(dmg)
							message(str(monster.name).capitalize() + ' burns for ' + str(dmg) + ' hit points!', libtcod.orange)
						else:
							message(str(monster.name).capitalize() + ' resists the effects of magical radiance!', libtcod.red)

			if buff.name == 'Immolation':
				if self.owner == player:
					message('You burn for 3 hit points!', libtcod.orange)
				else:
					message('The ' + self.owner.name + ' burns for 3 hit points!', libtcod.orange)
				self.take_damage(3)

			if buff.name == 'Satiated' and player.fighter.hp < player.fighter.max_hp:
				message('You gain 1 hit point.', libtcod.light_violet)
				player.fighter.heal(1)

			if buff.name == 'Bleeding':
				message('You lose 1 hit point due to bleeding!', libtcod.light_red)
				player.fighter.take_damage(1)

			
			if buff.name == 'Divination of Warmth' and player.fighter.hp < player.fighter.max_hp:
				message('You gain ' + str(buff.hp_regen_bonus) + ' hit points from Divination of Warmth!', libtcod.light_violet)
				player.fighter.heal(buff.hp_regen_bonus)

			if buff.name == 'White Light':
				for obj in objects:
					if obj.fighter and obj.distance_to(self.owner) <= 6 and obj != player and libtcod.map_is_in_fov(fov_map, obj.x, obj.y):
						damage = int(round((3 + player.fighter.conjuring * 0.65 + player.fighter.magic * 0.25)*(1 - obj.fighter.magic_resist)))
						for b in obj.fighter.buff:
							if b.name == 'Blinded':
								b.end_time = game_time + 5
								break
						else:
							inacc = 50 + player.fighter.conjuring*2.5
							inacc_buff = Buff('Blinded', accuracy_bonus=-inacc, end_time=game_time+5)
							obj.fighter.buff.append(inacc_buff)
							message('The ' + obj.name + ' is utterly blinded!', libtcod.light_blue)
						if (obj.fighter.magic_resist*100 + 7 > player.fighter.conjuring*2 + libtcod.random_get_int(0, 0, 100)):
							message('The ' + obj.name + ' resists the burning light with effort.', libtcod.yellow)
						obj.fighter.take_damage(damage)
						message('The ' + obj.name + ' burns for ' + str(damage) + ' points of damage.', libtcod.orange)

	def regenerate_tick(self):
		# only regenerate after recently slaying enemies
		if self.recent_kill_window > 0:
			# do not regenerate mana when at maximum capacity or at no capacity
			if (self.mana < self.max_mana and self.max_mana > 0):
				self.mana_incrementer += self.base_mana_regen
				while self.mana_incrementer >= 1:
					self.mana_incrementer -= 1
					self.mana += 1
				self.recent_kill_window -= 1

	def reset_kill_window(self):
		self.recent_kill_window = 120

	def already_buffed(self, name):
		for buff in self.buff:
			if buff.name == name:
				return True
		return False

	def is_transformed(self):
		for buff in self.buff:
			if buff.transm == True:
				return True
		return False

	#---COMBAT---#

	def block_chance(self, attacker):

		dice = libtcod.random_get_int(0, 0, 100)

		if self.owner == player:
			for equip in get_all_equipped(player):
				if equip.is_equipped and equip.slot == 'left hand':

					base_chance = 8
			else:
				base_chance = 0
		else:
			base_chance = 0

		if self.owner.prof == 'Fighter':
			shield_mod = 1.10 + 0.03*self.shielding
		elif self.owner.prof in ['Stalker', 'Alchemist']:
			shield_mod = 1.00 + 0.02*self.shielding
		else:
			shield_mod = 0.90 + 0.02*self.shielding

		block_mod = (self.shielding + self.defense*0.35)*shield_mod

		attack_mod = attacker.fighting

		chance = int(round(base_chance + block_mod - attack_mod))

		if dice > chance:
			#didnt block
			return True
		return False

	def miss_chance(self, attacker):

		dice = libtcod.random_get_int(0, 0, 100)

		base_chance = 8

		# was 0.30
		miss_mod = 0.5*self.fighting + (0.33 + 0.03*self.shielding)*self.defense + self.evasion

		attack_mod = attacker.fighting + attacker.accuracy

		chance = int(round(base_chance + miss_mod - attack_mod))

		if dice > chance:
			#didnt miss
			return True
		return False

	def miss_chance_ranged(self, attacker):

		dice = libtcod.random_get_int(0, 0, 100)

		base_chance = 17

		# was 0.20
		miss_mod = (0.55 + 0.03*self.shielding)*self.defense + self.evasion

		attack_mod = attacker.archery + attacker.accuracy

		chance = int(round(base_chance + miss_mod - attack_mod))

		if dice > chance:
			return True
		return False

	def block_chance_ranged(self, attacker):

		dice = libtcod.random_get_int(0, 0, 100)

		if self.owner == player:
			for equip in get_all_equipped(player):
				if equip.is_equipped and equip.slot == 'left hand':

					base_chance = 5
			else:
				base_chance = 0
		else:
			base_chance = 0

		if self.owner.prof == 'Fighter':
			shield_mod = 0.9 + 0.03*self.shielding
		elif self.owner.prof in ['Stalker', 'Alchemist']:
			shield_mod = 0.8 + 0.02*self.shielding
		else:
			shield_mod = 0.7 + 0.02*self.shielding

		block_mod = (self.shielding + self.defense*0.35)*shield_mod

		attack_mod = attacker.archery

		chance = int(round(base_chance + block_mod - attack_mod))

		if dice > chance:
			#didnt block
			return True
		return False

class BasicMonster:
	def take_turn(self):
		monster = self.owner
		if stealth_roll(monster):
			return 100
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			if monster.distance_to(player) >= 2:
				monster.move_astar(player)

			elif player.fighter.hp > 0:
				monster.fighter.attack(player)

		elif monster.distance_to(player) <= 10:
			monster.move_astar(player)

		else:
			dice = libtcod.random_get_int(0, 0, 10)
			if dice == 1:
				(x, y) = (libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))
				monster.move(x, y)

		return 100

class BasicMonsterBleed:
	def take_turn(self):
		global game_time
		monster = self.owner
		if stealth_roll(monster):
			return 100
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			if monster.distance_to(player) >= 2:
				monster.move_astar(player)
			elif player.fighter.hp > 0:
				attack = monster.fighter.attack(player)  
				if attack == 'hit':
					dice = libtcod.random_get_int(0, 0, 100)
					if dice < 17:
						if player.fighter.already_buffed('Bleeding') is not True:
							dur = game_time + 6 + libtcod.random_get_int(0, 1, 7)
							buff = Buff('Bleeding', hp_regen_bonus=-1, end_time=dur)
							message('The ' + monster.name + ' bites you! You begin to bleed from the opened wound.', libtcod.red)
							player.fighter.buff.append(buff)
		else:
			dice = libtcod.random_get_int(0, 0, 10)
			if dice == 1:
				(x, y) = (libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))
				monster.move(x, y)
		return 100

class BasicMonsterDrain:
	def take_turn(self):
		global game_time
		monster = self.owner
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			if monster.distance_to(player) >= 2:
				monster.move_astar(player)
			elif player.fighter.hp > 0:
				attack = monster.fighter.attack(player)  
				if attack == 'hit':
					dice = libtcod.random_get_int(0, 0, 100)
					if dice < 10:
						if player.fighter.already_buffed('Drain') is not True:
							dur = game_time + 60 + libtcod.random_get_int(0, 40, 120)
							buff = Buff('Drain', power_bonus=-1, magic_bonus=-1, end_time=dur)
							message('The ' + monster.name + ' drains your energy! Losing 1 Power and 1 Magic.', libtcod.red)
							player.fighter.buff.append(buff)
		else:
			dice = libtcod.random_get_int(0, 0, 10)
			if dice == 1:
				(x, y) = (libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))
				monster.move(x, y)
		return 100

class HunterMonster:
	def take_turn(self):
		monster = self.owner
		if monster.distance_to(player) >= 2:
			monster.move_astar(player)

		elif player.fighter.hp > 0:
			monster.fighter.attack(player)
		
		return 100
 
class RangedMonster:
	def take_turn(self):
		monster = self.owner
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			dice = libtcod.random_get_int(0, 0, 100)
			if dice > 30:
				if monster.distance_to(player) < 5:
					pos = (monster.x, monster.y)
					monster.move_from(player.x, player.y)
					new_pos = (monster.x, monster.y)
					if pos == new_pos and monster.distance_to(player) < 2:
						(x, y) = (libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))
						monster.move(x, y)

				elif monster.distance_to(player) >= 6:
					monster.move_astar(player)

			elif monster.distance_to(player) >= 2:
				if monster.distance_to(player) < 6:
					monster.fighter.ranged_attack(player)

				else:
					monster.move_astar(player)

			else:
				monster.fighter.attack(player)

		return 100

class FrozenMonster:
	def __init__(self, old_ai, old_color, num_turns):
		self.old_ai = old_ai
		self.num_turns = num_turns
		self.old_color = old_color

	def take_turn(self):
		if self.num_turns > 0:
			self.num_turns -= 1

		else:
			self.owner.ai = self.old_ai
			self.owner.color = self.old_color
			message('The ' + self.owner.name + ' is no longer frozen!', libtcod.red)
		
		return 100

class CasterMonster:
	def take_turn(self):
		global game_time, tilemap
		monster = self.owner
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			dice = libtcod.random_get_int(0, 0, 100)

			if dice <= 10: 
	
				x = libtcod.random_get_int(0, -1, 1) + monster.x
				y = libtcod.random_get_int(0, -1, 1) + monster.y

				if tilemap[x][y] and not is_blocked(x, y):
					fighter_component = Fighter(hp=25, defense=3, power=5, xp=0, armor=0, mana=0, magic=0, death_function=monster_death, lifesteal=0)
					ai_component = BasicMonster()
					time_component = TimeObj(0, 90)
					summon = Object(x, y, 'u', 'undead Orc', libtcod.desaturated_green, blocks=True, fighter=fighter_component, ai=ai_component, 
									timeobj=time_component)
					summon.timeobj.register()
					objects.append(summon)
					message('The lich raises the dead...!', libtcod.red)
				else:
					monster.move_from(player.x, player.y)
				return 100
			
			elif dice <= 10 + 5:

				if player.fighter.already_buffed('Curse of the lich'):
						monster.move_from(player.x, player.y)
				else:
					resist_chance = libtcod.random_get_int(0, 0, 100)
					if resist_chance + 2 > player.fighter.magic_resist*100:
						dur = game_time + 20
						buff = Buff( 'Curse of the lich', armor_bonus=-3, end_time=dur)
						player.fighter.buff.append(buff)
						message('The ' + monster.name + ' gestures at you.', libtcod.light_purple)
						message('You are cursed! You feel move vulnerable.', libtcod.red)
					else:
						message('The ' + monster.name + ' attempts to curse you but you resist it completely!', libtcod.yellow)

				return 100

			elif dice <= 10 + 5 + 40:

				if monster.distance_to(player) < 5:
					dice = libtcod.random_get_int(0, 0, 100)
					if dice <= 10:
						resist_chance = libtcod.random_get_int(0, 0, 100)
						if resist_chance + 2 > player.fighter.magic_resist * 100:
							damage = int(round(libtcod.random_get_int(0, 24, 37) * (1 - player.fighter.magic_resist)))
							player.fighter.take_damage(damage)
							message('The lich hits you with a blast of ice! You suffer ' + str(damage) + ' points of damage!', libtcod.light_blue)
						else:
							message('The lich attempts to blast you with ice, but you resist completely!', libtcod.yellow)
					elif monster.distance_to(player) < 2:
						monster.fighter.attack(player)
					else:
						x = libtcod.random_get_int(0, -1, 1)
						y = libtcod.random_get_int(0, -1, 1)
						monster.move(x, y)
				else:
					x = libtcod.random_get_int(0, -1, 1)
					y = libtcod.random_get_int(0, -1, 1)
					monster.move(x, y)

				return 100

			else:
				if monster.distance_to(player) < 2:
					monster.fighter.attack(player)
				else:
					monster.move_from(player.x, player.y)
				return 100
		return 100

class TrollHealer:
	def take_turn(self):
		global game_time
		monster = self.owner
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			dice = libtcod.random_get_int(0, 0, 100)
			if dice > 80 and monster.fighter.hp < monster.fighter.max_hp:
				if monster.fighter.already_buffed('Troll regeneration') is True:
						if monster.distance_to(player) >= 2:
							monster.move_astar(player)
						elif player.fighter.hp > 0:
							monster.fighter.attack(player)
				else:
					dur = game_time + 10
					buff = Buff('Troll regeneration', hp_regen_bonus=2, end_time=dur)
					monster.fighter.buff.append(buff)
					message('The ' + str(monster.name) + ' casts ' + str(buff.name) + '!', libtcod.red)

				return 100
			
			elif monster.distance_to(player) >= 2:
				monster.move_astar(player)
				return 100
			elif player.fighter.hp > 0:
				monster.fighter.attack(player)
				return 100
		return 100

class OrcCaster:
	def take_turn(self):
		global game_time
		monster = self.owner
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			dice = libtcod.random_get_int(0, 0, 100)
			if dice > 84 and monster.distance_to(player) < 6:
				dice2 = libtcod.random_get_int(0, 0, 100)
				if dice2 > 60:
					if player.fighter.already_buffed('Immolation') is True:
						if monster.distance_to(player) < 2:
							monster.fighter.attack(player)
						else:
							monster.move_from(player.x, player.y)
					else:
						dur = game_time + libtcod.random_get_int(0, 5, 9) 
						buff = Buff('Immolation', hp_regen_bonus=-3, end_time=dur)
						player.fighter.buff.append(buff)
						message('The ' + str(monster.name) + ' immolates you!', libtcod.red)
				else:
					damage = int(round(libtcod.random_get_int(0, 15, 22) * (1 - player.fighter.magic_resist)))
					dice3 = libtcod.random_get_int(0, 0, 100)
					if dice3 > player.fighter.magic_resist * 100:
						player.fighter.take_damage(damage)
						message('The orc warlock launches a bolt of concentrated arcane power at you! You suffer ' + str(damage) + ' points of damage!', libtcod.light_blue)
					else:
						message('The orc warlock launches a bolt of concentrated arcane power at you, but you shrug it off!', libtcod.yellow)

			elif monster.distance_to(player) < 2:
				monster.fighter.attack(player)
			elif monster.distance_to(player) < 6:
				monster.move_from(player.x, player.y)
			else:
				monster.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))

		return 100

class PainCaster:
	def take_turn(self):
		global game_time
		monster = self.owner
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			dice = libtcod.random_get_int(0, 0, 100)
			if dice < 11 and monster.distance_to(player) < 7:
				resist_chance = libtcod.random_get_int(0, 0, 100)
				if resist_chance + 4 > player.fighter.magic_resist*100:
					damage = int(round(player.fighter.hp * 0.45 * (1 - player.fighter.magic_resist)))
					if damage > 0:
						player.fighter.take_damage(damage)
						message('Your vision blurs from excruciating pain!! You suffer ' + str(damage) + ' points of damage!', libtcod.red)
				else:
					message('The ' + str(monster.name) + ' attempts to permeate you with pain, but you manage to resist it!', libtcod.yellow)

			elif monster.distance_to(player) < 2:
				dice2 = libtcod.random_get_int(0, 0, 100)
				if dice2 < 58:
					monster.fighter.attack(player)
				else:

					(x, y) = (monster.x + libtcod.random_get_int(0, -3, 3), monster.y + libtcod.random_get_int(0, -3, 3))

					if tilemap[x][y]:
						if tilemap[x][y].blocked == False and libtcod.map_is_in_fov(fov_map, monster.x, monster.y) and x != player.x and y != player.y:
							(monster.x, monster.y) = (x, y)
							message('The demonspawn emits a blinding light and reappears at another location!', libtcod.violet)
							return
						else:
							monster.fighter.attack(player)
					else:
						monster.fighter.attack(player)
					
			elif monster.distance_to(player) < 6:
				monster.move_from(player.x, player.y)
			else:
				monster.move_astar(player)
		return 100

class PainCaster_2:
	def take_turn(self):
		global game_time
		monster = self.owner
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			dice = libtcod.random_get_int(0, 0, 100)
			if dice < 12 and monster.distance_to(player) < 7:
				resist_chance = libtcod.random_get_int(0, 0, 100)
				if resist_chance + 4 > player.fighter.magic_resist*100:

					damage = int(round(player.fighter.hp * 0.45 * (1 - player.fighter.magic_resist)))
					if damage > 0:
						player.fighter.take_damage(damage)
						message('Your vision blurs from excruciating pain!! You suffer ' + str(damage) + ' points of damage!', libtcod.red)
				else:
					message('The ' + str(monster.name) + ' attempts to permeate you with pain, but you manage to resist it!', libtcod.yellow)

			elif monster.distance_to(player) < 2 and dice < 85:
				dice2 = libtcod.random_get_int(0, 0, 100)
				if dice2 < 55:
					monster.fighter.attack(player)
				else:

					(x, y) = (monster.x + libtcod.random_get_int(0, -3, 3), monster.y + libtcod.random_get_int(0, -3, 3))

					if tilemap[x][y]:
						if tilemap[x][y].blocked == False and libtcod.map_is_in_fov(fov_map, monster.x, monster.y) and x != player.x and y != player.y:
							(monster.x, monster.y) = (x, y)
							message('The demon emits a blinding light and reappears at another location!', libtcod.violet)
							return
						else:
							monster.fighter.attack(player)
					else:
						monster.fighter.attack(player)

			elif dice > 85 and monster.distance_to(player) < 7:
				magic_resist = libtcod.random_get_int(0, 0, 100)
				if magic_resist + 4 > player.fighter.magic_resist*100:

					damage = int(round(libtcod.random_get_int(0, 35, 50) * (1 - player.fighter.magic_resist)))
					if damage > 0:
						player.fighter.take_damage(damage)
						message('The demon hits you with a flaming projectile! You suffer ' + str(damage) + ' points of damage!', libtcod.orange)
				else:
					message('The demon fires a flaming projectile, but you shrug it off!', libtcod.yellow)

			elif monster.distance_to(player) < 2:
				monster.fighter.attack(player)
			else:
				monster.move_astar(player)
		return 100

class MalignantSpiritMonster:

	def __init__(self):

		self.cooldown = 8
		self.timer = 0

	def take_turn(self):
		global game_time
		monster = self.owner
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			dice = libtcod.random_get_int(0, 0, 100)
			if dice > 76 and monster.distance_to(player) < 6:
				dice2 = libtcod.random_get_int(0, 0, 100)
				if dice2 > 62:
					if player.fighter.already_buffed('Blur') is True:
						if monster.distance_to(player) < 2:
							monster.fighter.attack(player)
						else:
							monster.move_astar(player)
					else:
						dur = game_time + libtcod.random_get_int(0, 16, 24) 
						buff = Buff('Spectral Disruption', defense_bonus=-10, magic_resist_bonus=-0.30, end_time=dur)
						for other in player.fighter.buff:
							if other.name == 'Spectral Disruption':
								message('The ' + str(monster.name) + ' mumbles some strange words.', libtcod.red)
							break
						else:
							player.fighter.buff.append(buff)
							message('The ' + str(monster.name) + ' lets out a deafening shriek as it gazes towards you! You feel weaker...', libtcod.red)
						
				elif dice2 > 20 and self.timer == 0:
					damage = int(round(libtcod.random_get_int(0, 15, 24) * (1 - player.fighter.magic_resist)))
					dice3 = libtcod.random_get_int(0, 0, 100)
					if dice3 > player.fighter.magic_resist * 100:
						player.fighter.take_damage(damage)
						player.fighter.stunned += 1
						message('The ' + str(monster.name) + ' emits a flash of light that stuns you! You are unable to act for 1 turn and suffer ' + str(damage) + ' points of damage!', libtcod.light_blue)
					else:
						message('The ' + str(monster.name) + ' emits a flash of light, attempting to stun you but you shrug it off!', libtcod.yellow)
					self.timer += self.cooldown
						
				else:
					if monster.fighter.max_hp - monster.fighter.hp >= 30:
						if not monster.fighter.already_buffed('Protective Barrier'):

							dur = libtcod.random_get_int(0, 5, 8) + game_time

							message('The ' + str(monster.name) + ' evokes a powerful protective barrier around it!', libtcod.red)
							buff = Buff('Protective Barrier', armor_bonus=5, magic_resist_bonus=0.5, end_time=dur)
							monster.fighter.buff.append(buff)

					elif monster.distance_to(player) < 2:
						monster.fighter.attack(player)
					else:
						monster.move_astar(player)


			elif monster.distance_to(player) < 2:
				monster.fighter.attack(player)
			elif monster.distance_to(player):
				monster.move_astar(player)
			else:
				monster.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))

		if self.timer > 0: self.timer -= 1
		return 100

class Item:

	def __init__(self, name=None, use_function=None, material=False):
		self.name = name
		self.use_function = use_function
		self.material = material
		self.description = ''

	def pick_up(self):
		if len(inventory) >= 26:
			message('Your inventory is full, unable to pick up ' + self.owner.name + '.', libtcod.red)
		else:
			inventory.append(self.owner)
			objects.remove(self.owner)
			message('You picked up a ' + self.owner.name + '.', libtcod.green)
			equipment = self.owner.equipment

	def use(self):
		if self.owner.equipment:
			if not self.owner.equipment.prof_restriction:
				self.owner.equipment.toggle_equip()
				took_turn()
				return
			elif player.prof not in self.owner.equipment.prof_restriction:
				message('You cannot make use of this item!', libtcod.red)
				return
			else:
				self.owner.equipment.toggle_equip()
				took_turn()
				return
		elif self.use_function is None:
			message('The ' + self.owner.name + ' cannot be used.')
			return
		elif self.use_function() != 'cancelled':
			inventory.remove(self.owner)
			if self.name is not None:
				append_spell(self.name)
		


	def drop(self):
		objects.append(self.owner)
		inventory.remove(self.owner)
		self.owner.x = player.x
		self.owner.y = player.y
		message('You dropped a ' + self.owner.name + '.', libtcod.yellow)
		if self.owner.equipment:
			self.owner.equipment.dequip()

	def inspect(self):
		if self.owner.equipment:
			item = self.owner.equipment
			stats_list = []
			if item.power_bonus != 0:
				stats_list.append(str(item.power_bonus) + ' Power')
			if item.defense_bonus != 0:
				stats_list.append(str(item.defense_bonus) + ' Defense')
			if item.armor_bonus != 0:
				stats_list.append(str(item.armor_bonus) + ' AC')
			if item.magic_bonus != 0:
				stats_list.append(str(item.magic_bonus) + ' Magic')
			if item.max_hp_bonus != 0:
				stats_list.append(str(item.max_hp_bonus) + ' Max HP')
			if item.max_mana_bonus != 0:
				stats_list.append(str(item.max_mana_bonus) + ' Max Mana')
			if item.fighting_bonus != 0:
				stats_list.append(str(item.fighting_bonus) + ' Fighting')
			if item.shielding_bonus != 0:
				stats_list.append(str(item.shielding_bonus) + ' Shielding')
			if item.conjuring_bonus != 0:
				stats_list.append(str(item.conjuring_bonus) + ' Conjuring')
			if item.archery_bonus != 0:
				stats_list.append(str(item.archery_bonus) + ' Archery')
			if item.hexes_bonus != 0:
				stats_list.append(str(item.hexes_bonus) + ' Hexes')

			if item.evasion_bonus != 0:
				stats_list.append(str(item.evasion_bonus) + ' Evasion')
			if item.accuracy_bonus != 0:
				stats_list.append(str(item.accuracy_bonus) + ' Accuracy')
			if item.speed_bonus != 0:
				stats_list.append(str(item.speed_bonus) + ' Speed')
			if item.dmg_reduction_bonus != 0:
				stats_list.append('All physical damage taken reduced by ' + str(item.dmg_reduction_bonus))
			if item.heal_kill_bonus != 0:
				stats_list.append('Chance to restore health or mana on kill')


			if item.magic_resist_bonus != 0:
				stats_list.append(str(item.magic_resist_bonus*100) + ' %% Magic Resistance')
			if item.lifesteal_bonus != 0:
				stats_list.append(str(item.lifesteal_bonus) + ' Lifesteal')

			string = ', '.join(stats_list)
		else:
			string = ''
		
		youseea = 'You see a'
		if self.owner.name[0] in 'aeiouAEIOU':
			youseea += 'n '
		else:
			youseea += ' '
		if string != '':
			text = youseea + self.owner.name + '. ' + self.description + ' It yields ' + string + '.'
		else:
			text = youseea + self.owner.name + '. ' + self.description
		message(text, libtcod.light_gray)
		
class ConfusedMonster:
	def __init__(self, old_ai, num_turns=CONFUSE_NUM_TURNS, stealth=False):
		self.old_ai = old_ai
		self.num_turns = num_turns
		self.stealth = stealth

	def take_turn(self):
		if self.num_turns > 0:
			dice = libtcod.random_get_int(0, 0, 100)
			if dice > 70:
				self.owner.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))

			self.num_turns -=1
		else:
			self.owner.ai = self.old_ai
			
			if libtcod.map_is_in_fov(fov_map, player.x, player.y):
				message('The ' + self.owner.name + ' is no longer confused!', libtcod.red)

		return 100

class StealthMonster:
	def __init__(self, old_ai, num_turns):
		self.old_ai = old_ai
		self.num_turns = num_turns

	def take_turn(self):

		monster = self.owner

		if self.num_turns > 0:

			dur = libtcod.random_get_int(0, 1, 3)

			if player.fighter.transmutations >= 10:
				dur -= 1

			dice = libtcod.random_get_int(0, 0, 20)

			if dice > 6:

				self.owner.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))

			else:

				detect_chance = libtcod.random_get_int(0, 0, 20) + int(round((monster.fighter.power/2))) - int(0.5*monster.distance_to(player)**2)

				if detect_chance > libtcod.random_get_int(0, 0, 20) + player.level*2 + int(round(player.fighter.transmutations*1.5)) - 1:
					monster.ai = self.old_ai
					message('The ' + monster.name + ' detects you!', libtcod.red)
				else:
					self.num_turns -= dur
		else:
			monster.ai = self.old_ai
			if libtcod.map_is_in_fov(fov_map, self.owner.x, self.owner.y):
				message('The ' + monster.name + ' detects you!', libtcod.red)

		return 100

class AsleepMonster:
	def __init__(self, old_ai, num_turns, otc=0):
		self.old_ai = old_ai
		self.num_turns = num_turns
		self.otc = otc

	def take_turn(self, turns=1):

		monster = self.owner
		#for one turn, magical sleep cannot be broken
		

		if self.num_turns > 0:

			if self.otc == 1:

				awake_chance = libtcod.random_get_int(0, 0, 20) + int(round(monster.fighter.power/2)) - int(round(monster.distance_to(player)))

				cast_mod = 2*player.level + 2*player.fighter.hexes

				if awake_chance > 2*player.level + 2*player.fighter.hexes + 3:

					monster.ai = self.old_ai
					for buff in monster.fighter.buff:
						if buff.name == 'Asleep':
							monster.fighter.buff.remove(buff)

					if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

						message('The ' + str(monster.name) + ' suddenly awakes!', libtcod.red)
				else:
					turn_mod = libtcod.random_get_int(0, 1, 3)
					self.num_turns -= (turn_mod + turns - 1)

			else:
				turn_mod = libtcod.random_get_int(0, 1, 3)
				self.num_turns -= (turn_mod + turns - 1)
				self.otc = 1
		
		else:
			self.owner.ai = self.old_ai

			for buff in monster.fighter.buff:
				if buff.name == 'Asleep':
					monster.fighter.buff.remove(buff)

			if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
				message('The ' + str(monster.name) + ' awakes from its slumber!', libtcod.red)

		return 100

class Equipment:
	def __init__(self, slot, power_bonus=0, defense_bonus=0, armor_bonus=0, max_mana_bonus=0, magic_bonus=0, max_hp_bonus=0, lifesteal_bonus=0, damage_amp_bonus=0, magic_resist_bonus=0, fighting_bonus=0, shielding_bonus=0, conjuring_bonus=0, archery_bonus=0, transmutations_bonus=0, hexes_bonus=0, speed_bonus=0, dmg_reduction_bonus=0, evasion_bonus=0, accuracy_bonus=0, heal_kill_bonus=0, prof_restriction=None):
		self.slot = slot
		self.power_bonus = power_bonus
		self.defense_bonus = defense_bonus
		self.armor_bonus = armor_bonus
		self.max_mana_bonus = max_mana_bonus
		self.magic_bonus = magic_bonus
		self.max_hp_bonus = max_hp_bonus
		self.lifesteal_bonus = lifesteal_bonus
		self.damage_amp_bonus = damage_amp_bonus
		self.magic_resist_bonus = magic_resist_bonus
		self.fighting_bonus = fighting_bonus
		self.shielding_bonus = shielding_bonus
		self.conjuring_bonus = conjuring_bonus
		self.archery_bonus = archery_bonus
		self.transmutations_bonus = transmutations_bonus
		self.hexes_bonus = hexes_bonus
		self.evasion_bonus = evasion_bonus
		self.accuracy_bonus = accuracy_bonus

		self.speed_bonus = speed_bonus
		self.dmg_reduction_bonus = dmg_reduction_bonus
		self.heal_kill_bonus = heal_kill_bonus

		self.prof_restriction = prof_restriction
		self.is_equipped = False

	def toggle_equip(self):
		if self.is_equipped:
			self.dequip()
		else:
			self.equip()

	def equip(self):
		old_equipment = get_equipped_in_slot(self.slot)
		if old_equipment is not None:
			old_equipment.dequip()
		self.is_equipped = True
		message('Equipped ' + self.owner.name + ' on ' + self.slot + '.', libtcod.light_green)

	def dequip(self):
		if not self.is_equipped: return
		self.is_equipped = False
		message('Dequipped ' + self.owner.name + ' from ' + self.slot + '.', libtcod.light_yellow)

class Spell:

	def __init__(self, name, cost, use_function=None, school=None, level=0):
		
		self.name = name
		self.cost = cost
		self.use_function = use_function
		self.school = school
		self.level = level

	def cast(self):
		cost_mod = 0
		#check if use function is defined
		if self.use_function is None:
			message('You cannot cast this spell.')

		#check for divination of warmth
		for buff in player.fighter.buff:
			if buff.name == 'Divination of Warmth':
				cost_mod += 2
		#check mana for spell cost
		if player.fighter.mana < (self.cost - cost_mod):
				message('You do not have enough mana!', libtcod.red)
				return

		elif self.spell_check() is False:
				message('Your fingertips faintly sparks but fizzles out! You fumbled to cast ' + str(self.name) + '!', libtcod.red)
				if (self.cost - cost_mod) > 0:
					player.fighter.mana -= (self.cost - cost_mod)
				if player.fighter.mana < 0:
					player.fighter.mana = 0
				took_turn()
				return

		elif self.use_function() == 'cancelled':
			return

		if (self.cost - cost_mod) > 0:
			player.fighter.mana -= (self.cost - cost_mod)
		if player.fighter.mana < 0:
			player.fighter.mana = 0
		took_turn()

	def spell_check(self):
		if self.school == 'Conjurations':
			intel = player.fighter.magic*0.3 + player.fighter.conjuring*1.25

		elif self.school == 'Transmutations':
			intel = player.fighter.magic*0.3 + player.fighter.transmutations*1.25

		elif self.school == 'Hexes':
			intel = player.fighter.magic*0.3 + player.fighter.hexes*1.25

		elif self.school is None:
			intel = player.fighter.magic*0.5 + player.level

		dice = libtcod.random_get_int(0, 0, 20)
		if dice + intel > self.level * 1.75 + 1: 
			return True
		else:
			return False

class Buff:
	def __init__(self, name, color=libtcod.white, power_bonus=0, defense_bonus=0, armor_bonus=0, max_mana_bonus=0, magic_bonus=0, max_hp_bonus=0, lifesteal_bonus=0, hp_regen_bonus=0, magic_resist_bonus=0, fighting_bonus=0, shielding_bonus=0, conjuring_bonus=0, archery_bonus=0, transmutations_bonus=0, hexes_bonus=0, speed_bonus=0, dmg_reduction_bonus=0, evasion_bonus=0, accuracy_bonus=0, heal_kill_bonus=0, transm=False, end_time=0, displays=True):
		self.power_bonus = power_bonus
		self.defense_bonus = defense_bonus
		self.armor_bonus = armor_bonus
		self.max_mana_bonus = max_mana_bonus
		self.magic_bonus = magic_bonus
		self.max_hp_bonus = max_hp_bonus
		self.lifesteal_bonus = lifesteal_bonus
		self.hp_regen_bonus = hp_regen_bonus
		self.magic_resist_bonus = magic_resist_bonus
		self.fighting_bonus = fighting_bonus
		self.shielding_bonus = shielding_bonus
		self.conjuring_bonus = conjuring_bonus
		self.archery_bonus = archery_bonus
		self.transmutations_bonus = transmutations_bonus
		self.hexes_bonus = hexes_bonus
		self.evasion_bonus = evasion_bonus
		self.accuracy_bonus = accuracy_bonus

		self.speed_bonus = speed_bonus
		self.dmg_reduction_bonus = dmg_reduction_bonus
		self.heal_kill_bonus = heal_kill_bonus

		self.transm = transm
		self.displays = displays


		self.end_time = end_time
		self.name = name

class Trap:
	def __init__(self, name, trigger_function, dur):
		self.name = name
		self.trigger_function = trigger_function
		self.dur = dur

	def check_traps(self):
		for obj in objects:
			if obj.x == self.owner.x and obj.y == self.owner.y and obj.ai:
				self.trigger_function(obj)
				objects.remove(self.owner)

class TimeObj:
	def __init__(self, action_points, speed):
		self.action_points = action_points
		self.base_speed = speed

	@property
	def speed(self):
		bonus = sum(buff.speed_bonus for buff in self.owner.fighter.buff)
		return self.base_speed + bonus

	def register(self):
		time_travelers.append(self)
		self.action_points = 0

	def release(self):
		time_travelers.remove(self)

	def tick(self):
		if len(time_travelers) > 0:
			obj = time_travelers[0]
			time_travelers.rotate()
			speed_mod = player.fighter.speed - 100
			obj.action_points += obj.speed - speed_mod
			while obj.action_points > 0:
				obj.action_points -= obj.owner.ai.take_turn()

class LootObj:

	def __init__(self, name, loot=[]):
		self.name = name
		self.loot = loot

	def open(self):

		if len(self.loot) == 0:

			message('The ' + self.name + ' is empty.', libtcod.light_gray)
			return

		else:

			options = []

			for item in self.loot:

				text = item.name

				options.append(text)

		index = menu(self.name, options, SPELLBOOK_WIDTH)

		if index is None or len(self.loot) == 0: 
			return

		if len(inventory) >= 26:
			message('Your inventory is full, unable to pick up ' + self.owner.name + '.', libtcod.red)
			return
		message('You picked up a ' + str(self.loot[index].name) + '. ', libtcod.light_green)	
		inventory.append(self.loot[index])
		self.loot.remove(self.loot[index])
		
#---FUNCTIONS---#

def create_room(room):
	global tilemap
	for x in range(room.x1+1, room.x2):
		for y in range(room.y1+1, room.y2):
			tilemap[x][y].blocked = False
			tilemap[x][y].block_sight = False

def create_h_tunnel(x1, x2, y):
	global tilemap
	for x in range(min(x1, x2), max(x1, x2) + 1):
		tilemap[x][y].blocked = False
		tilemap[x][y].block_sight = False

def create_v_tunnel(y1, y2, x):
	global tilemap
	for y in range(min(y1, y2), max(y1, y2) + 1):
		tilemap[x][y].blocked = False
		tilemap[x][y].block_sight = False

def make_map():
	global tilemap, objects, stairs, dungeon_level, mana_well, health_shrine, rooms, lever

	objects = [player]

	#if dungeon_level <=5 or dungeon_level >=10:
	if True: # dungeon_level >= 1:

		tilemap = [[ Tile(True)
			for y in range(MAP_HEIGHT) ]
				for x in range(MAP_WIDTH) ]

		rooms = []
		num_rooms = 0



		if dungeon_level >= 3 and dungeon_level < 5:
			room_minsize = 7
			room_maxsize = 8
		elif dungeon_level < 3:
			room_minsize = ROOM_MIN_SIZE
			room_maxsize = ROOM_MAX_SIZE
		else:
			room_minsize = 8
			room_maxsize = 12

		for r in range(MAX_ROOMS):
			w = libtcod.random_get_int(0, room_minsize, room_maxsize)
			h = libtcod.random_get_int(0, room_minsize, room_maxsize)
			x = libtcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
			y = libtcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)

			new_room = Rectangle(x, y, w, h)

			failed = False
			for other_room in rooms:
				if new_room.intersect(other_room):
					failed = True
					break

			if not failed:
				create_room(new_room)
				(new_x, new_y) = new_room.center()

				if num_rooms == 0:
					player.x = new_x
					player.y = new_y
				else:
					(prev_x, prev_y) = rooms[num_rooms-1].center()
					if libtcod.random_get_int(0, 0, 1) == 1:
						create_h_tunnel(prev_x, new_x, prev_y)
						create_v_tunnel(prev_y, new_y, new_x)
					else:
						create_v_tunnel(prev_y, new_y, prev_x)
						create_h_tunnel(prev_x, new_x, new_y)

				place_objects(new_room)
				rooms.append(new_room)
				num_rooms += 1

		###SPECIAL EVENTS###

		if dungeon_level == 5:
		
			for room in rooms:
				(x, y) = room.center()
				if not is_blocked(x, y) and player.distance(x, y) >= 15:

					time_component = TimeObj(0, 102)
					fighter_component = Fighter(hp=80, defense=6, power=7, xp=75, armor=1, mana=0, magic=0, fighting=2, shielding=2, death_function=monster_death, lifesteal=0)
					ai_component = BasicMonster()
					monster = Object(x, y, 'O', 'Svublo, the fat orc', libtcod.desaturated_green, blocks=True, fighter=fighter_component, ai=ai_component, timeobj=time_component)
					objects.append(monster)
					monster.timeobj.register()
					break

		if dungeon_level == 10:

			for room in rooms:
				(x, y) = room.center()
				if not is_blocked(x, y) and player.distance(x, y) >= 15:

					time_component = TimeObj(0, 104)
					fighter_component = Fighter(hp=150, defense=10, power=14, xp=150, armor=2, mana=0, magic=0, fighting=5, shielding=5, death_function=monster_death, lifesteal=0)
					ai_component = MalignantSpiritMonster()
					monster = Object(x, y, 'Y', 'Malignant spirit', libtcod.light_violet, blocks=True, fighter=fighter_component, ai=ai_component, timeobj=time_component)
					objects.append(monster)
					monster.timeobj.register()
					break

		###PLACE LOOT OBJECTS###

		# number of loot obj
		value = int(round((dungeon_level*0.4) - libtcod.random_get_int(0, 0, 2) + 1))
		side_chance = libtcod.random_get_int(0, 0, 100)
		if side_chance > 75 and dungeon_level > 3:
			value += 3
		else:
			value -= 1

		# bookshelves
		place_lootobj(value, 'bookshelf')

		value = value*0.8 + libtcod.random_get_int(0, 0, 1)

		# ore deposits
		place_lootobj(value, 'ore deposit')

		dice = libtcod.random_get_int(0, 0, 100)
	
		if dice < 38 and dungeon_level >= 3:

			for room in rooms:
				(x, y) = room.center()
				if not is_blocked(x, y) and check_objects(x, y) is False:

					mana_well = Object(x, y, 'E', 'mana well', libtcod.white, blocks=False, always_visible=True)
					objects.append(mana_well)
					mana_well.send_to_back()
					break

		elif dice < 76 and dungeon_level >= 3:

			for room in rooms:
				(x, y) = room.center()
				if not is_blocked(x, y) and check_objects(x, y) is False:

					health_shrine = Object(x, y, 'R', 'health shrine', libtcod.white, blocks=False, always_visible=True)
					objects.append(health_shrine)
					health_shrine.send_to_back()
					break
		lever_chance = libtcod.random_get_int(0, 0, 100)
		if lever_chance > 75:
			for room in rooms:
				(x, y) = room.center()
				if not is_blocked(x, y) and check_objects(x, y) is False:
					lever = Object(x, y, 'l', 'lever', libtcod.red, blocks=False, always_visible=True)
					objects.append(lever)
					stair_name = 'stairs (blocked)'
					break
			else:
				stair_name = 'stairs'
		else:
			stair_name = 'stairs'

		stairs = Object(new_x, new_y, stairsdown_tile, stair_name, libtcod.white, always_visible=True)
		objects.append(stairs)
		stairs.send_to_back()

	else:
		smap = ['################################################################################',
				'##   ########   ############     ############    ##############    #############',
				'#     ####           ##  ##        ########              #####      ############',
				'#      ##                      ##   ######   ###          ####          ########',
				'#                ##            ###  ######  #####     ##   ##   ###      #######',
				'#               ####           ##    ###   #######   ####      #####        ####',
				'##             #####     ###             ##################   #########     ####',
				'###          ######     #####         ##################################    ####',
				'####        ######     ######        ####################################   ####',
				'####  ###  ######      #####         ############   ###   ###############   ####',
				'###  ###########       ####          ###########           ###############   ###',
				'##  ###########         ##            #########            ###############    ##',
				'###############                       #####               ############        ##',
				'##############               ####     ####               ############        ###',
				'#############       ##       #####   ####              ##############       ####',
				'#############      ####       ###########     ###     ####  ########        ####',
				'#####  ######   #######       ############   #####   ####    #######        ####',
				'##      #####  #######        ############   #####  ####      #####        #####',
				'#        ###   ######         ############    ####  ####  ##  ####         #####',
				'#               ####           ##     ###     ####   ##  ####  ###         #####',
				'##                                             ##        ####  ###          ####',
				'#####                                 ###                 ##   ##            ###',
				'#####                          ####  #####   ##               ###       ##   ###',
				'#####             ##          ############  ####             ###       ####  ###',
				'#####            ####     #   ############  #####          ####       #####  ###',
				'####   ##        #####   ###  ############  #####         #####       ######  ##',
				'###   #####       ###    ###   #   #######  #####         ####         ######  #',
				'##    #######            ##         ######  ######       #####           ####  #',
				'##     ########                      #####  #######      #####       #    ##   #',
				'##     #########                      ####  #######     ######      ###       ##',
				'##    ##########                ###   ####  ########   ######       ###       ##',
				'##    ##########               #####  ####  ##############           #        ##',
				'##     ########                #####  #### #############                      ##',
				'##      ######   ##            #####  ###  ############                       ##',
				'##      #####    ###  ##       ####   ###  ###########             ###        ##',
				'##      #####    ##  ####     ####    ###   ##                 #   ####    <  ##',
				'##     ######        ####     ####     ###                    ###  ####       ##',
				'##  P #######        ####     ####     ###                     #    ##   ##  ###',
				'###   ######          ##      ####    ####                              ########',
				'###########    ###             ##     ####     ##   ###                 ########',
				'###########   #####                  #####    ##########               #########',
				'###########  #################    #########  ##############   ##################',
				'################################################################################',
				]	 
		cmap_h = len(smap)
		cmap_w = len(smap[0])

		#declare variable 'tilemap' and fill with blocked tiles
		tilemap = [[Tile(True) for y in range(cmap_h)] for x in range(cmap_w)]
		for y in range(MAP_HEIGHT):
			for x in range(MAP_WIDTH):
				if smap[y][x] == ' ':
					tilemap[x][y] = Tile(False)
				elif smap[y][x] == '<':
					stair_x, stair_y = x, y
					tilemap[x][y] = Tile(False)
				elif smap[y][x] == 'P':
					player.x, player.y = x, y 
					tilemap[x][y] = Tile(False)
				
		dice = libtcod.random_get_int(0, 0, 100)

		if dice < 38 and dungeon_level >= 4:

			tries = 0
			
			while True:

				(x, y) = (libtcod.random_get_int(0, 0, MAP_WIDTH), libtcod.random_get_int(0, 0, MAP_HEIGHT))

				tries += 1

				if not is_blocked(x, y) and check_objects(x, y) is False:

					mana_well = Object(x, y, 'E', 'mana well', libtcod.white, blocks=False, always_visible=True)
					objects.append(mana_well)
					mana_well.send_to_back()
					break

				elif tries > 5:
					break

		elif dice < 76 and dungeon_level >= 4:

			tries = 0
			
			while True:

				(x, y) = (libtcod.random_get_int(0, 0, MAP_WIDTH), libtcod.random_get_int(0, 0, MAP_HEIGHT))

				tries += 1

				if not is_blocked(x, y) and check_objects(x, y) is False:

					health_shrine = Object(x, y, 'R', 'health shrine', libtcod.white, blocks=False, always_visible=True)
					objects.append(health_shrine)
					health_shrine.send_to_back()
					break

				elif tries > 5:
					break



		place_objects_random()
		stairs = Object(stair_x, stair_y, stairsdown_tile, 'stairs', libtcod.white, always_visible=True)
		objects.append(stairs)
		stairs.send_to_back

def make_bsp():
	global tilemap, objects, stairs, bsp_rooms

	objects = [player]

	tilemap = [[Tile(True) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]

	bsp_rooms = []

	bsp = libtcod.bsp_new_with_size(0, 0, MAP_WIDTH, MAP_HEIGHT)

	libtcod.bsp_split_recursive(bsp, 0, DEPTH, MIN_SIZE + 1, MIN_SIZE +1, 1.5, 1.5)

	libtcod.bsp_traverse_inverted_level_order(bsp, traverse_node)

	#Random room for the stairs
	stairs_location = random.choice(bsp_rooms)
	bsp_rooms.remove(stairs_location)
	stairs = Object(stairs_location[0], stairs_location[1], stairsdown_tile, 'stairs', libtcod.white, always_visible=True)
	objects.append(stairs)
	stairs.send_to_back()
 
	#Random room for player start
	player_room = random.choice(bsp_rooms)
	bsp_rooms.remove(player_room)
	player.x = player_room[0]
	player.y = player_room[1]
 
	#Add monsters and items
	for room in bsp_rooms:
		new_room = Rectangle(room[0], room[1], 2, 2)
		place_objects(new_room)

	
 
	initialize_fov()    

def vline(tilemap, x, y1, y2):
	if y1 > y2:
		y1,y2 = y2,y1
 
	for y in range(y1,y2+1):
		tilemap[x][y].blocked = False
		tilemap[x][y].block_sight = False
 
def vline_up(tilemap, x, y):
	while y >= 0 and tilemap[x][y].blocked == True:
		tilemap[x][y].blocked = False
		tilemap[x][y].block_sight = False
		y -= 1
 
def vline_down(tilemap, x, y):
	while y < MAP_HEIGHT and tilemap[x][y].blocked == True:
		tilemap[x][y].blocked = False
		tilemap[x][y].block_sight = False
		y += 1
 
def hline(tilemap, x1, y, x2):
	if x1 > x2:
		x1,x2 = x2,x1
	for x in range(x1,x2+1):
		tilemap[x][y].blocked = False
		tilemap[x][y].block_sight = False
 
def hline_left(tilemap, x, y):
	while x >= 0 and tilemap[x][y].blocked == True:
		tilemap[x][y].blocked = False
		tilemap[x][y].block_sight = False
		x -= 1
 
def hline_right(tilemap, x, y):
	while x < MAP_WIDTH and tilemap[x][y].blocked == True:
		tilemap[x][y].blocked = False
		tilemap[x][y].block_sight = False
		x += 1

def traverse_node(node, dat):
	global tilemap, bsp_rooms
 
	#Create rooms
	if libtcod.bsp_is_leaf(node):
		minx = node.x + 1
		maxx = node.x + node.w - 1
		miny = node.y + 1
		maxy = node.y + node.h - 1
 
		if maxx == MAP_WIDTH - 1:
			maxx -= 1
		if maxy == MAP_HEIGHT - 1:
			maxy -= 1
 
		#If it's False the rooms sizes are random, else the rooms are filled to the node's size
		if FULL_ROOMS == False:
			minx = libtcod.random_get_int(None, minx, maxx - MIN_SIZE + 1)
			miny = libtcod.random_get_int(None, miny, maxy - MIN_SIZE + 1)
			maxx = libtcod.random_get_int(None, minx + MIN_SIZE - 2, maxx)
			maxy = libtcod.random_get_int(None, miny + MIN_SIZE - 2, maxy)
 
		node.x = minx
		node.y = miny
		node.w = maxx-minx + 1
		node.h = maxy-miny + 1
 
		#Dig room
		for x in range(minx, maxx + 1):
			for y in range(miny, maxy + 1):
				tilemap[x][y].blocked = False
				tilemap[x][y].block_sight = False
 
		#Add center coordinates to the list of rooms
		bsp_rooms.append(((minx + maxx) / 2, (miny + maxy) / 2))
 
	#Create corridors    
	else:
		left = libtcod.bsp_left(node)
		right = libtcod.bsp_right(node)
		node.x = min(left.x, right.x)
		node.y = min(left.y, right.y)
		node.w = max(left.x + left.w, right.x + right.w) - node.x
		node.h = max(left.y + left.h, right.y + right.h) - node.y
		if node.horizontal:
			if left.x + left.w - 1 < right.x or right.x + right.w - 1 < left.x:
				x1 = libtcod.random_get_int(None, left.x, left.x + left.w - 1)
				x2 = libtcod.random_get_int(None, right.x, right.x + right.w - 1)
				y = libtcod.random_get_int(None, left.y + left.h, right.y)
				vline_up(tilemap, x1, y - 1)
				hline(tilemap, x1, y, x2)
				vline_down(tilemap, x2, y + 1)
 
			else:
				minx = max(left.x, right.x)
				maxx = min(left.x + left.w - 1, right.x + right.w - 1)
				x = libtcod.random_get_int(None, minx, maxx)
				vline_down(tilemap, x, right.y)
				vline_up(tilemap, x, right.y - 1)
 
		else:
			if left.y + left.h - 1 < right.y or right.y + right.h - 1 < left.y:
				y1 = libtcod.random_get_int(None, left.y, left.y + left.h - 1)
				y2 = libtcod.random_get_int(None, right.y, right.y + right.h - 1)
				x = libtcod.random_get_int(None, left.x + left.w, right.x)
				hline_left(tilemap, x - 1, y1)
				vline(tilemap, x, y1, y2)
				hline_right(tilemap, x + 1, y2)
			else:
				miny = max(left.y, right.y)
				maxy = min(left.y + left.h - 1, right.y + right.h - 1)
				y = libtcod.random_get_int(None, miny, maxy)
				hline_left(tilemap, right.x - 1, y)
				hline_right(tilemap, right.x, y)
 
	return True

def render_all():
	global fov_map, color_dark_wall, color_light_wall, debug
	global color_dark_ground, color_light_ground, fov_recompute, dungeon_level

	if fov_recompute:
		fov_recompute = False

		if player.race == 'Green Elf':
			torch = 12
		else:
			torch = 8
		libtcod.map_compute_fov(fov_map, player.x, player.y, torch, FOV_LIGHT_WALLS, FOV_ALGO)

		for y in range(MAP_HEIGHT):
			for x in range(MAP_WIDTH):
				if reveal_map:
					visible = True
				else:
					visible = libtcod.map_is_in_fov(fov_map, x, y)
				wall = tilemap[x][y].block_sight
				if not visible:
					if tilemap[x][y].explored:
						if dungeon_level < 5:
							if wall:
								libtcod.console_put_char_ex(con, x, y, wall_tile, libtcod.grey, libtcod.black)
							else:
								libtcod.console_put_char_ex(con, x, y, floor_tile, libtcod.grey, libtcod.black)
						elif dungeon_level >= 5:
							if wall:
								libtcod.console_put_char_ex(con, x, y, wall_tile, libtcod.grey, libtcod.black)
							else:
								libtcod.console_put_char_ex(con, x, y, floor_tile, libtcod.grey, libtcod.black)
				else:
					if dungeon_level < 5:

						if wall:
							libtcod.console_put_char_ex(con, x, y, wall_tile, libtcod.white, libtcod.black)
						else:
							libtcod.console_put_char_ex(con, x, y, floor_tile, libtcod.white, libtcod.black)
						tilemap[x][y].explored = True

					elif dungeon_level >= 5:
						if wall:
							libtcod.console_put_char_ex(con, x, y, wall_tile, libtcod.white, libtcod.black )
						else:
							libtcod.console_put_char_ex(con, x, y, floor_tile, libtcod.white, libtcod.black )

						tilemap[x][y].explored = True

		for obj in objects:
			if obj.fighter:
				for buff in obj.fighter.buff:
					if buff.name == 'Hex Of Radiance':
						for y in range(MAP_HEIGHT):
							for x in range(MAP_WIDTH):
								if obj.distance(x, y) <= 5:
									visible = libtcod.map_is_in_fov(fov_map, x, y)
									wall = tilemap[x][y].block_sight
									if not visible:
										if tilemap[x][y].explored:
											if wall:
												libtcod.console_put_char_ex(con, x, y, wall_tile, libtcod.dark_yellow, libtcod.black)
											else:									
												libtcod.console_put_char_ex(con, x, y, floor_tile, libtcod.dark_yellow, libtcod.black)
									else:
										if wall:
											libtcod.console_put_char_ex(con, x, y, wall_tile, libtcod.light_yellow, libtcod.black)
										else:
											libtcod.console_put_char_ex(con, x, y, floor_tile, libtcod.light_yellow, libtcod.black)
										tilemap[x][y].explored = True
		for b in player.fighter.buff:
			if b.name == 'White Light':
				for y in range(MAP_HEIGHT):
					for x in range(MAP_WIDTH):
						if player.distance(x, y) <= 7:
							visible = libtcod.map_is_in_fov(fov_map, x, y)
							wall = tilemap[x][y].block_sight
							if not visible:
								if tilemap[x][y].explored:
									if wall:
										libtcod.console_put_char_ex(con, x, y, wall_tile, libtcod.light_violet, libtcod.black)
									else:									
										libtcod.console_put_char_ex(con, x, y, floor_tile, libtcod.light_violet, libtcod.black)
							else:
								if wall:
									libtcod.console_put_char_ex(con, x, y, wall_tile, libtcod.lighter_violet, libtcod.black)
								else:
									libtcod.console_put_char_ex(con, x, y, floor_tile, libtcod.lighter_violet, libtcod.black)
								tilemap[x][y].explored = True


	for obj in objects:
		if obj != player:
			if reveal_map == True:
				obj.always_visible = True
			obj.draw()
	player.draw()

	libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

	libtcod.console_set_default_background(panel, libtcod.black)
	libtcod.console_clear(panel)

	y = 1
	for (line, color) in game_msgs:
		libtcod.console_set_default_foreground(panel, color)
		libtcod.console_print_ex(panel, MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
		y += 1


	if player.fighter.max_mana <= 0:
		player.fighter.max_mana = 1

	render_bar(1, 1, BAR_WIDTH, 'HP', player.fighter.hp, player.fighter.max_hp, libtcod.light_red, libtcod.darker_red)
	render_bar(1, 2, BAR_WIDTH, 'Mana', player.fighter.mana, player.fighter.max_mana,
		libtcod.light_blue, libtcod.darker_blue)

	libtcod.console_print_ex(panel, 5, 3, libtcod.BKGND_NONE, libtcod.LEFT, 'Dungeon level ' + str(dungeon_level))
	libtcod.console_set_default_foreground(panel, libtcod.light_gray)
	libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse())
	libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_player())

	libtcod.console_blit(panel, 0, 0, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0, PANEL_Y)

def handle_keys():
	global fov_recompute, key, stairs, mana_well, health_shrine, lever, debug, reveal_map

	if key.vk == libtcod.KEY_ENTER and key.lalt:
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
	elif key.vk == libtcod.KEY_ESCAPE:
		return 'exit'
	if game_state == 'playing':

		if key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
			player_move_or_attack(0, -1)
		elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
			player_move_or_attack(0, 1)
		elif key.vk == libtcod.KEY_LEFT or key.vk == libtcod.KEY_KP4:
			player_move_or_attack(-1, 0)
		elif key.vk == libtcod.KEY_RIGHT or key.vk == libtcod.KEY_KP6:
			player_move_or_attack(1, 0)
		elif key.vk == libtcod.KEY_HOME or key.vk == libtcod.KEY_KP7:
			player_move_or_attack(-1, -1)
		elif key.vk == libtcod.KEY_PAGEUP or key.vk == libtcod.KEY_KP9:
			player_move_or_attack(1, -1)
		elif key.vk == libtcod.KEY_END or key.vk == libtcod.KEY_KP1:
			player_move_or_attack(-1, 1)
		elif key.vk == libtcod.KEY_PAGEDOWN or key.vk == libtcod.KEY_KP3:
			player_move_or_attack(1, 1)

		elif key.vk == libtcod.KEY_KP5:
			pass

		elif key.vk == libtcod.KEY_TAB:
			monster = closest_monster(10)
			if monster is not None and libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
				if player.distance_to(monster) >= 2:
					if get_equipped_in_slot('ranged weapon') is None:
						player.move_astar(monster)
						fov_recompute = True
					else:
						if player.distance_to(monster) <= 6:
							player.fighter.ranged_attack(monster)
							fov_recompute = True
						else:
							player.move_astar(monster)
							fov_recompute = True
				elif monster.fighter.hp > 0:
					player.fighter.attack(monster)
					fov_recompute = True
		else:
			key_char = chr(key.c)

			if key_char == 'g':
				for obj in objects:
					if obj.x == player.x and obj.y == player.y and obj.item:
						obj.item.pick_up()
						break

			if key_char == 'i' and menu_check == False:
				chosen_item = inventory_menu('Press the key next to an item to use it, or any other key to cancel.')
				if chosen_item is not None:
					chosen_item.use()

			if key_char == 'd' and menu_check == False:
				chosen_item = inventory_menu('Press the key next to an item to drop it, or any other key to cancel.')
				if chosen_item is not None:
					chosen_item.drop()	

			if key_char == '<':
				if stairs.x == player.x and stairs.y == player.y:
					if stairs.name == 'stairs (blocked)':
						message('The stairs are blocked by a wall of stone... How do I get out of here?', libtcod.yellow)
					else:
						next_level()
				elif tilemap[stairs.x][stairs.y].explored:
					done = auto_walk(stairs.x, stairs.y)
					while not done:
						done = auto_walk(stairs.x, stairs.y)			

			if key_char == 'c' and menu_check == False:
				character_screen()

			if key_char == 'q' and menu_check == False:
				chosen_item = inventory_menu('Press the key next to an item to inspect it, or any other key to cancel.')
				if chosen_item is not None:
					chosen_item.inspect()

			if key_char == 'w' and menu_check == False:
				chosen_spell = spell_menu('Press the key next to a spell to cast it, or any other key to cancel.')
				if chosen_spell is not None:
					chosen_spell.cast()

			if key_char == 'r':
				if get_equipped_in_slot('ranged weapon') is None:
					message('You must have a ranged weapon equipped to perform a ranged attack!', libtcod.red)
				else:
					message('Click a target to attack it.', libtcod.yellow)
					monster = target_monster(6)
					if monster is not None:
						if monster.distance_to(player) < 2:
							message('Too close to perform ranged attack!', libtcod.red)
						else:
							player.fighter.ranged_attack(monster)
							for obj in objects:
								obj.clear()

							return 'took turn'
					else:
						message('Must have a target to attack!', libtcod.red)
			if key_char == 'e':
				for obj in objects:
					if obj.name == 'mana well':
						if mana_well.x == player.x and mana_well.y == player.y:
							mana_well_use()
					elif obj.name == 'health shrine':
						if health_shrine.x == player.x and health_shrine.y == player.y:
							health_shrine_use()
					elif obj.name == 'bookshelf':
						if obj.x == player.x and obj.y == player.y:
							obj.loot.open()
					elif obj.name == 'ore deposit':
						if obj.x == player.x and obj.y == player.y:
							obj.loot.open()
					elif obj.name == 'lever':
						if obj.x == player.x and obj.y == player.y:
							if lever.color == libtcod.red:
								lever.color = libtcod.green
								stairs.name = 'stairs'
							else:
								lever.color = libtcod.red
								stairs.name = 'stairs (blocked)'
							message('You flip the lever. You hear a rumbling noise in the distance...', libtcod.light_gray)


			if key_char == 'z':
				auto_explore()

			if key_char == 't':
				for item in inventory:
					if item.equipment:
						break
				else:
					message('Your inventory contains no equipment to transmute.', libtcod.yellow)
					return 'didnt-take-turn'
				chosen_material = transmute_menu('Press the key next to a material to select it, or any other key to cancel.')				

			if key_char == 'D':
				message('***Entering debug mode***', libtcod.light_red)
				debug = True

			# DEBUG
			if debug:
				if key_char == 'm':
					debug_stats_menu('Modify which stat?')
				if key_char == 'y':
					if reveal_map == False:
						reveal_map = True
						return 'didnt-take-turn'
					else:
						reveal_map = False
						return 'didnt-take-turn'
				if key_char == 's':
					next_level()


			return 'didnt-take-turn'

def place_objects(room):
	global dungeon_level
	max_monsters = from_dungeon_level([[2, 1], [3, 4], [4, 6], [5, 7], [6, 9]])

	monster_chances = {}
	monster_chances['orc'] = from_dungeon_level([[30, 1], [45, 2], [30, 3], [20, 4], [10, 6], [0, 7]])
	monster_chances['snake'] = from_dungeon_level([[20, 1], [15, 3], [7, 5], [0, 7]])
	monster_chances['troll'] = from_dungeon_level([[12, 3], [20, 4], [27, 5], [22, 6], [17, 7], [7, 8], [2, 9], [0, 10]])
	monster_chances['guard dog'] = from_dungeon_level([[2, 4], [7, 5], [7, 6], [10, 7], [15, 8], [10, 9], [5, 10], [0, 11]])
	monster_chances['orc spearthrower'] = from_dungeon_level([[5, 4], [8, 5], [20, 6], [10, 8], [5, 9], [0, 10]])
	monster_chances['skeleton'] = from_dungeon_level([[3, 6], [6, 7], [10, 8], [8, 9], [9, 10], [7, 11], [5, 12]])
	monster_chances['orc soldier'] = from_dungeon_level([[2, 6], [4, 7], [6, 8], [8, 9], [5, 10], [3, 11], [0, 12]])

	monster_chances['phantasm'] = from_dungeon_level([[1, 6], [2, 7], [3, 8], [4, 9], [5, 10], [6, 11], [5, 12], [4, 13]])
	monster_chances['ancient troll'] = from_dungeon_level([[1, 8], [2, 9], [3, 10], [5, 11]])
	monster_chances['orc warlock'] = from_dungeon_level([[2, 5], [4, 7], [3, 8], [2, 10], [0, 11]])
	monster_chances['vampire'] = from_dungeon_level([[2, 8], [3, 9], [4, 10]])
	monster_chances['lich'] = from_dungeon_level([[1, 9], [2, 10], [3, 12], [5, 13]])
	monster_chances['demonspawn'] = from_dungeon_level([[1, 12], [2, 13], [3, 14]])
	monster_chances['demon'] = from_dungeon_level([[1, 15], [2, 16], [5, 17]])

	max_items = from_dungeon_level([[1, 1], [2, 3], [3, 10]])

	item_chances = {}
	#POTIONS
	item_chances['nothing'] = from_dungeon_level( [ [30, 1], [27, 2], [24, 3], [21, 4], [18, 5] ])
	item_chances['heal'] = from_dungeon_level([[30, 1], [27, 3], [24, 5], [22, 7]])
	item_chances['mana'] = from_dungeon_level([[24, 1], [22, 3], [20, 5]])
	item_chances['berserker potion'] = from_dungeon_level([[4, 2], [6, 3], [4, 5]])
	item_chances['magic potion'] = from_dungeon_level([[1, 1], [2, 3], [4, 5]])
	#SCROLLS
	item_chances['lightning'] = from_dungeon_level([[4, 2], [6, 4], [5, 7]])
	item_chances['fireball'] = from_dungeon_level([[2, 3], [3, 5], [4, 6]])
	item_chances['confuse'] = from_dungeon_level([[3, 1], [5, 2], [4, 3], [3, 5]])
	item_chances['scroll of knowledge'] = from_dungeon_level([[1, 3]])
	#TIER 1 EQ
	item_chances['short sword'] = from_dungeon_level([[3, 1], [5, 2], [6, 3], [5, 4], [2, 6]])
	item_chances['wooden shield'] = from_dungeon_level([[3, 1], [7, 3], [6, 4], [4, 5], [2, 6], [0, 8]])
	item_chances['dagger'] = from_dungeon_level([[4, 1], [7, 2], [6, 3], [4, 5], [0, 7]])	
	item_chances['cape'] = from_dungeon_level([[3, 1], [6, 2], [5, 5], [0, 7]])
	item_chances['wand'] = from_dungeon_level([[3, 1], [5, 2], [6, 4], [4, 5], [0, 6]])
	item_chances['mace'] = from_dungeon_level([[2, 1], [4, 2], [5, 3], [4, 4], [3, 5], [2, 6], [1, 7], [0, 8]])
	item_chances['small axe'] = from_dungeon_level([[2, 1], [3, 2], [4, 3], [5, 4], [4, 5], [3, 6], [1, 7], [0, 9]])	
	item_chances['cap'] = from_dungeon_level([[3, 1], [4, 2], [3, 4], [2, 5], [1, 6], [0, 7]])
	item_chances['robe'] = from_dungeon_level([[2, 1], [3, 2], [4, 3], [5, 4], [4, 5], [2, 6], [0, 9]])

	#TIER 2 EQ
	item_chances['longbow'] = from_dungeon_level([[2, 4], [4, 5], [5, 6], [4, 9], [2, 11]])
	item_chances['chained helmet'] = from_dungeon_level([[3, 2], [5, 3], [7, 4], [3, 5], [1, 10]])
	item_chances['sharpened dagger'] = from_dungeon_level([[2, 4], [4, 5], [9, 7], [7, 9], [4, 10], [2, 11]])
	item_chances['wave-patterned sword'] = from_dungeon_level([[3, 5], [5, 6], [7, 7], [6, 9], [4, 10], [1, 11]])
	item_chances['rondache'] = from_dungeon_level([[1, 2], [3, 3], [4, 4], [5, 6], [4, 10], [2, 11]])
	item_chances['quilted armor'] = from_dungeon_level([[2, 3], [3, 4], [5, 5], [7, 6], [6, 8], [2, 10]])
	item_chances['short staff'] = from_dungeon_level([[2, 3], [3, 4], [5, 5], [7, 6], [6, 8], [3, 10]])
	item_chances['leather armor'] = from_dungeon_level([[1, 3], [3, 5], [5, 6], [4, 8], [3, 9], [2, 10], [0, 11]])
	item_chances['large axe'] = from_dungeon_level([[1, 4], [2, 5], [5, 6], [6, 7], [4, 8], [2, 9], [0, 11]])
	item_chances['spiked mace'] = from_dungeon_level([[1, 3], [2, 5], [5, 6], [6, 7], [4, 8], [2, 9], [0, 11]])
	#TIER 3 EQ
	item_chances['crossbow'] = from_dungeon_level([[1, 5], [2, 6], [3, 7], [4, 8], [5, 9], [4, 10], [2, 11], [1, 12]])
	item_chances['visored close helmet'] = from_dungeon_level([[1, 5], [2, 6], [4, 7], [6, 8], [5, 9], [4, 10], [2, 11], [1, 12]])
	item_chances['chain mail'] = from_dungeon_level([[1, 6], [3, 7], [5, 8], [6, 9], [5, 10], [4, 11], [0, 14]])
	item_chances['long sword'] = from_dungeon_level([[1, 5], [2, 6], [3, 7], [4, 8], [5, 9], [4, 10], [2, 11], [1, 12]])
	item_chances['large shield'] = from_dungeon_level([[1, 6], [3, 7], [5, 8], [6, 9], [5, 10], [3, 11], [1, 12]])
	item_chances['azure shiv'] = from_dungeon_level([[1, 6], [3, 7], [5, 8], [7, 9], [6, 10], [4, 11], [2, 12], [0, 14]])
	item_chances['war mace'] = from_dungeon_level([[1, 5], [2, 6], [3, 7], [4, 8], [5, 9], [4, 10], [2, 11], [1, 12]])
	item_chances['runic wand'] = from_dungeon_level([[2, 6], [3, 7], [4, 8], [5, 9], [4, 10], [2, 11], [1, 12]])
	item_chances['battle axe'] = from_dungeon_level([[1, 5], [2, 6], [3, 7], [4, 8], [5, 9], [4, 10], [2, 11], [1, 12]])
	item_chances['ceremonial robes'] = from_dungeon_level([[1, 5], [2, 6], [3, 7], [4, 8], [5, 9], [4, 10], [2, 11], [1, 12]])
	item_chances['hard leather armor'] = from_dungeon_level([[1, 5], [2, 6], [3, 7], [4, 8], [5, 9], [4, 10], [2, 11], [1, 12]])
	#TIER 4 EQ
	item_chances['breast plate'] = from_dungeon_level([[1, 7], [2, 8], [3, 9], [4, 10]])
	item_chances['trollweave'] = from_dungeon_level([[1, 7], [2, 8], [3, 9], [4, 10]])
	# not yet added item: item_chances['robe3'] = from_dungeon_level([[1, 7], [2, 8], [4, 9]])
	# not yet added item: item_chances['wand3'] = from_dungeon_level([[1, 7], [2, 8], [4, 9]])
	item_chances['full helm'] = from_dungeon_level([[1, 7], [2, 8], [3, 9]])
	item_chances['noble mask'] = from_dungeon_level([[1, 7], [2, 8], [3, 9]])
	item_chances['cleaver'] = from_dungeon_level([[1, 7], [2, 8], [3, 9]])
	item_chances['falcata'] = from_dungeon_level([[1, 7], [2, 8], [3, 9]])
	item_chances['trident dagger'] = from_dungeon_level([[1, 7], [2, 8], [3, 9]])
	item_chances['giant maul'] = from_dungeon_level([[1, 7], [3, 8], [4, 9]])
	item_chances['long staff'] = from_dungeon_level([[1, 7], [3, 8], [4, 9]])
	item_chances['tower shield'] = from_dungeon_level([[1, 7], [2, 8], [3, 9]])
	item_chances['double bow'] = from_dungeon_level([[1, 7], [2, 8], [4, 9]])
	#TIER 5 EQ
	item_chances['winged helmet'] = from_dungeon_level([[1, 9], [2, 10], [3, 11]])
	item_chances['full plate mail'] = from_dungeon_level([[1, 9], [2, 10], [3, 11]])
	item_chances['panaba'] = from_dungeon_level([[1, 9], [2, 10], [3, 11]])
	item_chances['great sword'] = from_dungeon_level([[1, 9], [2, 10], [3, 11]])
	item_chances['oakwood spire'] = from_dungeon_level([[1, 9], [2, 10], [3, 11]])
	item_chances['greatshield'] = from_dungeon_level([[1, 9], [2, 10], [3, 11]])
	item_chances['arbalest'] = from_dungeon_level([[1, 9], [2, 10], [3, 11]])

	item_chances['book of ice conj'] = from_dungeon_level([[1, 1], [2, 3]])
	item_chances['book of fire conj'] = from_dungeon_level([[1, 1], [2, 3]])
	item_chances['book of transmutations'] = from_dungeon_level([[1, 1], [2, 3]])
	item_chances['book of hexes'] = from_dungeon_level([[1, 1], [2, 3]])
	item_chances['book of assorted spells'] = from_dungeon_level([[1, 1], [2, 2]])

	#RINGS AND AMULETS
	item_chances['ring of amp'] = from_dungeon_level([[1, 3]])
	item_chances['ring of protection'] = from_dungeon_level([[1, 1], [2, 4]])
	item_chances['arcane ring'] = from_dungeon_level([[1, 1], [2, 3]])
	item_chances['ring of vigor'] = from_dungeon_level([[1, 4], [2, 6]])
	item_chances['amulet of resist magic'] = from_dungeon_level([[1, 3], [2, 5]])
	item_chances['amulet of speed'] = from_dungeon_level([[1, 1]])
	item_chances['ring of evasion'] = from_dungeon_level([[1, 3], [2, 4]])


	#ARTIFACTS
	item_chances['ivory visage'] = from_dungeon_level([[1, 3]])
	item_chances['windsong silver blade'] = from_dungeon_level([[1, 3]])
	item_chances['crystal ring'] = from_dungeon_level([[1, 4]])
	item_chances['cowl of divine sorrow'] = from_dungeon_level([[1, 5]])
	item_chances['bloodcursed'] = from_dungeon_level([[1, 5]])
	item_chances['wall of the wicked'] = from_dungeon_level([[1, 6]])
	item_chances['ornament of clarity'] = from_dungeon_level([[1, 6]])
	item_chances['dazzling tricellite ring'] = from_dungeon_level([[1, 7]])
	item_chances['maple battle staff'] = from_dungeon_level([[1, 7]])

	#item_chances['apple'] = 10000


	num_monsters = libtcod.random_get_int(0, 0, max_monsters)

	for i in range(num_monsters):
		x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
		y = libtcod.random_get_int(0, room.y1+1, room.y2-1)

		if not is_blocked(x, y):

			choice = random_choice(monster_chances)

			if choice == 'orc':

				hp_mod = item_rand(3)
				speed_mod = item_rand(5)
				def_mod = item_rand(5)
				fight_mod = item_rand(2)

				time_component = TimeObj(0, 88+speed_mod)
				fighter_component = Fighter(hp=9+hp_mod, defense=2+def_mod, power=3, xp=5, armor=0, mana=0, magic=0, death_function=monster_death, fighting=-1+fight_mod)
				ai_component = BasicMonster()
				monster = Object(x, y, orc_tile, 'orc', libtcod.white, blocks=True, fighter=fighter_component, ai=ai_component, timeobj=time_component)
			
			elif choice == 'snake':

				hp_mod = item_rand(2)
				speed_mod = item_rand(6)
				def_mod = item_rand(5)

				time_component = TimeObj(0, 96+speed_mod)
				fighter_component = Fighter(hp=6+hp_mod, defense=6+def_mod, power=2, xp=3, armor=0, mana=0, magic=0, death_function=monster_death)
				ai_component = BasicMonster()
				monster = Object(x, y, 's', 'angry-looking snake', libtcod.darker_lime, blocks=True, fighter=fighter_component, ai=ai_component, timeobj=time_component)

			elif choice == 'guard dog':

				hp_mod = item_rand(5)
				speed_mod = item_rand(7)
				def_mod = item_rand(5)

				time_component = TimeObj(0, 112+speed_mod)
				fighter_component = Fighter(hp=20+hp_mod, defense=4+def_mod, power=6, xp=13, armor=0, mana=0, magic=0, death_function=monster_death, lifesteal=0)
				ai_component = BasicMonsterBleed()
				monster = Object(x, y, 'g', 'orcish guard-dog', libtcod.darker_sepia, blocks=True, fighter=fighter_component, ai=ai_component, timeobj=time_component)

			elif choice == 'troll':

				hp_mod = item_rand(4)
				speed_mod = item_rand(5)
				def_mod = item_rand(4)
				shield_mod = item_rand(1)

				time_component = TimeObj(0, 85+speed_mod)
				fighter_component = Fighter(hp=19+hp_mod, defense=2+def_mod, power=4, xp=8, armor=1, mana=0, magic=0, death_function=monster_death, shielding=0+shield_mod)
				ai_component = BasicMonster()
				monster = Object(x, y, troll_tile, 'troll', libtcod.white, blocks=True, fighter=fighter_component, ai=ai_component, timeobj=time_component)

			elif choice == 'orc spearthrower':

				hp_mod = item_rand(3)
				speed_mod = item_rand(6)
				archery_mod = item_rand(2)

				time_component = TimeObj(0, 90+speed_mod)
				fighter_component = Fighter(hp=11+hp_mod, defense=5, power=6, xp=10, armor=0, mana=0, magic=0, death_function=monster_death, archery=-1+archery_mod)
				ai_component = RangedMonster()
				monster = Object(x, y, 'h', 'orc spearthrower', libtcod.desaturated_green, blocks=True, fighter=fighter_component, ai=ai_component, timeobj=time_component)

			elif choice == 'orc soldier':

				speed_mod = item_rand(7)
				hp_mod = item_rand(5)
				fight_mod = item_rand(2)

				time_component = TimeObj(0, 97+speed_mod)
				fighter_component = Fighter(hp=30+hp_mod, defense=10, power=7, xp=18, armor=2, mana=0, magic=0, fighting=2+fight_mod, shielding=3, magic_resist=0.10, death_function=monster_death)
				ai_component = BasicMonster()
				monster = Object(x, y, 'o', 'orc soldier', libtcod.dark_sepia, blocks=True, fighter=fighter_component, ai=ai_component, timeobj=time_component)

			elif choice == 'skeleton':

				hp_mod = item_rand(9)
				speed_mod = item_rand(4)

				time_component = TimeObj(0, 92+speed_mod)
				fighter_component = Fighter(hp=32+hp_mod, defense=12, power=8, xp=14, armor=2, mana=0, magic=0, fighting=2, shielding=2, death_function=monster_death)
				ai_component = BasicMonster()
				monster = Object(x, y, 'K', 'animated skeleton', libtcod.silver, blocks=True, fighter=fighter_component, ai=ai_component, timeobj=time_component)

			elif choice == 'phantasm':

				time_component = TimeObj(0, 110)
				fighter_component = Fighter(hp=40, defense=30, power=9, xp=24, armor=1, mana=0, magic=0, death_function=monster_death)
				ai_component = HunterMonster()
				monster = Object(x, y, 'w', 'phantasm', libtcod.black, blocks=True, fighter=fighter_component, ai=ai_component, timeobj=time_component)

			elif choice == 'ancient troll':

				time_component = TimeObj(0, 88)
				fighter_component = Fighter(hp=110, defense=8, power=10, xp=32, armor=2, mana=0, magic=0, fighting=3, shielding=3, death_function=monster_death, lifesteal=0)
				ai_component = TrollHealer()
				monster = Object(x, y, 'G', 'ancient troll', libtcod.darker_green, blocks=True, fighter=fighter_component, ai=ai_component, timeobj=time_component)

			elif choice == 'orc warlock':

				time_component = TimeObj(0, 97)
				fighter_component = Fighter(hp=35, defense=5, power=7, xp=20, armor=1, mana=0, magic=0, death_function=monster_death, lifesteal=0)
				ai_component = OrcCaster()
				monster = Object(x, y, 'W', 'orc warlock', libtcod.desaturated_green, blocks=True, fighter=fighter_component, ai=ai_component, timeobj=time_component)
			
			elif choice == 'vampire':

				time_component = TimeObj(0, 105)
				fighter_component = Fighter(hp=56, defense=16, power=10, xp=28, armor=3, mana=0, magic=0, fighting=3, shielding=3, death_function=monster_death, lifesteal=2)
				ai_component = BasicMonsterDrain()
				monster = Object(x, y, 'V', 'vampire', libtcod.black, blocks=True, fighter=fighter_component, ai=ai_component, timeobj=time_component)

			elif choice == 'lich':

				time_component = TimeObj(0, 105)
				fighter_component = Fighter(hp=95, defense=10, power=8, xp=50, armor=2, mana=0, magic=0, death_function=monster_death, lifesteal=0)
				ai_component = CasterMonster()
				monster = Object(x, y, 'L', 'lich', libtcod.blue, blocks=True, fighter=fighter_component, ai=ai_component, timeobj=time_component)

			elif choice == 'demonspawn':

				time_component = TimeObj(0, 100)
				fighter_component = Fighter(hp=160, defense=18, power=16, xp=100, armor=3, mana=0, magic=0, fighting=2, shielding=5, magic_resist=0.10, death_function=monster_death, lifesteal=0)
				ai_component = PainCaster()
				monster = Object(x, y, 'X', 'demonspawn', libtcod.red, blocks=True, fighter=fighter_component, ai=ai_component, timeobj=time_component)

			elif choice == 'demon':

				time_component = TimeObj(0, 100)
				fighter_component = Fighter(hp=300, defense=20, power=24, xp=280, armor=4, mana=0, magic=0, fighting=5, shielding=10, magic_resist=0.15, death_function=monster_death, lifesteal=0)
				ai_component = PainCaster_2()
				monster = Object(x, y, 'M', 'demon', libtcod.red, blocks=True, fighter=fighter_component, ai=ai_component, timeobj=time_component)

			objects.append(monster)
			monster.timeobj.register()

	num_items = libtcod.random_get_int(0, 0, max_items)

	for i in range(num_items):
		x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
		y = libtcod.random_get_int(0, room.y1+1, room.y2-1)

		if not is_blocked(x, y):

			choice = random_choice(item_chances)

			###---POTIONS---###

			if choice == 'heal':

				item_component = Item(use_function=cast_heal)
				item_component.description = HEALING_POTION_DESCR
				item = Object(x, y, healthpot_tile, 'healing potion', libtcod.white, item=item_component)

			elif choice == 'magic potion':

				item_component = Item(use_function=cast_magic_buff)
				item_component.description = POTION_OF_MAGIC_DESCR
				item = Object(x, y, magicpot_tile, 'potion of magic', libtcod.white, item=item_component)

			elif choice == 'berserker potion':

				item_component = Item(use_function=cast_berserk)
				item_component.description = POTION_OF_BERSERK_DESCR
				item = Object(x, y, berserkpot_tile, 'potion of berserk', libtcod.white, item=item_component)

			elif choice == 'mana':

				item_component = Item(use_function=cast_restore_mana)
				item_component.description = MANA_POTION_DESCR
				item = Object(x, y, manapot_tile, 'mana potion', libtcod.white, item=item_component)

			###---SCROLLS---###

			elif choice == 'lightning':

				item_component = Item(use_function=cast_lightning)
				item_component.description = SCROLL_LIGHTNING_BOLT_DESCR
				item = Object(x, y, scroll_tile, 'scroll of lightning bolt', libtcod.white, item=item_component)

			elif choice == 'confuse':

				item_component = Item(use_function=cast_confuse)
				item_component.description = SCROLL_CONFUSION_DESCR
				item = Object(x, y, scroll_tile, 'scroll of confusion', libtcod.white, item=item_component)

			elif choice == 'fireball':

				item_component = Item(use_function=cast_fireball)
				item_component.description = SCROLL_FIREBALL_DESCR
				item = Object(x, y, scroll_tile, 'scroll of fireball', libtcod.white, item=item_component)

			elif choice == 'scroll of knowledge':

				item_component = Item(use_function=gain_skill)
				item_component.description = SCROLL_KNOWLEDGE_DESCR
				item = Object(x, y, scroll_tile, 'scroll of knowledge', libtcod.white, item=item_component)

			###---TIER 1 ITEMS---###

			elif choice == 'cap':

				def_mod = item_rand(2)
				maxhp_mod = item_rand(3)
				maxmp_mod = item_rand(2)

				equipment_component = Equipment(slot='head', defense_bonus=1+def_mod, max_hp_bonus=-1+maxhp_mod, max_mana_bonus=0+maxmp_mod)	
				item = Object(x, y, 'n', 'cap', libtcod.dark_sepia, equipment=equipment_component)
				item.item.description = CAP_DESCR

			elif choice == 'cape':

				def_mod = item_rand(2)
				maxhp_mod = item_rand(3)

				dice = libtcod.random_get_int(0, 0, 100)

				equipment_component = Equipment(slot='body', defense_bonus=2+def_mod, max_hp_bonus=2+maxhp_mod)
				item = Object(x, y, 'M', 'cape', libtcod.light_blue, equipment=equipment_component)
				item.item.description = CAPE_DESCR

			elif choice == 'robe':

				def_mod = item_rand(1)
				maxhp_mod = item_rand(2)
				maxmp_mod = item_rand(2)

				equipment_component = Equipment(slot='body', defense_bonus=1+def_mod, magic_bonus=1, max_hp_bonus=-2+maxhp_mod, max_mana_bonus=1+maxmp_mod)
				item = Object(x, y, 'R', 'robe', libtcod.desaturated_sky, equipment=equipment_component)
				item.item.description = ROBE_DESCR

			elif choice == 'short sword':

				pwr_mod = item_rand(1)
				def_mod = item_rand(2)
				maxhp_mod = item_rand(4)

				quality = [pwr_mod, def_mod, maxhp_mod]

				if sum(quality) > 5:
					name = 'polished sword'
				else:
					name = 'crude sword'

				equipment_component = Equipment(slot='right hand', power_bonus=1+pwr_mod, defense_bonus=0+def_mod, max_hp_bonus=1+maxhp_mod)
				item = Object(x, y, '/', name, libtcod.sky, equipment=equipment_component)
				if name == 'polished sword':
					item.item.description = SWORD_E_DESCR
				else:
					item.item.description = SWORD_DESCR

			elif choice == 'wooden shield':

				def_mod = item_rand(3)
				maxhp_mod = item_rand(4)

				quality = [def_mod, maxhp_mod]

				if sum(quality) > 5:
					name = 'high-quality wooden shield'
				else:
					name = 'stained wooden shield'

				equipment_component = Equipment(slot='left hand', defense_bonus=1+def_mod, armor_bonus=0, max_hp_bonus=1+maxhp_mod)
				item = Object(x, y, 'D', name, libtcod.darker_green, equipment=equipment_component)
				if name == 'high-quality wooden shield':
					item.item.description = WOODEN_SHIELD_E_DESCR
				else:
					item.item.description = WOODEN_SHIELD_DESCR

			elif choice == 'dagger':

				pwr_mod = item_rand(1)
				def_mod = item_rand(2)
				maxhp_mod = item_rand(2)

				quality = [pwr_mod, def_mod, maxhp_mod]

				if pwr_mod == 1:
					name = 'fine dagger'
				else:
					name = 'rusty dagger'

				equipment_component = Equipment(slot='right hand', power_bonus=1+pwr_mod, defense_bonus=2+def_mod, max_hp_bonus=-4+maxhp_mod)
				item = Object(x, y, '-', name, libtcod.gray, equipment=equipment_component)
				if name == 'fine dagger':
					item.item.description = DAGGER_E_DESCR
				else:
					item.item.description = DAGGER_DESCR

			elif choice == 'wand':

				maxmp_mod = item_rand(1)
				mag_mod = 0

				chance = libtcod.random_get_int(0, 0, 100)

				if chance > 85:
					mag_mod += 1
					name = 'fine magical wand'
				else:
					name = 'magical wand'

				equipment_component = Equipment(slot='right hand', max_mana_bonus=2+maxmp_mod, magic_bonus=1+mag_mod)
				item = Object(x, y, 'i', name, libtcod.purple, equipment=equipment_component)
				if name == 'fine magical wand':
					item.item.description = MAGICAL_WAND_E_DESCR
				else:
					item.item.description = MAGICAL_WAND_DESCR

			elif choice == 'small axe':

				def_mod = item_rand(2)
				maxhp_mod = item_rand(2)

				equipment_component = Equipment(slot='right hand', power_bonus=2, defense_bonus=-2+def_mod, max_hp_bonus=-2+maxhp_mod)
				item = Object(x, y, 'p', 'small axe', libtcod.light_gray, equipment=equipment_component)
				item.item.description = SMALL_AXE_DESCR

			elif choice == 'mace':

				def_mod = item_rand(2)
				maxhp_mod = item_rand(2)

				equipment_component = Equipment(slot='right hand', power_bonus=2, defense_bonus=0+def_mod, max_hp_bonus=0+maxhp_mod)
				item = Object(x, y, 't', 'mace', libtcod.silver, equipment=equipment_component)
				item.item.description = MACE_DESCR

			###---TIER 2 ITEMS---###

			elif choice == 'chained helmet':

				maxhp_mod = item_rand(2)
				def_mod = item_rand(3)

				name = 'chained helmet'

				equipment_component = Equipment(slot='head', armor_bonus=1, defense_bonus=-2+def_mod, max_hp_bonus=2+maxhp_mod)
				item = Object(x, y, 'n', name, libtcod.white, equipment=equipment_component)
				item.item.description = CHAINED_HELMET_DESCR

			elif choice == 'leather armor':

				def_mod = item_rand(2)
				maxhp_mod = item_rand(3)
				
				
				name = 'leather armor'

				equipment_component = Equipment(slot='body', armor_bonus=1, defense_bonus=2+def_mod, max_hp_bonus=4+maxhp_mod, max_mana_bonus=-1)
				item = Object(x, y, 'H', name, libtcod.dark_green, equipment=equipment_component)
				item.item.description = LEATHER_ARMOR_DESCR

			elif choice == 'sharpened dagger':

				pwr_mod = item_rand(1)
				def_mod = item_rand(3)
				maxhp_mod = item_rand(2)

				quality = [pwr_mod, def_mod, maxhp_mod]

				if sum(quality) > 5 and pwr_mod == 1:
					name = 'high-quality sharpened dagger'
				else:
					name = 'sharpened dagger'

				equipment_component = Equipment(slot='right hand', power_bonus=2+pwr_mod, defense_bonus=4+def_mod, max_hp_bonus=-6+maxhp_mod)
				item = Object(x, y, '-', name, libtcod.dark_sea, equipment=equipment_component)
				if name == 'high-quality sharpened dagger':
					item.item.description = SHARPENED_DAGGER_E_DESCR
				else:
					item.item.description = SHARPENED_DAGGER_DESCR

			elif choice == 'wave-patterned sword':

				def_mod = item_rand(3)
				maxhp_mod = item_rand(2)
		
				name = 'wave-patterned sword'

				equipment_component = Equipment(slot='right hand', power_bonus=2, defense_bonus=2+def_mod, max_hp_bonus=4+maxhp_mod)
				item = Object(x, y, '/', name, libtcod.amber, equipment=equipment_component)
				item.item.description = WAVE_PATTERNED_SWORD_DESCR

			elif choice == 'large axe':

				def_mod = item_rand(2)
				maxhp_mod = item_rand(3)
				fight_mod = 0

				chance = libtcod.random_get_int(0, 0, 100)

				if chance > 75:
					fight_mod += 1
					name = 'splendid large axe'
				else:
					name = 'large axe'

				equipment_component = Equipment(slot='right hand', power_bonus=3, defense_bonus=-4+def_mod, max_hp_bonus=-6+maxhp_mod, fighting_bonus=0+fight_mod)
				item = Object(x, y, 'p', name, libtcod.sepia, equipment=equipment_component)
				if name == 'splendid large axe':
					item.item.description = LARGE_AXE_E_DESCR
				else:
					item.item.description = LARGE_AXE_DESCR

			elif choice == 'spiked mace':

				def_mod = item_rand(3)
				maxhp_mod = item_rand(4)

				equipment_component = Equipment(slot='right hand', power_bonus=3, defense_bonus=0+def_mod, max_hp_bonus=0+maxhp_mod)
				item = Object(x, y, 't', 'spiked mace', libtcod.light_gray, equipment=equipment_component)
				item.item.description = SPIKED_MACE_DESCR

			elif choice == 'rondache':

				def_mod = item_rand(2)
				maxhp_mod = item_rand(3)
				name = 'rondache'

				equipment_component = Equipment(slot='left hand', defense_bonus=2+def_mod, armor_bonus=1, max_hp_bonus=1+maxhp_mod)
				item = Object(x, y, 'D', name, libtcod.silver, equipment=equipment_component)
				item.item.description = RONDACHE_DESCR

			elif choice == 'short staff':

				maxmp_mod = item_rand(3)
				def_mod = item_rand(2)

				name = 'short staff'

				equipment_component = Equipment(slot='right hand', power_bonus=1, defense_bonus=0+def_mod, max_mana_bonus=2+maxmp_mod, magic_bonus=2)
				item = Object(x, y, 'i', name, libtcod.dark_turquoise, equipment=equipment_component)
				item.item.description = SHORT_STAFF_DESCR

			elif choice == 'quilted armor':

				def_mod = item_rand(2)
				maxhp_mod = item_rand(3)
				maxmp_mod = item_rand(2)

				equipment_component = Equipment(slot='body', defense_bonus=3+def_mod, magic_bonus=1, armor_bonus=1, max_hp_bonus=0+maxhp_mod, max_mana_bonus=0+maxmp_mod)
				item = Object(x, y, 'H', 'quilted armor', libtcod.dark_sepia, equipment=equipment_component)
				item.item.description = QUILTED_ARMOR_DESCR

			elif choice == 'longbow':

				equipment_component = Equipment(slot='ranged weapon', power_bonus=2, prof_restriction=['Stalker'])
				item = Object(x, y, 'L', 'longbow', libtcod.dark_sepia, equipment=equipment_component)
				item.item.description = LONGBOW_DESCR

			###---TIER 3 ITEMS---###

			elif choice == 'chain mail':

				def_mod = item_rand(2)
				maxhp_mod = item_rand(4)
				
				name = 'chain mail'

				equipment_component = Equipment(slot='body', magic_bonus=-1, armor_bonus=3, defense_bonus=-4+def_mod, max_hp_bonus=6+maxhp_mod, max_mana_bonus=-4)
				item = Object(x, y, 'H', name, libtcod.silver, equipment=equipment_component)
				item.item.description = CHAIN_MAIL_DESCR

			elif choice == 'visored close helmet':

				def_mod = item_rand(2)
				maxhp_mod = item_rand(4)

				name = 'visored close helmet'

				equipment_component = Equipment(slot='head', armor_bonus=1, defense_bonus=3+def_mod, max_hp_bonus=5+maxhp_mod, magic_resist_bonus=0.05)
				item = Object(x, y, 'n', name, libtcod.light_sepia, equipment=equipment_component)
				item.item.description = VISORED_CLOSE_HELMET_DESCR

			elif choice == 'long sword':

				def_mod = item_rand(3)
				maxhp_mod = item_rand(4)

				name = 'long sword'

				equipment_component = Equipment(slot='right hand', power_bonus=3, defense_bonus=4+def_mod, max_hp_bonus=6+maxhp_mod)
				item = Object(x, y, '/', name, libtcod.crimson, equipment=equipment_component)
				item.item.description = LONG_SWORD_DESCR

			elif choice == 'ceremonial robes':

				def_mod = item_rand(2)
				maxhp_mod = item_rand(4)
				maxmp_mod = item_rand(2)

				name = 'ceremonial robes'

				equipment_component = Equipment(slot='body', defense_bonus=2+def_mod, magic_bonus=2, max_mana_bonus=2+maxmp_mod, max_hp_bonus=0+maxhp_mod)
				item = Object(x, y, 'R', name, libtcod.dark_lime, equipment=equipment_component)
				item.item.description = CEREMONIAL_ROBES_DESCR

			elif choice == 'large shield':

				def_mod = item_rand(3)
				maxhp_mod = item_rand(4)

				equipment_component = Equipment(slot='left hand', defense_bonus=6+def_mod, armor_bonus=2, max_hp_bonus=2+maxhp_mod, speed_bonus=-2)
				item = Object(x, y, 'D', 'large shield', libtcod.darker_sepia, equipment=equipment_component)
				item.item.description = LARGE_SHIELD_DESCR

			elif choice == 'azure shiv':

				pwr_mod = item_rand(1)
				def_mod = item_rand(5)
				maxhp_mod = item_rand(3)

				name = 'azure shiv'


				equipment_component = Equipment(slot='right hand', power_bonus=3+pwr_mod, defense_bonus=4+def_mod, max_hp_bonus=-8+maxhp_mod)
				item = Object(x, y, '_', name, libtcod.dark_azure, equipment=equipment_component)
				item.item.description = AZURE_SHIV_DESCR

			elif choice == 'runic wand':

				mag_mod = item_rand(1)
				maxmp_mod = item_rand(2)
				conj_mod = 0
				transm_mod = 0
				hex_mod = 0

				chance = libtcod.random_get_int(0, 0, 100)

				if chance > 85:
					conj_mod += 1
					conj = "conjurer's"
					name = '%s runic wand' % conj

				elif chance > 70:
					transm_mod += 1
					transm = "alchemist's"
					name = '%s runic wand' % transm

				elif chance > 55:
					hex_mod += 1
					hexer = "witch-doctor's"
					name = '%s runic wand' % hexer

				else:
					name = 'runic wand'

				equipment_component = Equipment(slot='right hand', magic_bonus=3+mag_mod, max_mana_bonus=4+maxmp_mod, conjuring_bonus=0+conj_mod, transmutations_bonus=0+transm_mod, hexes_bonus=0+hex_mod)
				item = Object(x, y, 'I', name, libtcod.dark_crimson, equipment=equipment_component)
				item.item.description = RUNIC_WAND_DESCR

			elif choice == 'war mace':

				def_mod = item_rand(4)
				maxhp_mod = item_rand(6)
				fight_mod = 0

				chance = libtcod.random_get_int(0, 0, 100)

				if chance > 75:
					fight_mod += 1
					name = 'brutal war mace'
				else:
					name = 'war mace'

				equipment_component = Equipment(slot='right hand', power_bonus=4, defense_bonus=0+def_mod, max_hp_bonus=0+maxhp_mod, fighting_bonus=0+fight_mod)
				item = Object(x, y, 'P', name, libtcod.dark_sepia, equipment=equipment_component)
				if name == 'brutal war mace':
					item.item.description = WAR_MACE_E_DESCR
				else:
					item.item.description = WAR_MACE_DESCR

			elif choice == 'battle axe':

				def_mod = item_rand(2)
				maxhp_mod = item_rand(3)
				fight_mod = 0

				chance = libtcod.random_get_int(0, 0, 100)

				if chance + dungeon_level*2 > 80:

					fight_mod += 1
					name = 'enchanted battle axe'
				else:
					name = 'battle axe'

				equipment_component = Equipment(slot='right hand', power_bonus=5, defense_bonus=-6+def_mod, max_hp_bonus=-8+maxhp_mod, fighting_bonus=0+fight_mod)
				item = Object(x, y, 'p', name, libtcod.darker_amber, equipment=equipment_component)
				if name == 'enchanted battle axe':
					item.item.description = BATTLE_AXE_E_DESCR
				else:
					item.item.description = BATTLE_AXE_DESCR

			elif choice == 'hard leather armor':

				def_mod = item_rand(2)
				maxhp_mod = item_rand(2)

				equipment_component = Equipment(slot='body', defense_bonus=0+def_mod, armor_bonus=2, max_hp_bonus=2+maxhp_mod, max_mana_bonus=-2)
				item = Object(x, y, 'H', 'hard leather armor', libtcod.dark_sepia, equipment=equipment_component)
				item.item.description = HARD_LEATHER_DESCR

			elif choice == 'crossbow':

				equipment_component = Equipment(slot='ranged weapon', power_bonus=3, archery_bonus=1, prof_restriction=['Stalker'])
				item = Object(x, y, 'k', 'crossbow', libtcod.desaturated_crimson, equipment=equipment_component)
				item.item.description = CROSSBOW_DESCR

			###---TIER 4 ITEMS---###

			elif choice == 'full helm':

				def_mod = item_rand(3)
				maxhp_mod = item_rand(6)

				equipment_component = Equipment(slot='head', defense_bonus=4+def_mod, armor_bonus=2, max_hp_bonus=5+maxhp_mod, shielding_bonus=1)
				item = Object(x, y, 'n', 'full helm', libtcod.darker_turquoise, equipment=equipment_component)
				item.item.description = FULL_HELM_DESCR

			elif choice == 'noble mask':

				def_mod = item_rand(3)
				maxmp_mod = item_rand(3)

				equipment_component = Equipment(slot='head', defense_bonus=2+def_mod, magic_bonus=2, armor_bonus=1, max_mana_bonus=3+maxmp_mod)
				item = Object(x, y, 'a', 'noble mask', libtcod.darker_amber, equipment=equipment_component)
				item.item.description = NOBLE_MASK_DESCR

			elif choice == 'breast plate':

				def_mod = item_rand(2)
				maxhp_mod = item_rand(5)

				equipment_component = Equipment(slot='body', defense_bonus=-4+def_mod, magic_bonus=-1, armor_bonus=3, max_hp_bonus=8, max_mana_bonus=-5, shielding_bonus=1)
				item = Object(x, y, 'H', 'breast plate', libtcod.lighter_azure, equipment=equipment_component)
				item.item.description = BREAST_PLATE_DESCR

			elif choice == 'trollweave':

				def_mod = item_rand(4)
				mag_mod = item_rand(1)
				maxhp_mod = item_rand(4)
				maxmp_mod = item_rand(2)
				conj_mod = 0
				transm_mod = 0
				hex_mod = 0
				mr_mod = libtcod.random_get_int(0, 2, 9)/100

				dice = libtcod.random_get_int(0, 0, 100)

				if dice > 85:
					conj_mod += 1
					conj = "conjurer's"
					name = '%s trollweave' % conj
				elif dice > 70:
					transm_mod += 1
					transm = "alchemist's"
					name = '%s trollweave' % transm
				elif dice > 55:
					hex_mod += 1
					hexer = "witch-doctor's"
					name = '%s trollweave' % hexer
				else:
					name = 'trollweave'

				equipment_component = Equipment(slot='body', defense_bonus=2+def_mod, magic_bonus=3+mag_mod, max_hp_bonus=4+maxhp_mod, max_mana_bonus=4+maxmp_mod, conjuring_bonus=0+conj_mod, transmutations_bonus=0+transm_mod, hexes_bonus=0+hex_mod, magic_resist_bonus=mr_mod)
				item = Object(x, y, 'R', name, libtcod.dark_lime, equipment=equipment_component)
				item.item.description = TROLLWEAVE_DESCR

			elif choice == 'cleaver':

				def_mod = item_rand(3)
				maxhp_mod = item_rand(3)

				equipment_component = Equipment(slot='right hand', power_bonus=5, defense_bonus=-8+def_mod, max_hp_bonus=-11+maxhp_mod, fighting_bonus=1)
				item = Object(x, y, 'p', 'cleaver', libtcod.darker_violet, equipment=equipment_component)
				item.item.description = CLEAVER_DESCR

			elif choice == 'falcata':

				def_mod = item_rand(3)
				maxhp_mod = item_rand(5)

				equipment_component = Equipment(slot='right hand', power_bonus=4, defense_bonus=5+def_mod, max_hp_bonus=9+maxhp_mod)
				item = Object(x, y, '/', 'falcata', libtcod.desaturated_sea, equipment=equipment_component)
				item.item.description = FALCATA_DESCR

			elif choice == 'trident dagger':

				pwr_mod = item_rand(1)
				def_mod = item_rand(5)
				maxhp_mod = item_rand(3)

				equipment_component = Equipment(slot='right hand', power_bonus=4+pwr_mod, defense_bonus=6+def_mod, max_hp_bonus=-11+maxhp_mod)
				item = Object(x, y, 't', 'trident dagger', libtcod.dark_gray, equipment=equipment_component)
				item.item.description = TRIDENT_DAGGER_DESCR

			elif choice == 'giant maul':

				def_mod = item_rand(5)
				maxhp_mod = item_rand(7)

				equipment_component = Equipment(slot='right hand', power_bonus=5, defense_bonus=0+def_mod, max_hp_bonus=0+maxhp_mod)
				item = Object(x, y, 'q', 'giant maul', libtcod.dark_han, equipment=equipment_component)
				item.item.description = GIANT_MAUL_DESCR

			elif choice == 'long staff':

				def_mod = item_rand(2)
				mag_mod = item_rand(1)
				maxmp_mod = item_rand(3)
				conj_mod = 0
				transm_mod = 0
				hex_mod = 0
				mr_mod = libtcod.random_get_int(0, 3, 11)/100

				dice = libtcod.random_get_int(0, 0, 100)

				if dice > 85:
					conj_mod += 1
					conj = "conjurer's"
					name = '%s long staff' % conj
				elif dice > 70:
					transm_mod += 1
					transm = "alchemist's"
					name = '%s long staff' % transm
				elif dice > 55:
					hex_mod += 1
					hexer = "witch-doctor's"
					name = '%s long staff' % hexer
				else:
					name = 'long staff'

				equipment_component = Equipment(slot='right hand', power_bonus=2, defense_bonus=2+def_mod, magic_bonus=4+mag_mod, max_mana_bonus=4+maxmp_mod, conjuring_bonus=0+conj_mod, transmutations_bonus=0+transm_mod, hexes_bonus=0+hex_mod, magic_resist_bonus=mr_mod)
				item = Object(x, y, 'I', name, libtcod.light_purple, equipment=equipment_component)
				item.item.description = LONG_STAFF_DESCR

			elif choice == 'tower shield':

				def_mod = item_rand(4)
				maxhp_mod = item_rand(4)
				shielding_mod = 0

				chance = libtcod.random_get_int(0, 0, 100)

				if chance > 75: 
					shielding_mod += 1
					name = 'fantastic tower shield'
				else:
					name = 'tower shield'

				equipment_component = Equipment(slot='left hand', defense_bonus=3+def_mod, armor_bonus=2, max_hp_bonus=4+maxhp_mod, shielding_bonus=1+shielding_mod, prof_restriction=['Fighter'])
				item = Object(x, y, 'D', name, libtcod.dark_orange, equipment=equipment_component)
				if name == 'fantastic tower shield':
					item.item.description = TOWER_SHIELD_E_DESCR
				else:
					item.item.description = TOWER_SHIELD_DESCR

			elif choice == 'double bow':

				equipment_component = Equipment(slot='ranged weapon', power_bonus=4, archery_bonus=1, prof_restriction=['Stalker'])
				item = Object(x, y, 'B', 'double bow', libtcod.dark_sepia, equipment=equipment_component)
				item.item.description = DOUBLE_BOW_DESCR

			###---TIER 5 ITEMS---###

			elif choice == 'winged helmet':

				def_mod = item_rand(3)
				maxhp_mod = item_rand(6)

				equipment_component = Equipment(slot='head', defense_bonus=5+def_mod, armor_bonus=3, max_hp_bonus=8+maxhp_mod, shielding_bonus=1)
				item = Object(x, y, 'n', 'winged helmet', libtcod.desaturated_flame, equipment=equipment_component)
				item.item.description = WINGED_HELMET_DESCR

			elif choice == 'full plate mail':

				def_mod = item_rand(2)
				maxhp_mod = item_rand(7)

				equipment_component = Equipment(slot='body', defense_bonus=-6+def_mod, magic_bonus=-2, armor_bonus=4, max_hp_bonus=10+maxhp_mod, max_mana_bonus=-5, shielding_bonus=1)
				item = Object(x, y, 'H', 'full plate mail', libtcod.darker_crimson, equipment=equipment_component)
				item.item.description = FULL_PLATE_MAIL_DESCR

			elif choice == 'panaba':

				pwr_mod = item_rand(1)
				def_mod = item_rand(6)
				maxhp_mod = item_rand(4)

				equipment_component = Equipment(slot='right hand', power_bonus=6+pwr_mod, defense_bonus=-10+def_mod, max_hp_bonus=-15+maxhp_mod, fighting_bonus=2)
				item = Object(x, y, 'J', 'panaba', libtcod.darkest_cyan, equipment=equipment_component)
				item.item.description = PANABA_DESCR

			elif choice == 'great sword':

				def_mod = item_rand(4)
				maxhp_mod = item_rand(6)

				equipment_component = Equipment(slot='right hand', power_bonus=6, defense_bonus=6+def_mod, max_hp_bonus=13+maxhp_mod, fighting_bonus=1)
				item = Object(x, y, '/', 'great sword', libtcod.dark_azure, equipment=equipment_component)
				item.item.description = GREAT_SWORD_DESCR

			elif choice == 'oakwood spire':

				mag_mod = item_rand(2)
				maxmp_mod = item_rand(3)
				conj_mod = 0
				transm_mod = 0
				hex_mod = 0
				mr_mod = libtcod.random_get_int(0, 5, 14)/100

				dice = libtcod.random_get_int(0, 0, 100)

				name = 'oakwood spire'

				if dice > 85:
					conj_mod += 2
					conj = "conjurer's"
					name = '%s oakwood spire' % conj
				elif dice > 70:
					transm_mod += 2
					transm = "alchemist's"
					name = '%s oakwood spire' % transm
				elif dice > 55:
					hex_mod += 2
					hexer = "witch-doctor's"
					name = '%s oakwood spire' % hexer

				equipment_component = Equipment(slot='right hand', magic_bonus=5+mag_mod, max_mana_bonus=6+maxmp_mod, conjuring_bonus=0+conj_mod, transmutations_bonus=0+transm_mod, hexes_bonus=0+hex_mod, magic_resist_bonus=mr_mod)
				item = Object(x, y, 'j', name, libtcod.darker_amber, equipment=equipment_component)
				item.item.description = OAKWOOD_SPIRE_DESCR

			elif choice == 'greatshield':

				def_mod = item_rand(4)
				maxhp_mod = item_rand(5)

				equipment_component = Equipment(slot='left hand', defense_bonus=6+def_mod, armor_bonus=3, max_hp_bonus=8+maxhp_mod, shielding_bonus=1)
				item = Object(x, y, 'D', 'greatshield', libtcod.desaturated_han, equipment=equipment_component)
				item.item.description = GREATSHIELD_DESCR

			elif choice == 'arbalest':

				equipment_component = Equipment(slot='ranged weapon', power_bonus=5, archery_bonus=2)
				item = Object(x, y, 'K', 'arbalest', libtcod.dark_crimson, equipment=equipment_component)
				item.item.description = ARBALEST_DESCR

			###---ARTIFACTS---###

			###---TIER 1 ARTIFACTS---###

			elif choice == 'ivory visage':

				def_mod = item_rand(2)
				maxhp_mod = item_rand(3)

				equipment_component = Equipment(slot='head', defense_bonus=3+def_mod, magic_bonus=1, max_hp_bonus=3, max_mana_bonus=2, dmg_reduction_bonus=1)
				item = Object(x, y, 'n', 'ivory visage', libtcod.dark_orange, equipment=equipment_component)
				item.item.description = IVORY_VISAGE_DESCR

			elif choice == 'crystal ring':

				equipment_component = Equipment(slot='finger', fighting_bonus=1, shielding_bonus=1, archery_bonus=1, conjuring_bonus=1, transmutations_bonus=1, hexes_bonus=1)
				item = Object(x, y, 'Q', 'crystal ring', libtcod.dark_yellow, equipment=equipment_component)
				item.item.description = CRYSTAL_RING_DESCR

			elif choice == 'windsong silver blade':

				equipment_component = Equipment(slot='right hand', power_bonus=4, defense_bonus=12, fighting_bonus=1, lifesteal_bonus=1, speed_bonus=5, prof_restriction=['Fighter'])
				item = Object(x, y, '/', 'windsong silver blade', libtcod.dark_gray, equipment=equipment_component)
				item.item.description = WINDSONG_SILVER_BLADE_DESCR

			elif choice == 'cowl of divine sorrow':

				equipment_component = Equipment(slot='head', magic_bonus=3, conjuring_bonus=2, magic_resist_bonus=0.10, prof_restriction=['Conjurer', 'Hex Mage'])
				item = Object(x, y, 'e', 'cowl of divine sorrow', libtcod.sky, equipment=equipment_component)
				item.item.description = COWL_DIVINE_SORROW_DESCR

			elif choice == 'bloodcursed':

				equipment_component = Equipment(slot='ranged weapon', power_bonus=6, archery_bonus=2, speed_bonus=5, prof_restriction=['Stalker'])
				item = Object(x, y, 'k', 'bloodcursed crossbow', libtcod.crimson, equipment=equipment_component)
				item.item.description = BLOODCURSED_DESCR

			elif choice == 'wall of the wicked':

				equipment_component = Equipment(slot='left hand', defense_bonus=8, armor_bonus=4, max_hp_bonus=14, shielding_bonus=2, prof_restriction=['Fighter', 'Alchemist'])
				item = Object(x, y, 'D', 'wall of the wicked', libtcod.crimson, equipment=equipment_component)
				item.item.description = WALL_OF_THE_WICKED_DESCR

			elif choice == 'ornament of clarity':

				equipment_component = Equipment(slot='right hand', magic_bonus=4, max_mana_bonus=8, speed_bonus=5, prof_restriction=['Conjurer', 'Hex Mage', 'Alchemist'])
				item = Object(x, y, 'r', 'ornament of clarity', libtcod.crimson, equipment=equipment_component)
				item.item.description = ORNAMENT_OF_CLARITY_DESCR

			elif choice == 'dazzling tricellite ring':

				equipment_component = Equipment(slot='finger', defense_bonus=10, fighting_bonus=1, shielding_bonus=1, magic_resist_bonus=0.05, prof_restriction=['Fighter', 'Alchemist'])
				item = Object(x, y, 'Q', 'dazzling tricellite ring', libtcod.dark_azure, equipment=equipment_component)
				item.item.description = DAZZLING_TRICELLITE_RING_DESCR

			elif choice == 'maple battle staff':

				equipment_component = Equipment(slot='right hand', power_bonus=6, defense_bonus=14, magic_bonus=2, transmutations_bonus=2, prof_restriction=['Alchemist'])
				item = Object(x, y, 'I', 'maple battle staff', libtcod.dark_flame, equipment=equipment_component)
				item.item.description = MAPLE_BATTLE_STAFF_DESCR

			#elif choice == 'incense stick':

			#	equipment_component = Equipment(slot='right hand', defense_bonus=2, magic_bonus=4, transmutations_bonus=2, hexes_bonus=3, max_mana_bonus=5, prof_restriction['Hex Mage', 'Alchemist'])

			###---RINGS & AMULETS---###

			elif choice == 'amulet of resist magic':

				mr_mod = item_rand(10) * 0.01
				maxhp_mod = 0

				if mr_mod >= 0.08:
					maxhp_mod += 5
					name = 'amulet of spellshielding'
				else:
					name = 'amulet of magic protection'

				equipment_component = Equipment(slot='neck', magic_resist_bonus=0.15+mr_mod, max_hp_bonus=maxhp_mod)
				item = Object(x, y, 'v', name, libtcod.dark_red, equipment=equipment_component)
				if name == 'amulet of spellshielding':
					item.item.description = AMULET_OF_MAGIC_PROTECTION_E_DESCR
				else:
					item.item.description = AMULET_OF_MAGIC_PROTECTION_DESCR

			elif choice == 'amulet of speed':

				equipment_component = Equipment(slot='neck', speed_bonus=item_rand(5))
				item = Object(x, y, 'v', 'amulet of speed', libtcod.light_blue, equipment=equipment_component)
				item.item.description = AMULET_OF_SPEED_DESCR

			elif choice == 'ring of amp':

				equipment_component = Equipment(slot='finger', damage_amp_bonus=0.25)
				item = Object(x, y, 'Q', 'ring of amplification', libtcod.crimson, equipment=equipment_component)
				item.item.description = RING_OF_AMPLIFICATION_DESCR

			elif choice == 'ring of protection':

				equipment_component = Equipment(slot='finger', armor_bonus=1)
				item = Object(x, y, 'Q', 'ring of protection', libtcod.copper, equipment=equipment_component)
				item.item.description = RING_OF_PROTECTION_DESCR

			elif choice == 'arcane ring':

				equipment_component = Equipment(slot='finger', magic_bonus=1)
				item = Object(x, y, 'Q', 'arcane ring', libtcod.light_violet, equipment=equipment_component)
				item.item.description = ARCANE_RING_DESCR

			elif choice == 'ring of vigor':

				def_mod = item_rand(4)
				maxhp_mod = item_rand(4)

				quality = [def_mod, maxhp_mod]

				if sum(quality) > 5:
					name = 'ring of agility'
				else:
					name = 'ring of vigor'

				equipment_component = Equipment(slot='finger', defense_bonus=3+def_mod, max_hp_bonus=2+maxhp_mod, speed_bonus=2)
				item = Object(x, y, 'Q', name, libtcod.darker_yellow, equipment=equipment_component)
				if name == 'ring of agility':
					item.item.description = RING_OF_AGILITY_E_DESCR
				else:
					item.item.description = RING_OF_AGILITY_DESCR

			elif choice == 'ring of evasion':

				equipment_component = Equipment(slot='finger', evasion_bonus=item_rand(5))
				item = Object(x, y, 'Q', 'ring of evasion', libtcod.dark_lime, equipment=equipment_component)
				item.item.description = RING_OF_EVASION_DESCR

			###---SPELLBOOKS---###

			elif choice == 'book of ice conj':

				item_component = Item(use_function=learn_spell_ice_conj)
				item = Object(x, y, 'B', 'Book of Ice Conjurations', libtcod.darker_lime, item=item_component)
				item.item.description = BOOK_ICE_CONJ_DESCR

			elif choice == 'book of fire conj':
  				item_component = Item(use_function=learn_spell_fire_conj)
				item = Object(x, y, 'B', 'Book of Fire Conjurations', libtcod.darker_lime, item=item_component)
				item.item.description = BOOK_FIRE_CONJ_DESCR

			elif choice == 'book of transmutations':

				item_component = Item(use_function=learn_spell_transm)
				item = Object(x, y, 'B', 'Book of Transmutations', libtcod.darker_lime, item=item_component)
				item.item.description = BOOK_TRANSM_DESCR

			elif choice == 'book of hexes':

				item_component = Item(use_function=learn_spell_hex)
				item = Object(x, y, 'B', 'Book of Hexes', libtcod.darker_lime, item=item_component)
				item.item.description = BOOK_HEXES_DESCR

			elif choice == 'book of assorted spells':

				item_component = Item(use_function=learn_spell_assorted)
				item = Object(x, y, 'B', 'Gustor\'s lost magicbook', libtcod.dark_azure, item=item_component)
				item.item.description = BOOK_GUSTORS_DESCR

			elif choice == 'nothing':
				return

			print(choice)

			if item: 
				if item.equipment:
					dice = libtcod.random_get_int(0, 0, 100)
					if dice > 90:
						item = add_suffix(item)

				objects.append(item)
				item.send_to_back()
				item.always_visible = True

def item_rand(interval):
	
	value = libtcod.random_get_int(0, 0, interval)
	return value

def add_suffix(obj):

	suffixes = [' of might', ' of the ox', ' of protection', ' of deflection', ' of brilliance',
				' of wizardry', ' of the wolf', ' of the colossus', ' of energy', ' of the mind',
				' of warmongering', ' of blocking', ' of evocations', ' of hunting', ' of spellcrafting',
				' of transmutations']

	length = len(suffixes)

	suffix = libtcod.random_get_int(0, 0, (length-1))

	if obj.equipment.slot != 'finger' and obj.equipment.slot != 'neck':
		obj.name += suffixes[suffix]

	if suffix == 0:
		obj.equipment.power_bonus += 1
	elif suffix == 1:
		obj.equipment.power_bonus += 2
	elif suffix == 2:
		obj.equipment.defense_bonus += libtcod.random_get_int(0, 1, 3)
	elif suffix == 3:
		obj.equipment.defense_bonus += libtcod.random_get_int(0, 3, 6)
	elif suffix == 4:
		obj.equipment.magic_bonus += 1
	elif suffix == 5:
		obj.equipment.magic_bonus += 2
	elif suffix == 6:
		obj.equipment.max_hp_bonus += libtcod.random_get_int(0, 2, 5)
	elif suffix == 7:
		obj.equipment.max_hp_bonus += libtcod.random_get_int(0, 5, 10)
	elif suffix == 8:
		obj.equipment.max_mana_bonus += libtcod.random_get_int(0, 2, 4)
	elif suffix == 9:
		obj.equipment.max_mana_bonus += libtcod.random_get_int(0, 4, 7)
	elif suffix == 10:
		obj.equipment.fighting_bonus += 1
	elif suffix == 11:
		obj.equipment.shielding_bonus += 1
	elif suffix == 12:
		obj.equipment.conjuring_bonus += 1
	elif suffix == 13:
		obj.equipment.archery_bonus += 1
	elif suffix == 14:
		obj.equipment.hexes_bonus += 1
	elif suffix == 15:
		obj.equipment.transmutations_bonus += 1

	return obj

def is_blocked(x, y):
	if tilemap[x][y].blocked:
		return True
	for object in objects:
		if object.blocks and object.x == x and object.y == y:
			return True
	return False

def player_move_or_attack(dx, dy):
	global fov_recompute

	x = player.x + dx
	y = player.y + dy

	target = None
	for object in objects:
		if object.fighter and object.x == x and object.y == y:
			target = object
			break

	if target is not None:
		player.fighter.attack(target)
	else:
		player.move(dx, dy)
		fov_recompute = True

def player_death(player):
	global game_state
	message('You have died!', libtcod.dark_red)
	game_state = 'dead'

	player.char = 'X'
	player.color = libtcod.dark_red

def monster_death(monster):
	if player.race == 'Human': 
		message('You have slain the ' + monster.name + '! You gain ' + str(int(round(monster.fighter.xp * 1.33))) + ' experience.', libtcod.orange)
	else:
		message('You have slain the ' + monster.name + '! You gain ' + str(monster.fighter.xp) + ' experience.', libtcod.orange)
		
	monster.char = 'x'
	monster.color = libtcod.dark_red
	monster.blocks = False
	monster.fighter = None
	monster.ai = None
	monster.name = 'remains of ' + monster.name
	monster.send_to_back()

	try:
		monster.timeobj.release()
	except AttributeError:
		print('Tried to release ' + monster.name + ' but no time component found!')
		


	if player.race == 'Dwarf':
		div = libtcod.random_get_int(0, 12, 20)
		amount = int(round(player.fighter.max_hp/div))
		player.fighter.heal(amount)
		message('Your dwarven fighting spirit empowers you! You heal for ' + str(amount) + ' hit points.', libtcod.light_blue)
	elif player.race == 'Gnome':
		player.fighter.restore_mana(1)
		message('Your Gnomish grit augments your magical powers! Gained 1 mana.')

	if player.fighter.heal_kill != 0:
		for i in range(player.fighter.heal_kill):
			dice = libtcod.random_get_int(0, 0, 100)
			if dice > 60:
				 dice2 = libtcod.random_get_int(0, 0, 100)
				 if dice2 > 50:
				 	amount = int(round(player.fighter.max_hp/20))
				 	if amount == 0:
				 		amount = 1
				 	player.fighter.heal(amount)
				 	message('You gain ' + str(amount) + ' hit points from slaying the ' + monster.name + '!', libtcod.light_blue)
				 else:
				 	amount = int(round(player.fighter.max_mana/20))
				 	if amount == 0:
				 		amount = 1
				 	player.fighter.restore_mana(amount)
				 	message('You gain ' + str(amount) + ' points of mana from slaying the ' + monster.name + '!', libtcod.light_blue)

	player.fighter.reset_kill_window()

def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
	bar_width = int(float(value) / maximum * total_width)

	libtcod.console_set_default_background(panel, back_color)
	libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

	libtcod.console_set_default_background(panel, bar_color)
	if bar_width > 0:
		libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

	libtcod.console_set_default_foreground(panel, libtcod.white)
	libtcod.console_print_ex(panel, x + total_width/2, y, libtcod.BKGND_NONE, libtcod.CENTER, 
		name + ': ' + str(value) + '/' + str(maximum))

def message(new_msg, color = libtcod.white):

	new_msg_lines = textwrap.wrap(new_msg, MSG_WIDTH)

	for line in new_msg_lines:
		if len(game_msgs) == MSG_HEIGHT:
			del game_msgs[0]
		game_msgs.append( (line, color) )

def get_names_under_mouse():
	global mouse

	(x, y) = (mouse.cx, mouse.cy)

	names = [obj.name for obj in objects
		if obj.x == x and obj.y == y and libtcod.map_is_in_fov(fov_map, obj.x, obj.y)]

	names = ', '.join(names)
	return names.capitalize()

def get_names_under_player():
	(x, y) = (player.x, player.y)
	names = [obj.name for obj in objects
		if obj.x == x and obj.y == y and obj != player]

	names = ', '.join(names)
	return names.capitalize()

def menu(header, options, width, recomp=True):
	global key, mouse, menu_check, menu_recompute

	if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')
	header_height = libtcod.console_get_height_rect(con, 0, 0, width, SCREEN_HEIGHT, header)

	if header == '':
		header_height = 0
	height = len(options) + header_height
	window = libtcod.console_new(width, height)

	libtcod.console_set_default_foreground(window, libtcod.white)
	libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

	y = header_height
	letter_index = ord('a')
	for option_text in options:
		text = '(' + chr(letter_index) + ')' + option_text
		libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
		y += 1
		letter_index += 1

	x = SCREEN_WIDTH/2 - width/2
	y = SCREEN_HEIGHT/2 - height/2
	libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

	x_offset = x
	y_offset = y + header_height

	while True:
		if recomp == True:
			menu_check = True
		libtcod.console_flush()
		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

		if (mouse.lbutton_pressed):
			(menu_x, menu_y) = (mouse.cx - x_offset, mouse.cy - y_offset)
			if menu_x >= 0 and menu_x < width and menu_y >= 0 and menu_y < height - header_height:
				if recomp == True:
					menu_recompute = True
				return menu_y
				

		if mouse.rbutton_pressed or key.vk == libtcod.KEY_ESCAPE:
			if recomp == True:
				menu_recompute = True
			return None
			

		if key.vk == libtcod.KEY_ENTER and key.lalt:
			libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

		index = key.c - ord('a')
		if index >= 0 and index < len(options): 
			if recomp == True:
				menu_recompute = True
			return index
			
		if index >= 0 and index <= 26: 
			if recomp == True:
				menu_recompute = True
			return None

def transp_menu(header, options, width, transp):
	global key, mouse

	if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')
	header_height = libtcod.console_get_height_rect(con, 0, 0, width, SCREEN_HEIGHT, header)
	if header == '':
		header_height = 0
	height = len(options) + header_height
	window = libtcod.console_new(width, height)

	libtcod.console_set_default_foreground(window, libtcod.white)
	libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

	y = header_height
	letter_index = ord('a')
	for option_text in options:
		text = '(' + chr(letter_index) + ')' + option_text
		libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
		y += 1
		letter_index += 1

	x = SCREEN_WIDTH/2 - width/2
	y = SCREEN_HEIGHT/2 - height/2
	libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, transp)

	x_offset = x
	y_offset = y + header_height

	while True:
		libtcod.console_flush()
		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

		if (mouse.lbutton_pressed):
			(menu_x, menu_y) = (mouse.cx - x_offset, mouse.cy - y_offset)
			if menu_x >= 0 and menu_x < width and menu_y >= 0 and menu_y < height - header_height:
				return menu_y

		if mouse.rbutton_pressed or key.vk == libtcod.KEY_ESCAPE:
			return None

		if key.vk == libtcod.KEY_ENTER and key.lalt:
			libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

		index = key.c - ord('a')
		if index >= 0 and index < len(options): return index
		if index >= 0 and index <= 26: return None

def inventory_menu(header):
	global menu_check

	if len(inventory) == 0:
		options = ['Inventory is empty.']
	else:
		options = []
		for item in inventory:
			text = item.name
			if item.equipment and item.equipment.is_equipped:
				text = text + ' (on ' + item.equipment.slot + ')'
			options.append(text)

	index = menu(header, options, INVENTORY_WIDTH)
	if index is None or len(inventory) == 0:
 
		return None

	return inventory[index].item

def character_screen():
	global menu_check, menu_recompute

	level_up_xp = LEVEL_UP_BASE + player.level * LEVEL_UP_FACTOR

	header = 'Character information\n\n'

	level = 'Level: ' + str(player.level)
	xp = 'Current XP: ' + str(player.fighter.xp)
	next_level = 'Next level at: ' + str(level_up_xp) + '\n'

	max_hp = 'Max HP: ' + str(player.fighter.base_max_hp + player.fighter.fighting)
	max_hp_bonus = ''
	b = player.fighter.max_hp - player.fighter.base_max_hp - player.fighter.fighting
	if b > 0:
		max_hp_bonus = ' + ' + str(b)

	max_mana = 'Max MP: ' + str(player.fighter.max_mana) + '\n'
	max_mp_bonus = ''
	b = player.fighter.max_mana - player.fighter.base_max_mana
	if b > 0:
		max_mp_bonus = ' + ' + str(b)

	power = 'Power: ' + str(player.fighter.power)
	power_bonus = ''
	b = player.fighter.power - player.fighter.base_power
	if b > 0:
		power_bonus = ' + ' + str(b)

	defense = 'Defense: ' + str(player.fighter.defense)
	defense_bonus = ''
	b = player.fighter.defense - player.fighter.base_defense
	if b > 0:
		defense_bonus = ' + ' + str(b)

	armor = 'AC: ' + str(player.fighter.armor)
	armor_bonus = ''
	b = player.fighter.armor - player.fighter.base_armor
	if b > 0:
		armor_bonus = ' + ' + str(b)

	magic ='Magic: ' + str(player.fighter.magic) + '\n'
	magic_bonus = ''
	b = player.fighter.magic - player.fighter.base_magic
	if b > 0:
		magic_bonus = ' + ' + str(b)

	fighting = 'Fighting: ' + str(player.fighter.fighting)
	fighting_bonus = ''
	b = player.fighter.fighting - player.fighter.base_fighting
	if b > 0:
		fighting_bonus = ' + ' + str(b)

	shielding = 'Shielding: ' + str(player.fighter.shielding)
	shielding_bonus = ''
	b = player.fighter.shielding - player.fighter.base_shielding
	if b > 0:
		shielding_bonus = ' + ' + str(b)

	conjuring = 'Conjuring: ' + str(player.fighter.conjuring)
	conjuring_bonus = ''
	b = player.fighter.conjuring - player.fighter.base_conjuring
	if b > 0:
		conjuring_bonus = ' + ' + str(b)

	archery = 'Archery: ' + str(player.fighter.archery)
	archery_bonus = ''
	b = player.fighter.archery - player.fighter.base_archery
	if b > 0:
		archery_bonus = ' + ' + str(b)

	transmutations ='Transmutations: ' + str(player.fighter.transmutations)
	transmutations_bonus = ''
	b = player.fighter.transmutations - player.fighter.base_transmutations
	if b > 0:
		transmutations_bonus = ' + ' + str(b)

	hexes = 'Hexes: ' + str(player.fighter.hexes) + '\n'
	hexes_bonus = ''
	b = player.fighter.hexes - player.fighter.base_hexes
	if b > 0:
		hexes_bonus = ' + ' + str(b)

	buffs = [x.name for x in player.fighter.buff]
	effects = ', '.join(buffs) 
	status = 'Status Effects: ' + effects

	text = header + level + xp + next_level + max_hp + max_mana + power + defense + armor + magic + fighting + shielding + conjuring + archery + transmutations + hexes + status
	text_width = 50
	text_height = 25

	window = libtcod.console_new(text_width, text_height)

	y = 0
	libtcod.console_set_default_foreground(window, libtcod.white)
	libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, header)
	y += 2

	libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, level)
	y += 1
	libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, xp)
	y += 1
	libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, next_level)
	y += 2

	libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, max_hp)
	libtcod.console_set_default_foreground(window, libtcod.light_green)
	libtcod.console_print_ex(window, len(max_hp), y, libtcod.BKGND_NONE, libtcod.LEFT, max_hp_bonus)
	y += 1
	libtcod.console_set_default_foreground(window, libtcod.white)
	libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, max_mana)
	libtcod.console_set_default_foreground(window, libtcod.light_green)
	libtcod.console_print_ex(window, len(max_mana), y, libtcod.BKGND_NONE, libtcod.LEFT, max_mp_bonus)
	y += 2

	libtcod.console_set_default_foreground(window, libtcod.white)
	libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, power)
	libtcod.console_set_default_foreground(window, libtcod.light_green)
	libtcod.console_print_ex(window, len(power), y, libtcod.BKGND_NONE, libtcod.LEFT, power_bonus)
	y += 1
	libtcod.console_set_default_foreground(window, libtcod.white)
	libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, defense)
	libtcod.console_set_default_foreground(window, libtcod.light_green)
	libtcod.console_print_ex(window, len(defense), y, libtcod.BKGND_NONE, libtcod.LEFT, defense_bonus)
	y += 1
	libtcod.console_set_default_foreground(window, libtcod.white)
	libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, armor)
	libtcod.console_set_default_foreground(window, libtcod.light_green)
	libtcod.console_print_ex(window, len(armor), y, libtcod.BKGND_NONE, libtcod.LEFT, armor_bonus)
	y += 1
	libtcod.console_set_default_foreground(window, libtcod.white)
	libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, magic)
	libtcod.console_set_default_foreground(window, libtcod.light_green)
	libtcod.console_print_ex(window, len(magic), y, libtcod.BKGND_NONE, libtcod.LEFT, magic_bonus)
	y += 2

	libtcod.console_set_default_foreground(window, libtcod.white)
	libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, fighting)
	libtcod.console_set_default_foreground(window, libtcod.light_green)
	libtcod.console_print_ex(window, len(fighting), y, libtcod.BKGND_NONE, libtcod.LEFT, fighting_bonus)
	y += 1
	libtcod.console_set_default_foreground(window, libtcod.white)	
	libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, shielding)
	libtcod.console_set_default_foreground(window, libtcod.light_green)
	libtcod.console_print_ex(window, len(shielding), y, libtcod.BKGND_NONE, libtcod.LEFT, shielding_bonus)
	y += 1
	libtcod.console_set_default_foreground(window, libtcod.white)	
	libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, conjuring)
	libtcod.console_set_default_foreground(window, libtcod.light_green)
	libtcod.console_print_ex(window, len(conjuring), y, libtcod.BKGND_NONE, libtcod.LEFT, conjuring_bonus)
	y += 1
	libtcod.console_set_default_foreground(window, libtcod.white)	
	libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, archery)
	libtcod.console_set_default_foreground(window, libtcod.light_green)
	libtcod.console_print_ex(window, len(archery), y, libtcod.BKGND_NONE, libtcod.LEFT, archery_bonus)
	y += 1
	libtcod.console_set_default_foreground(window, libtcod.white)	
	libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, transmutations)
	libtcod.console_set_default_foreground(window, libtcod.light_green)
	libtcod.console_print_ex(window, len(transmutations), y, libtcod.BKGND_NONE, libtcod.LEFT, transmutations_bonus)
	y += 1
	libtcod.console_set_default_foreground(window, libtcod.white)	
	libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, hexes)
	libtcod.console_set_default_foreground(window, libtcod.light_green)
	libtcod.console_print_ex(window, len(transmutations), y, libtcod.BKGND_NONE, libtcod.LEFT, hexes_bonus)
	y += 2

	#libtcod.console_print_rect_ex(window, 0, y, text_width, text_height, libtcod.BKGND_NONE, libtcod.LEFT, status)


	x = SCREEN_WIDTH/2 - text_width/2
	y = SCREEN_HEIGHT/2 - text_height/2
	libtcod.console_blit(window, 0, 0, text_width, text_height, 0, x, y, 1.0, 0.7)

	recomp = True
	while True:
		if recomp == True:
			menu_check = True
		libtcod.console_flush()
		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

		if (mouse.lbutton_pressed):
			return
				

		if mouse.rbutton_pressed or key.vk == libtcod.KEY_ESCAPE:
			if recomp == True:
				menu_recompute = True
			return None
			

		if key.vk == libtcod.KEY_ENTER and key.lalt:
			libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

		index = key.c - ord('a')
		if index >= 0 and index < 26: 
			if recomp == True:
				menu_recompute = True
			return 

	#msgbox('Character information\n\nLevel: ' + str(player.level) + '\nCurrent XP: ' + 
	#		str(player.fighter.xp) + '\nNext level at: ' + str(level_up_xp) + '\n\nMax HP: '
	#		 + str(player.fighter.max_hp) + '\nMax MP: ' + str(player.fighter.max_mana) + '\n\nPower: ' + str(player.fighter.power) + '\nDefense: ' + 
	#		 str(player.fighter.defense) + '\nAC: ' + str(player.fighter.armor) + '\nMagic: ' + str(player.fighter.magic) + '\n\nFighting: ' + 
	#		 str(player.fighter.fighting) + '\nShielding: ' + str(player.fighter.shielding) + '\nConjuring: ' + str(player.fighter.conjuring) + '\nArchery: ' + str(player.fighter.archery) + 
	#		 '\nTransmutations: ' + str(player.fighter.transmutations) + '\nHexes: ' + str(player.fighter.hexes) + '\n\nCombat Bonuses:\n + ' + str(5*player.fighter.fighting) + ' %% Power ' + '\n + ' + str(player.fighter.shielding + player.fighter.defense/2 + player.fighter.fighting/2) + 
	#		 ' %% chance to block ' + '\n + ' + str(3 * player.fighter.shielding) + 
	#		 ' %% AC bonus ' + '\n + ' + str(3*player.fighter.conjuring) + ' %% spell damage' + '\n + ' + str(player.fighter.magic_resist*100) + ' %% magic resistance' + '\n\n' + str(player.fighter.evasion) + ' Evasion'
	#		 + '\n' + str(player.fighter.accuracy) + ' Accuracy' + '\n' + str(player.fighter.speed) + ' Speed', CHARACTER_SCREEN_WIDTH)

def closest_monster(max_range):
	closest_enemy = None
	closest_dist = max_range + 1

	for object in objects:
		if object.fighter and not object == player and libtcod.map_is_in_fov(fov_map, object.x, object.y):
			dist = player.distance_to(object)
			if dist < closest_dist:
				closest_enemy = object
				closest_dist = dist
	return closest_enemy

def target_tile(max_range=None):
	global key, mouse
	while True:
		
		(x, y) = (mouse.cx, mouse.cy)

		libtcod.console_flush()
		render_all()

		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

		if (mouse.lbutton_pressed and libtcod.map_is_in_fov(fov_map, x, y) and (max_range is None or player.distance(x, y) <= max_range)):
			return (x, y)
		if mouse.rbutton_pressed or key.vk == libtcod.KEY_ESCAPE:
			message('Cancelled', libtcod.yellow)
			return (None, None)

def target_monster(max_range=None):
	while True:
		(x, y) = target_tile(max_range)
		if x is None:
			return None

		for obj in objects:
			if obj.x == x and obj.y == y and obj.fighter and obj != player:
				return obj

def new_game(race, prof):
	global player, inventory, game_msgs, game_state, dungeon_level, spellbook, game_time, debug
	global reveal_map

	game_time = 0
	time_travelers = deque()

	if prof == 'Fighter':
		hp_bonus = 10
		power_bonus = 1
		def_bonus = 2

		mana_bonus = 0
		magic_bonus = 0

		fighting_bonus = 1
		shielding_bonus = 0
		conjuring_bonus = 0
		archery_bonus = 0
		transmutations_bonus = 0
		hexes_bonus = 0

	elif prof == 'Stalker':

		hp_bonus = 5
		power_bonus = 0
		def_bonus = 3
		mana_bonus = 1
		magic_bonus = 0

		fighting_bonus = 0
		shielding_bonus = 0
		conjuring_bonus = 0
		archery_bonus = 2
		transmutations_bonus = 0
		hexes_bonus = 0

	elif prof == 'Conjurer':

		hp_bonus = 2
		power_bonus = 0
		def_bonus = 0

		mana_bonus = 3
		magic_bonus = 2

		fighting_bonus = 0
		shielding_bonus = 0
		conjuring_bonus = 2
		archery_bonus = 0
		transmutations_bonus = 0
		hexes_bonus = 0

	elif prof == 'Alchemist':

		hp_bonus = 5
		power_bonus = 0
		def_bonus = 0
		fighting_bonus = 0
		shielding_bonus = 0
		mana_bonus = 2
		magic_bonus = 1

		shielding_bonus = 0
		fighting_bonus = 0
		conjuring_bonus = 0
		archery_bonus = 0
		transmutations_bonus = 2
		hexes_bonus = 0

	elif prof == 'Hex Mage':

		hp_bonus = 5
		mana_bonus = 3

		power_bonus = 0
		def_bonus = 0
		magic_bonus = 2

		fighting_bonus = 0
		shielding_bonus = 0
		conjuring_bonus = 0
		archery_bonus = 0
		transmutations_bonus = 0
		hexes_bonus = 2


	if race == 'Human':
		fighter_component = Fighter(hp= 20 + hp_bonus, defense= 3 + def_bonus, power= 3 + power_bonus, 
									xp=0, armor=0, mana= 4 + mana_bonus, magic=1 + magic_bonus, 
									death_function=player_death, lifesteal=0, shielding=1+shielding_bonus, 
									fighting=1+fighting_bonus, conjuring=1+conjuring_bonus, 
									archery=1+archery_bonus, transmutations=1+transmutations_bonus, 
									hexes=1+hexes_bonus, speed=100, mana_regen=0.025)
	elif race == 'Dwarf':
		fighter_component = Fighter(hp= 25 + hp_bonus, defense= 2 + def_bonus, power= 3 + power_bonus, 
									xp=0, armor=0, mana= 2 + mana_bonus, magic=0 + magic_bonus,
									death_function=player_death, lifesteal=0, shielding=1+shielding_bonus, 
									fighting=1+fighting_bonus, conjuring=0+conjuring_bonus,
									archery=0+archery_bonus, transmutations=0+transmutations_bonus, 
									hexes=0+hexes_bonus, speed=95, mana_regen=0.02)
	elif race == 'Gnome':		
		fighter_component = Fighter(hp= 15 + hp_bonus, defense= 5 + def_bonus, power= 2 + power_bonus, 
									xp=0, armor=0, mana= 6 + mana_bonus, magic=2 + magic_bonus, 
									death_function=player_death, lifesteal=0, shielding=0+shielding_bonus, 
									fighting=0+fighting_bonus, conjuring=2+conjuring_bonus, 
									archery=0+archery_bonus, transmutations=1+transmutations_bonus, 
									hexes=1+hexes_bonus, speed=100, mana_regen=0.04)
	elif race == 'Green Elf':
		fighter_component = Fighter(hp= 18 + hp_bonus, defense= 8 + def_bonus, power= 2 + power_bonus, 
									xp=0, armor=0, mana= 4 + mana_bonus, magic=1 + magic_bonus, 
									death_function=player_death, lifesteal=0, shielding=0+shielding_bonus, 
									fighting=0+fighting_bonus, conjuring=1+conjuring_bonus, 
									archery=1+archery_bonus, transmutations=2+transmutations_bonus, 
									hexes=2+hexes_bonus, speed=105, mana_regen=0.03)

	fighter_component.stealthiness = 1
	if race == 'Green Elf':
		fighter_component.stealthiness += 1

	player = Object(0, 0, player_tile, 'player', libtcod.white, blocks=True, fighter=fighter_component, race=race, prof=prof)
	player.level = 1

	inventory = []
	game_msgs = []
	spellbook = []

	debug = False
	reveal_map = False

	# testing

	append_spell('White Light')

	dungeon_level = 1
	make_map()
	initialize_fov()
	game_state = 'playing'
	

	if prof == 'Conjurer':

		append_spell('Magic Dart')

		item_component1 = Item(use_function=cast_heal)
		item1 = Object(0, 0, healthpot_tile, 'healing potion', libtcod.white, item=item_component1)
		item_component2 = Item(use_function=cast_restore_mana)
		item2 = Object(0, 0, manapot_tile, 'mana potion', libtcod.white, item=item_component2)
		
		inventory.append(item1)
		inventory.append(item2)

	elif prof == 'Fighter':
		
		item_component = Item(use_function=cast_heal)
		item = Object(0, 0, healthpot_tile, 'healing potion', libtcod.violet, item=item_component)

		inventory.append(item)

		item_component = Item(material=True)
		item = Object(0, 0, 'e', 'albite', libtcod.white, item=item_component)

		inventory.append(item)
		inventory.append(item)
	
	elif prof == 'Stalker':

		item_component = Item(use_function=cast_heal)
		item = Object(0, 0, healthpot_tile, 'healing potion', libtcod.violet, item=item_component)
		equipment_component = Equipment(slot='ranged weapon', power_bonus=1)
		item2 = Object(0, 0, 'R', 'short bow', libtcod.dark_sepia, equipment=equipment_component)
		inventory.append(item)
		inventory.append(item2)
		item2.item.use()	
	
	elif prof == 'Alchemist':
		
		#add starting items
		item_component1 = Item(use_function=cast_heal)
		item1 = Object(0, 0, healthpot_tile, 'healing potion', libtcod.white, item=item_component1)
		item_component2 = Item(use_function=cast_restore_mana)
		item2 = Object(0, 0, manapot_tile, 'mana potion', libtcod.white, item=item_component2)
		inventory.append(item1)
		inventory.append(item2)
		#add starting spells
		append_spell('Beastly Talons')
		
	elif prof == 'Hex Mage':

		item_component1 = Item(use_function=cast_heal)
		item1 = Object(0, 0, healthpot_tile, 'healing potion', libtcod.white, item=item_component1)
		item_component2 = Item(use_function=cast_restore_mana)
		item2 = Object(0, 0, manapot_tile, 'mana potion', libtcod.white, item=item_component2)

		inventory.append(item1)
		inventory.append(item2)
		#add starting spells
		append_spell('Hibernation')

	if player.race == 'Human':
		racial_text = 'You are a quick learner and start with +1 to all aptitudes and gain a 33 %% experience bonus.'
	elif player.race == 'Dwarf':
		racial_text = 'The dwarven fighting spirit allows you to restore a small portion of your health upon slaying foes.'
	elif player.race == 'Gnome':
		racial_text = 'Your gnomish grit allows you to restore 1 MP upon slaying foes.'
	elif player.race == 'Green Elf':
		racial_text = 'Your formidable vision allows you to see far into the distance. You start with the skill Stealth.'
		#add racial skill
		append_spell('Stealth')

	if inventory:
		items = ''
		for i in inventory:
			if items == '': 
				items += str(i.name)
				continue
			if str(i.name)[0] in 'aeiouAEIOU':
				pref = ', an '
			else:
				pref = ', a '
			items += pref + str(i.name)

	player.fighter.hp = player.fighter.max_hp
	player.fighter.mana = player.fighter.max_mana

	libtcod.console_flush()
	render_all()

	msgbox('You are a ' + str(player.race) + '.' + racial_text + ' Your inventory contains a ' + items + '. \n\nPress any letter to continue.')

def initialize_fov():
	global fov_recompute, fov_map
	fov_recompute = True

	fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			libtcod.map_set_properties(fov_map, x, y, not tilemap[x][y].block_sight, not tilemap[x][y].blocked)

	libtcod.console_clear(con)

def play_game():
	global key, mouse, game_time, menu_recompute, menu_check
	menu_check = False
	menu_recompute = False
	player_action = None

	while not libtcod.console_is_window_closed():

		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

		render_all()
	
		libtcod.console_flush()

		check_level_up()

		for obj in objects:
			if obj.fighter:
				obj.fighter.check_buffs()
			if obj.trap:
				obj.trap.check_traps()
			if obj.fighter:
				if obj.fighter.hp > obj.fighter.max_hp:
					obj.fighter.hp = obj.fighter.max_hp
				if obj.fighter.mana > obj.fighter.max_mana:
					obj.fighter.mana = obj.fighter.max_mana
			obj.clear()

		(x, y) = (mouse.cx, mouse.cy)

		if (0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT):
			if (mouse.lbutton_pressed):
				if not tilemap[x][y].blocked and tilemap[x][y].explored:
					done = False
					while not done:
						done = auto_walk(x, y)

				
		if mouse.rbutton_pressed or key.vk == libtcod.KEY_ESCAPE:
			message('Cancelled', libtcod.yellow)
			return (None, None)
		
		if menu_recompute == False and player.fighter.stunned == 0:
			player_action = handle_keys()
			if player_action == 'exit':
				# very outdated not working save func: save_game()
				break

		if menu_recompute == True:
			menu_check = False
			menu_recompute = False

		# if player took turn
		if game_state == 'playing' and player_action != 'didnt-take-turn' and player.fighter.stunned == 0:
			for obj in objects:
				if obj.fighter:						
					obj.fighter.apply_buff_effects()
				# obj.fighter can die from buff effects, turning obj.fighter into NoneType object
				# thus need to check again before applying (mana) regen
				if obj.fighter:
					obj.fighter.regenerate_tick()
			for obj in objects:
				if obj.ai and obj.timeobj:
					obj.timeobj.tick()
			game_time += 1

		elif player.fighter.stunned > 0 and game_state == 'playing':
			time.sleep(.250)
			for obj in objects:
				if obj.fighter:						
					obj.fighter.apply_buff_effects()
				if obj.fighter:
					obj.fighter.regenerate_tick()
				if obj.ai and obj.timeobj:
					obj.timeobj.tick()
			game_time += 1
			player.fighter.stunned -= 1
		
def main_menu():
	img = libtcod.image_load('menu_background1.png')

	while not libtcod.console_is_window_closed():
		libtcod.image_blit_2x(img, 0, 0, 0)

		libtcod.console_set_default_foreground(0, libtcod.light_yellow)
		libtcod.console_print_ex(0, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-4, libtcod.BKGND_NONE, libtcod.CENTER, 'TOMBS OF THE ANCIENT KINGS')
		libtcod.console_print_ex(0, SCREEN_WIDTH/2, SCREEN_HEIGHT-2, libtcod.BKGND_NONE, libtcod.CENTER, 'By Arvid')

		choice = menu('', ['New Game', 'Continue', 'Quit'], 24)

		if choice == 0:
			race_menu()

		if choice == 1:
			try:
				load_game()
			except:
				msgbox('\n No saved game to load.\n', 24)
				continue
			play_game()

		elif choice == 2:
			break

def race_menu():

	race_list = ['Human', 'Dwarf', 'Gnome', 'Green Elf']
	class_list = ['Fighter', 'Stalker', 'Conjurer', 'Alchemist', 'Hex Mage']

	choice = None
	choice2 = None

	while choice == None:

		choice = transp_menu('Choose a race!', race_list, 24, 1)

		if choice is not None:

		#elif choice == 4:

			while choice2 == None:

				choice2 = transp_menu('Choose a profession!', class_list, 70, 1)

				if choice2 is not None:

					new_game(str(race_list[choice]), str(class_list[choice2]))
					play_game()

	#if choice == 4:

def save_game():
	file = shelve.open('savegame', 'n')
	file['map'] = tilemap
	file['objects'] = objects
	file['player_index'] = objects.index(player)
	file['inventory'] = inventory
	file['game_msgs'] = game_msgs
	file['game_state'] = game_state
	file['stairs_index'] = objects.index(stairs)
	file['dungeon_level'] = dungeon_level
	file.close()

def load_game():
	global tilemap, objects, inventory, game_msgs, game_state, stairs, dungeon_level

	file = shelve.open('savegame', 'r')
	tilemap = file['map']
	objects = file['objects']
	player = objects[file['player_index']]
	inventory = file['inventory']
	game_msgs = file['game_msgs']
	game_state = file['game_state']
	stairs = objects[file['stairs_index']]
	dungeon_level = file['dungeon_level']
	file.close()

	initialize_fov()

def msgbox(text, width=50):
	menu(text, [], width)

def transp_msgbox(text, width=50, transp=1):
	transp_menu(text, [], width, transp)

def COLCTRL(c1=libtcod.gold, c2=libtcod.light_gray, c3=libtcod.green, c4=libtcod.yellow, c5=libtcod.orange):

	libtcod.console_set_color_control(libtcod.COLCTRL_1, c1, libtcod.black)
	libtcod.console_set_color_control(libtcod.COLCTRL_2, c2, libtcod.black)
	libtcod.console_set_color_control(libtcod.COLCTRL_3, c3, libtcod.black)
	libtcod.console_set_color_control(libtcod.COLCTRL_4, c4, libtcod.black)
	libtcod.console_set_color_control(libtcod.COLCTRL_5, c5, libtcod.black)

def next_level():
	global dungeon_level, time_travelers
	message('You take a moment to rest and recover your strength.', libtcod.violet)
	player.fighter.heal(player.fighter.max_hp/2)
	player.fighter.restore_mana(player.fighter.max_mana/2)
	message('You descend deeper into the heart of the dungeon...', libtcod.red)
	dungeon_level +=1
	#if dungeon_level < 5:

	# clear previous level from acting entities
	time_travelers = deque()

	make_map()
	initialize_fov()
	render_all()
	libtcod.console_flush()
	for buff in player.fighter.buff:
		if buff.name == 'Divination of Warmth cd':
			player.fighter.buff.remove(buff)
	for obj in objects:
		if obj.name == 'Svublo, the fat orc':
			msgbox('You hear a distant noise of an orc growling. \nBut this sound couldnt possibly be from any ordinary orc...\n\nPress any letter to continue.', 50)
			break
		if obj.name == 'Malignant spirit':
			msgbox('You feel the presence of something evil...Be on your guard!\n\nPress any letter to continue.', 30)
			break
	#else:
	#	make_bsp()
	#	initialize_fov()
	#if dungeon_level == 5:
	#	msgbox('Entering the caves...', 20)

def check_level_up():

	level_up_xp = LEVEL_UP_BASE + player.level * LEVEL_UP_FACTOR
	if player.fighter.xp >= level_up_xp:
		player.level += 1
		player.fighter.xp -= level_up_xp
		message('You have advanced to level ' + str(player.level) + '!', libtcod.yellow)
		libtcod.console_flush()
		render_all()
		race_lvlup(player)
		class_lvlup()

		choice = None
		while choice == None:
			choice = menu('Choose an aptitude to raise:\n',
			['+Fighting',
			'+Shielding', 
			'+Conjuring',
			'+Archery',
			'+Transmutations',
			'+Hexes'], LEVEL_SCREEN_WIDTH)
		if choice == 0:
			player.fighter.base_fighting += 1
			
		elif choice == 1:
			player.fighter.base_shielding += 1

		elif choice == 2:
			player.fighter.base_conjuring += 1 

		elif choice == 3:
			player.fighter.base_archery += 1

		elif choice == 4:
			player.fighter.base_transmutations += 1

		elif choice == 5:
			player.fighter.base_hexes += 1

def random_choice_index(chances):

	dice = libtcod.random_get_int(0, 1, sum(chances))

	running_sum = 0
	choice = 0
	for w in chances:
		running_sum += w

		if dice <= running_sum:
			return choice
		choice += 1

def random_choice(chances_dict):
	chances = chances_dict.values()
	strings = chances_dict.keys()
	return strings[random_choice_index(chances)]

def from_dungeon_level(table):
	for (value, level) in reversed(table):
		if dungeon_level >= level:
			return value
	return 0

def get_equipped_in_slot(slot):
	for obj in inventory:
		if obj.equipment and obj.equipment.slot == slot and obj.equipment.is_equipped:
			return obj.equipment
	return None

def get_all_equipped(obj):
	if obj == player:
		equipped_list = []
		for item in inventory:
			if item.equipment and item.equipment.is_equipped:
				equipped_list.append(item.equipment)
		return equipped_list
	else:
		return []

def get_all_buffs(obj):
	buffed_list = []
	for buff in obj.fighter.buff:
		buffed_list.append(buff)
	return buffed_list

def debug_stats_menu(header):
	options = ['experience', 'power', 'defense', 'AC', 'magic', 'fighting', 'shielding',
				'conjuring', 'archery', 'transmutations', 'hexes', 'evasion', 'accuracy', 
				'speed']
	index = menu(header, options, DEBUG_WIDTH)

	if index is None: return None

	width = 40

	if options[index] == 'experience':
		player.fighter.xp += gain_menu('Gain what amount?', ['10', '100', '1000'], width)
	elif options[index] == 'power':
		player.fighter.base_power += gain_menu('Gain what amount?', ['1', '5', '25'], width)
	elif options[index] == 'defense':
		player.fighter.base_defense += gain_menu('Gain what amount?', ['1', '5', '25'], width)
	elif options[index] == 'AC':
		player.fighter.base_armor += gain_menu('Gain what amount?', ['1', '5', '25'], width)
	elif options[index] == 'magic':
		player.fighter.base_magic += gain_menu('Gain what amount?', ['1', '5', '25'], width)
	elif options[index] == 'fighting':
		player.fighter.base_fighting += gain_menu('Gain what amount?', ['1', '5', '25'], width)
	elif options[index] == 'shielding':
		player.fighter.base_shielding += gain_menu('Gain what amount?', ['1', '5', '25'], width)
	elif options[index] == 'conjuring':
		player.fighter.base_conjuring += gain_menu('Gain what amount?', ['1', '5', '25'], width)
	elif options[index] == 'archery':
		player.fighter.base_archery += gain_menu('Gain what amount?', ['1', '5', '25'], width)
	elif options[index] == 'transmutations':
		player.fighter.base_transmutations += gain_menu('Gain what amount?', ['1', '5', '25'], width)
	elif options[index] == 'hexes':
		player.fighter.base_hexes += gain_menu('Gain what amount?', ['1', '5', '25'], width)
	elif options[index] == 'evasion':
		player.fighter.base_evasion += gain_menu('Gain what amount?', ['1', '5', '25'], width)
	elif options[index] == 'accuracy':
		player.fighter.base_accuracy += gain_menu('Gain what amount?', ['1', '5', '25'], width)
	elif options[index] == 'speed':
		player.fighter.base_speed += gain_menu('Gain what amount?', ['1', '5', '25'], width)


def gain_menu(header, options, width):
	index = menu(header, options, width)
	if index is None: return 0
	return int(options[index])

def spell_menu(header):
	#show a menu with each spell as an option
	if len(spellbook) == 0:
		options = ['Your spellbook is empty.']
	else:
		options = []
	for spell in spellbook:
		if spell.school is not None:
			text = spell.name + '    Mana: ' + str(spell.cost) + '        ' + spell.school 
		else:
			text = spell.name + '    Mana: ' + str(spell.cost) + '        ' 


		options.append(text)

	index = menu(header, options, SPELLBOOK_WIDTH)

	#if a spell was chosen, cast it
	if index is None or len(spellbook) == 0: return None
	return spellbook[index]

def race_lvlup(obj):
	if obj == player:
		if player.race == 'Human':
			player.fighter.base_max_hp += 4
			player.fighter.hp += 4
			player.fighter.base_max_mana += 1
			player.fighter.mana += 1
			player.fighter.magic_resist += 0.01
		if player.race == 'Dwarf':
			player.fighter.base_max_hp += 5
			player.fighter.hp += 5
			player.fighter.base_max_mana += 1
			player.fighter.mana += 1
		if player.race == 'Gnome':
			player.fighter.base_max_hp += 2
			player.fighter.hp += 2
			player.fighter.base_max_mana += 3
			player.fighter.mana += 3
		if player.race == 'Green Elf':
			player.fighter.base_max_hp += 3
			player.fighter.hp += 3
			player.fighter.base_max_mana += 2
			player.fighter.mana += 1

def class_lvlup():
	if player.prof == 'Fighter':
		if player.level == 5:
			append_spell('Shield Block')
	elif player.prof == 'Stalker':
		if player.level == 5:
			append_spell('Freezing Trap')
		if player.level == 8:
			append_spell('Explosive Trap')
	elif player.prof == 'Conjurer':
		if player.level == 3:
			append_spell('Bolt of Ice')
		if player.level == 6:
			append_spell('Chain Lightning')
	elif player.prof == 'Alchemist':
		if player.level == 4:
			append_spell('Bear Form')
		elif player.level == 6:
			append_spell('Felid Form')

def find_spell(name):
	global spellbook
	for spell in spellbook:
		if spell.name == name:
			return spell

def took_turn():
	global game_time, fov_recompute

	fov_recompute = True

	render_all()
	
	libtcod.console_flush()

	check_level_up()

	for obj in objects:
		if obj.fighter:
			obj.fighter.check_buffs()
		if obj.trap:
			obj.trap.check_traps()

	for obj in objects:
		if obj.fighter:
			if obj.fighter.hp > obj.fighter.max_hp:
				obj.fighter.hp = obj.fighter.max_hp
			if obj.fighter.mana > obj.fighter.max_mana:
				obj.fighter.mana = obj.fighter.max_mana

	for obj in objects:
		obj.clear()

	for obj in objects:
		if obj.ai and obj.timeobj:
			obj.timeobj.tick()

		if obj.fighter:
			obj.fighter.apply_buff_effects()

	game_time += 1

def load_customfont():
	a = 256

	for y in range(5, 6):
		libtcod.console_map_ascii_codes_to_font(a, 32, 0, y)
		a += 32

def check_objects(x, y):
	for obj in objects:
		if obj.x == x and obj.y == y:
			return True
	return False

def auto_walk(dest_x, dest_y):

	fov = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)

	#set sight and walkable tiles to same as original map
	for y1 in range(MAP_HEIGHT):
		for x1 in range(MAP_WIDTH):
			libtcod.map_set_properties(fov, x1, y1, not tilemap[x1][y1].block_sight, not tilemap[x1][y1].blocked)

	#set blocking objects to not block tiles from being walkable
	for obj in objects:
		if obj.blocks and obj != player:
			libtcod.map_set_properties(fov, obj.x, obj.y, True, True)

	my_path = libtcod.path_new_using_map(fov, 1)
	libtcod.path_compute(my_path, player.x, player.y, dest_x, dest_y)
	if not libtcod.path_is_empty(my_path):
		x, y = libtcod.path_walk(my_path, True)
		old_x = player.x
		old_y = player.y
		if x or y:
			#set player coordinates to the next path tile
			player.x = x
			player.y = y
	else:
		message('Don\'t know how to get there.', libtcod.light_gray)
		libtcod.path_delete(my_path)
		return True
		
	libtcod.path_delete(my_path)
	if player.race == 'Green Elf':
		torch = 12
	else:
		torch = 8
	libtcod.map_compute_fov(fov_map, player.x, player.y, torch, FOV_LIGHT_WALLS, FOV_ALGO)
	for obj in objects:
		if libtcod.map_is_in_fov(fov_map, obj.x, obj.y):
			if obj.item and not tilemap[obj.x][obj.y].explored:
				if obj.name[0] in 'aeiou':
					pref = 'an '
				else:
					pref = 'a '
				message('Found ' + pref + obj.name + '.', libtcod.light_gray)
				took_turn()
				return True
	took_turn()
	if player.x == dest_x and player.y == dest_y: 
		return True
	if monster_in_view(): 
		return True
	return False

def auto_explore():
	global fov_map

	#make new map with same dimensions
	fov = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
	found_item = False

	#break if monster comes into view
	while not monster_in_view() and not found_item:

		smallest_path = None
		min_size = 175

		#set sight and walkable tiles to same as original map
		for y1 in range(MAP_HEIGHT):
			for x1 in range(MAP_WIDTH):
				libtcod.map_set_properties(fov, x1, y1, not tilemap[x1][y1].block_sight, not tilemap[x1][y1].blocked)

		#set blocking objects to not block tiles from being walkable
		for obj in objects:
			if obj.blocks and obj != player:
				libtcod.map_set_properties(fov, obj.x, obj.y, True, True)

		#add unexplored tiles to targets
		for x in range(MAP_WIDTH):
			for y in range(MAP_HEIGHT):

				visible = libtcod.map_is_in_fov(fov_map, x, y)
				explored = tilemap[x][y].explored
				wall = tilemap[x][y].block_sight

				#tiles that are not visible or explored
				if not visible and not explored and not wall:

					#make new path with diagonal movement cost 1
					my_path = libtcod.path_new_using_map(fov, 1)

					#compute path to (x, y)
					libtcod.path_compute(my_path, player.x, player.y, x, y)

					#if path exists and is smaller than min_size, delete earlier smallest path and replace it					
					if not libtcod.path_is_empty(my_path):
						if libtcod.path_size(my_path) < min_size:
							min_size = libtcod.path_size(my_path)
							if smallest_path:
								libtcod.path_delete(smallest_path)
							smallest_path = my_path
						else:
							libtcod.path_delete(my_path)

		#if path exists, walk it
		if smallest_path:

			#find the next coordinates in the computed full path	
			x, y = libtcod.path_walk(smallest_path, True)

			old_x = player.x
			old_y = player.y
			
			if x or y:
				#set player coordinates to the next path tile
				player.x = x
				player.y = y
				# search for new items at location
			else:
				libtcod.path_delete(smallest_path)
				break

			#delete path
			libtcod.path_delete(smallest_path)

		
		else:
			#path doesnt exist
			message('Nothing left to explore.')
			break

		#player is stuck
		if old_x == player.x and old_y == player.y:
			if smallest_path:
				libtcod.path_delete(smallest_path)
			break

		if player.race == 'Green Elf':
			torch = 12
		else:
			torch = 8
		libtcod.map_compute_fov(fov_map, player.x, player.y, torch, FOV_LIGHT_WALLS, FOV_ALGO)
		for obj in objects:
			if libtcod.map_is_in_fov(fov_map, obj.x, obj.y):
				if obj.item and not tilemap[obj.x][obj.y].explored:
					if obj.name[0] in 'aeiou':
						pref = 'an '
					else:
						pref = 'a '
					message('Found ' + pref + obj.name + '.', libtcod.light_gray)
					found_item = True
					break
		#player took turn
		took_turn()

def monster_in_view():
	for obj in objects:
		if obj.fighter and libtcod.map_is_in_fov(fov_map, obj.x, obj.y) and obj != player:
			message('A ' + str(obj.name) + ' appears!', libtcod.light_gray)
			return True
	return False
	
#---POTION FUNCTIONS---#

def cast_heal():
	if player.fighter.hp == player.fighter.max_hp:
		message('You are already at full health.', libtcod.red)
		return 'cancelled'
	else:
		amount = player.level * 2 + int(round((player.fighter.max_hp/4))) + 15
		message('You feel a surge of energy pass through your body as your wounds magically start to seal...', libtcod.violet) 
		player.fighter.heal(amount)
	
		for object in objects:
			object.clear()

		for object in objects:
			if object.ai:
				object.ai.take_turn()

def cast_restore_mana():
	if player.fighter.mana == player.fighter.max_mana:
		message('You are already at full mana.', libtcod.red)
		return 'cancelled'
	else:
		amount = int(round(player.fighter.max_mana/2)) + 5 + player.level * 2
		message('You feel your magical power return!', libtcod.violet) 
		player.fighter.restore_mana(amount)
	
		for object in objects:
			object.clear()

		for object in objects:
			if object.ai:
				object.ai.take_turn()

def cast_berserk():
	global game_time
	message('Rage and madness cosumes you!! You gain +3 PWR.', libtcod.red)
	dur = game_time + 20
	buff = Buff('Berserk', power_bonus=3, end_time=dur)
	player.fighter.buff.append(buff)

def cast_magic_buff():
	global game_time
	for buff in player.fighter.buff:
		if buff.name == 'Potion of magic':
			message('You are already affected by potion of magic!', libtcod.red)
			return
	dur = 120 + libtcod.random_get_int(0, 1, 60) + game_time
	buff = Buff('Potion of magic', magic_bonus=3, conjuring_bonus=3, end_time=dur)
	player.fighter.buff.append(buff)
	message('Your spellcasting is augmented! Gaining +3 Magic, +3 Conjuring.', libtcod.light_violet)

#---SCROLL FUNCTIONS---#

def cast_lightning():
	monster = closest_monster(LIGHTNING_RANGE)
	if monster is None:
		message('No enemies are close enough to strike!', libtcod.red)
		return 'cancelled'
	resist_chance = libtcod.random_get_int(0, 0, 100)
	if resist_chance + player.fighter.conjuring > monster.fighter.magic_resist*100 + 5: 
		damage = int(round((libtcod.random_get_int(0, 14, 22) + 0.6*player.fighter.magic + 0.6*player.fighter.conjuring)*(1-monster.fighter.magic_resist)))
	
		message('Your lightning bolt hits ' + monster.name + ' with a loud bang! It deals ' + str(damage) + 
			' points of damage.', libtcod.light_violet)
		monster.fighter.take_damage(damage)
	else:
		message('You let loose a bolt of lightning towards the ' + monster.name + ', but it resists the attack completely!', libtcod.red)

	took_turn()

def cast_confuse():
	message('Left-click and enemy to confuse it, or right-click to cancel.', libtcod.light_cyan)
	monster = target_monster(CONFUSE_RANGE)
	if monster is None: return 'cancelled'
	
	resist_chance = libtcod.random_get_int(0, 0, 100)
	if resist_chance + player.fighter.conjuring > monster.fighter.magic_resist*100 + 5:

		old_ai = monster.ai
		monster.ai = ConfusedMonster(old_ai)
		monster.ai.owner = monster
		message('The eyes of the ' + monster.name + ' goes blank as it starts to stumble around!', libtcod.light_blue)
	else:
		message('You attempt to confuse ' + monster.name + ', but it has no effect!', libtcod.red)

	took_turn()

def cast_fireball():
	message('Left-click a target tile or right-click to cancel.', libtcod.light_cyan)
	(x, y) = target_tile()
	if x is None: return 'cancelled'

	message('The fireball explodes, burning everything within' + str(FIREBALL_RADIUS) + ' tiles!', libtcod.light_blue)
	for obj in objects:
		if obj.distance(x, y) <= FIREBALL_RADIUS and obj.fighter:
			resist_chance = libtcod.random_get_int(0, 0, 100)
			if resist_chance + player.fighter.conjuring > obj.fighter.magic_resist*100 + 5:
				damage = int(round((libtcod.random_get_int(0, 15, 21) + player.fighter.magic*0.5 + player.fighter.conjuring*0.4)*(1 - obj.fighter.magic_resist)))
				message('The ' + obj.name + ' burns for ' + str(damage) + ' hit points.', libtcod.light_blue)
				obj.fighter.take_damage(damage)
			else:
				message('The ' + obj.name + ' completely resists the fireball!', libtcod.red)
	took_turn() 

def gain_skill():
	choice = None
	while choice == None:
		choice = menu('Choose an aptitude to raise:\n',
		['+Fighting',
		'+Shielding', 
		'+Conjuring',
		'+Archery',
		'+Transmutations',
		'+Hexes'], LEVEL_SCREEN_WIDTH)
	if choice == 0:
		player.fighter.base_fighting += 1
	elif choice == 1:
		player.fighter.base_shielding += 1
	elif choice == 2:
		player.fighter.base_conjuring += 1 
	elif choice == 3:
		player.fighter.base_archery += 1
	elif choice == 4:
		player.fighter.base_transmutations += 1
	elif choice == 5:
		player.fighter.base_hexes += 1

#---SPELL FUNCTIONS---#

# Conjurations

def cast_magic_dart():

	message('Left-click a target, or right-click to cancel.', libtcod.light_cyan)
	monster = target_monster(MAGIC_DART_RANGE)

	if monster is None: 
		return 'cancelled'

	apt_bonus = 1 + 0.03*player.fighter.conjuring
	resist_chance = libtcod.random_get_int(0, 0, 100)
	if resist_chance + player.fighter.conjuring > monster.fighter.magic_resist*100 + 5:

		damage = int(round(((libtcod.random_get_int(0, 2, 6) + player.fighter.magic * 0.81) * apt_bonus * (1 - monster.fighter.magic_resist))))
			
		message('Your magic dart hits ' + monster.name + ' for ' + str(damage) + ' magic damage!', libtcod.light_blue) 
		monster.fighter.take_damage(damage)
	else:
		message('You launch a magic dart towards ' + monster.name + ' but ' + monster.name + ' shrugs it off!', libtcod.red)

def cast_life_tap():
	#Cost: 10 - 1/5*magic but no less than 5
	s = player.fighter.magic / 5 + player.level / 3
	i, d = divmod(s, 1)
	value = int(round(10 - i))
	if value <= 5:
		value = 5

	if player.fighter.hp <= value:
		message('Not enough health!')
		return 'cancelled'
	else:
		player.fighter.hp -= value
		player.fighter.mana += 3
		message('You feel your head tingle as you channel magical powers. Your sanity crumbles...', libtcod.light_cyan)

def cast_ice_barrier():
	global game_time
	
	def_bonus = int(round(player.fighter.magic * 1.17)) + 2 + int(round(player.fighter.conjuring/3))
	arm_bonus = int(round(player.fighter.magic * 0.13)) + 1 + int(round(player.fighter.conjuring/5))
	dur_bonus = int(round(player.fighter.magic * 0.75)) + int(round(player.fighter.conjuring*0.75))
	dur = game_time + 12 + dur_bonus

	message('A magical shield of ice protects you from harm! You gain +' + str(def_bonus) + ' Defense and +' + str(arm_bonus) + ' AC.', libtcod.light_blue)
	buff = Buff('Ice Barrier', defense_bonus=def_bonus, armor_bonus=arm_bonus, end_time=dur)
	player.fighter.buff.append(buff)

def cast_lesser_heal():

	amount = libtcod.random_get_int(0, 2, 4) + int(round((0.54 * player.fighter.magic))) + int(round(player.fighter.conjuring*0.35))
	player.fighter.heal(amount)
	message('You feel your strength return! You gain ' + str(amount) + ' hit points!', libtcod.light_blue)
	
def cast_rain_of_ice():

	message('Clusters of ice strikes all enemies nearby!', libtcod.light_blue)

	for object in objects:

		if object.fighter and not object == player:

			dist = player.distance_to(object)

			if dist <= RAIN_OF_ICE_RADIUS:

				dice = libtcod.random_get_int(0, 0, 20) 

				if dice + player.fighter.magic + player.fighter.conjuring > 100*object.fighter.magic_resist:

					turns = libtcod.random_get_int(0, 1, 2) + int(round(player.fighter.conjuring/5))
					old_ai = object.ai
					object.ai = FrozenMonster(old_ai, object.color, turns)
					object.color = libtcod.sky
					object.ai.owner = object
					message('The ' + str(object.name) + ' is frozen solid!', libtcod.violet)

				resist_chance = libtcod.random_get_int(0, 0, 100)	
				if resist_chance + player.fighter.conjuring > object.fighter.magic_resist*100 + 5:
					apt_bonus = 1 + 0.03*player.fighter.conjuring
					damage = int(round((libtcod.random_get_int(0, 8, 14) + (player.fighter.magic * 1.55))*apt_bonus*(1 - object.fighter.magic_resist)))
					object.fighter.take_damage(damage)
					message('The ' + str(object.name) + ' suffers ' + str(damage) + ' points of damage!', libtcod.light_blue)
				else:
					message('The ' + str(object.name) + ' completely resists!', libtcod.red)

def cast_chain_lightning():
	
	monster = closest_monster(CHAIN_LIGHTNING_RANGE)

	if monster is None:
		message('No enemies are close enough to strike!', libtcod.red)
		return 'cancelled'

	resist_chance = libtcod.random_get_int(0, 0, 100)
	if resist_chance + player.fighter.conjuring > monster.fighter.magic_resist:
		apt_bonus = 1 + 0.03*player.fighter.conjuring
		damage = int(round((libtcod.random_get_int(0, 6, 14) + player.fighter.magic * 1.65)*apt_bonus*(1 - monster.fighter.magic_resist)))
		message('Your chain lightning hits ' + monster.name + ' with a loud bang! It deals ' + str(damage) + 
				' points of damage.', libtcod.light_blue)
		monster.fighter.take_damage(damage)
	else:
		message('The ' + str(monster.name) + ' completely resists!', libtcod.red)
		return
		
	(x, y) = (monster.x, monster.y)
	for obj in objects:
		if obj.distance(x, y) <= CHAIN_LIGHTNING_RADIUS and obj.fighter and obj != player:
			bounce_damage = int(round(damage * (0.55 + 0.02 * player.fighter.conjuring)))
			message('The chain lightning bounces! You hit ' + obj.name + ' for ' + str(bounce_damage) + ' points of damage.', libtcod.light_blue)
			obj.fighter.take_damage(bounce_damage)

def cast_fire_blast():
	
	message('Left-click a target tile or right-click to cancel.', libtcod.light_cyan)
	(x, y) = target_tile()
	if x is None: 
		return 'cancelled'

	message('Your fireblast explodes, burning everything within 2 tiles!!', libtcod.light_blue)

	for obj in objects:
		if obj.distance(x, y) <= FIREBLAST_RADIUS and obj.fighter:
			resist_chance = libtcod.random_get_int(0, 0, 100)
			if resist_chance + player.fighter.conjuring > obj.fighter.magic_resist + 5:
				apt_bonus = 1 + 0.03*player.fighter.conjuring
				damage = int(round((libtcod.random_get_int(0, 12, 21) + player.fighter.magic * 1.75)*apt_bonus*(1-obj.fighter.magic_resist)))

				message('The ' + obj.name + ' burns for ' + str(damage) + ' hit points.', libtcod.light_blue)
				obj.fighter.take_damage(damage)
			else:
				message('The ' + obj.name + ' completely resists!', libtcod.red)

def cast_conjure_food():
	global spellbook

	dice = libtcod.random_get_int(0, 0, 100)
	if dice < 14 - player.fighter.conjuring:
		message('Your fingertips faintly sparks... You conjure up a rotten apple.', libtcod.light_violet)
		if len(inventory) >= 26:
			message('Your inventory is full!', libtcod.red)
			(x, y) = (player.x, player.y)
			item_component = Item(use_function=no_thanks)
			item = Object(x, y, 'a', 'rotten apple', libtcod.darker_green, item=item_component)
			objects.append(item)
		else:
			item_component = Item(use_function=no_thanks)
			item = Object(0, 0, 'a', 'rotten apple', libtcod.darker_green, item=item_component)
			inventory.append(item)
	elif dice < 18:
		message('You conjure up a healing potion! Great!', libtcod.light_violet)
		if len(inventory) >= 26:
			message('Your inventory is full!', libtcod.red)
			(x, y) = (player.x, player.y)
			item_component = Item(use_function=cast_heal)
			item = Object(x, y, '!', 'healing potion', libtcod.violet, item=item_component)
			objects.append(item)
		else:
			item_component = Item(use_function=cast_heal)
			item = Object(0, 0, '!', 'healing potion', libtcod.violet, item=item_component)
			inventory.append(item)

	elif dice < 24 + player.fighter.conjuring:
		message('You conjure up a potion of magic! Fantastic!', libtcod.light_violet)
		if len(inventory) >= 26:
			message('Your inventory is full!', libtcod.red)
			(x, y) = (player.x, player.y)
			item_component = Item(use_function=cast_magic_buff)
			item = Object(x, y, magicpot_tile, 'potion of magic', libtcod.white, item=item_component)
			objects.append(item)
		else:
			item_component = Item(use_function=cast_magic_buff)
			item = Object(0, 0, '!', 'potion of magic', libtcod.blue, item=item_component)
			inventory.append(item)

	elif dice < 46:
		message('You conjure up an apple! Tasty.', libtcod.light_violet)
		if len(inventory) >= 26:
			message('Your inventory is full!', libtcod.red)
			(x, y) = (player.x, player.y)
			item_component = Item(use_function=eat_apple)
			item = Object(x, y, 'a', 'apple', libtcod.green, item=item_component)
			objects.append(item)
		else:
			item_component = Item(use_function=eat_apple)
			item = Object(0, 0, 'a', 'apple', libtcod.green, item=item_component)
			inventory.append(item)
		
	elif dice < 61:
		message('You conjure up a single french fry. ...What?', libtcod.light_violet)
		if len(inventory) >= 26:
			message('Your inventory is full!', libtcod.red)
			(x, y) = (player.x, player.y)
			item_component = Item(use_function=eat_fry)
			item = Object(x, y, 'l', 'french fry', libtcod.dark_yellow, item=item_component)
			objects.append(item)
		else:
			item_component = Item(use_function=eat_fry)
			item = Object(0, 0, 'l', 'french fry', libtcod.dark_yellow, item=item_component)
			inventory.append(item)
	elif dice < 88:
		message('You conjure forth a loaf of bread.', libtcod.light_violet)
		if len(inventory) >= 26:
			message('Your inventory is full!', libtcod.red)
			(x, y) = (player.x, player.y)
			item_component = Item(use_function=eat_bread)
			item = Object(x, y, '!', 'loaf of bread', libtcod.dark_yellow, item=item_component)
			objects.append(item)
		else:
			item_component = Item(use_function=eat_bread)
			item = Object(0, 0, '!', 'loaf of bread', libtcod.dark_yellow, item=item_component)
			inventory.append(item)
	else:
		message('You mumble a few strange words. Nothing appears to happen.', libtcod.light_gray)

def cast_bolt_of_ice():
	global spellbook

	message('Left-click a target, or right-click to cancel.', libtcod.light_cyan)
	monster = target_monster(BOLT_OF_ICE_RANGE)

	if monster is None: 
		return 'cancelled'

	resist_chance = libtcod.random_get_int(0, 0, 100)
	if resist_chance + player.fighter.conjuring > monster.fighter.magic_resist*100 + 5:

		apt_bonus = 1 + 0.03*player.fighter.conjuring

		damage = int(round(((libtcod.random_get_int(0, 4, 7) + player.fighter.magic * 0.96) * apt_bonus * (1 - monster.fighter.magic_resist))))
			
		message('Your bolt of ice hits ' + monster.name + ' for ' + str(damage) + ' magic damage!', libtcod.light_blue)
		monster.fighter.take_damage(damage)
 
		dice = libtcod.random_get_int(0, 0, 100)
		if dice + player.fighter.conjuring + player.fighter.magic > 50:
			turns = libtcod.random_get_int(0, 1, 2)
			old_ai = monster.ai
			monster.ai = FrozenMonster(old_ai, monster.color, turns)
			monster.color = libtcod.sky
			monster.ai.owner = monster
			message('The ' + str(monster.name) + ' is frozen solid!', libtcod.violet)

	else:
		message('The ' + str(monster.name) + ' completely resists!', libtcod.red)

def cast_immolate():
	global spellbook, game_time

	message('Left-click a target, or right-click to cancel.', libtcod.light_cyan)
	monster = target_monster(IMMOLATE_RANGE)

	if monster is None: 
		return 'cancelled'

	for buff in monster.fighter.buff:
		if buff.name == 'Immolate':
			message('Target is already burning!', libtcod.red)
			return 'cancelled'

	resist_chance = libtcod.random_get_int(0, 0, 100)
	if resist_chance + player.fighter.conjuring > monster.fighter.magic_resist*100 + 5:
		apt_bonus = 0.03*player.fighter.conjuring
		dmg = int(round(1 + player.fighter.magic*0.3 + player.fighter.conjuring*0.2))
		dur_bonus = int(round(player.fighter.magic*0.4 + player.fighter.conjuring*0.3))
		dur = libtcod.random_get_int(0, 4, 6) + dur_bonus + game_time
		buff = Buff('Immolate', hp_regen_bonus=-dmg, end_time=dur)
		monster.fighter.buff.append(buff)
		message('You incinerate the ' + str(monster.name) + '!', libtcod.light_blue)
	else:
		message('The ' + str(monster.name) + ' completely resists!', libtcod.red)

def cast_divination_of_warmth():
	global game_time
	for buff in player.fighter.buff:
		if buff.name == 'Divination of Warmth cd':
			message('This ability is still on cooldown!', libtcod.red)
			return 'cancelled'

	dur = game_time + 80000
	buff1 = Buff('Divination of Warmth cd', end_time=dur, displays=False)
	player.fighter.buff.append(buff1)

	dur2 = game_time + 8 + (player.level*0.5 + player.fighter.magic*0.25)
	reg_mod = int(round((player.fighter.max_hp*0.04 + player.fighter.magic*0.15))) + 1
	buff2 = Buff('Divination of Warmth', hp_regen_bonus=reg_mod, end_time=dur2)
	player.fighter.buff.append(buff2)
	message('You feel a surge of heat spread through your body! Your health gradually returns and spells cost -2 MP.', libtcod.light_blue)
 
def cast_white_light():
	global spellbook, game_time
	duration = game_time + int(round(player.level*1.45 + player.fighter.conjuring*2.35 + 4))
	buff = Buff('White Light', magic_resist_bonus=0.55, end_time=duration)
	player.fighter.buff.append(buff)
	message('You begin to emit a blinding light. You gain 55%% magic resistance.' , libtcod.light_blue)

def cast_summon_ice_beast():
	global spellbook, game_time
	duration = int(round(game_time + player.level*3.25 + player.fighter.conjuring*8.25 + 16))
	pass
# Transmutations

def cast_beastly_talons():
	global game_time, spellbook

	if player.fighter.is_transformed():
		
		transm_list = []
		
		for buff in player.fighter.buff:
			if buff.transm == True:
				transm_list.append(buff.name)
				player.fighter.buff.remove(buff)

	dur_bonus = int(round(player.fighter.magic * 1.15)) + int(round(player.fighter.transmutations * 2.5))
	pwr_mod = int(round(0.5 + 0.24*player.fighter.transmutations))
	dur = game_time + 3000 + dur_bonus

	message('Talons start to grow out from your feet! You gain ' + str(pwr_mod) + ' power and have a chance to perform auxiliary attacks in close combat!', libtcod.light_blue)
	buff = Buff('Beastly Talons', power_bonus=pwr_mod, transm=True, end_time=dur)
	player.fighter.buff.append(buff)

def cast_unholy_rage():
	global game_time, spellbook

	dur_bonus = int(round(player.fighter.magic * 1)) + int(round(player.fighter.transmutations/2))
	steal_bonus = int(round(player.fighter.magic * 0.17)) + 3 + int(round(player.fighter.transmutations/5))
	dur = game_time + 12 + dur_bonus

	message('You enter an unholy rage, gaining ' + str(steal_bonus) + ' hit points with each strike!', libtcod.light_blue)
	buff = Buff('Unholy Rage', lifesteal_bonus=steal_bonus, end_time=dur)
	player.fighter.buff.append(buff)
	
def cast_felid_form():
	global game_time, spellbook

	if player.fighter.is_transformed():

		transm_list = []
		
		for buff in player.fighter.buff:
			if buff.transm == True:
				transm_list.append(buff.name)
				player.fighter.buff.remove(buff)

		message('Removed ' + str(', '.join(transm_list)), libtcod.red)


	dur_bonus = int(round(player.fighter.magic * 1.15)) + int(round(player.fighter.transmutations * 2.5))
	dur = game_time + dur_bonus + 6000

	message('You transform in to a felid! You gain sharp claws and teeth and feel more agile!', libtcod.light_blue)
	hp_red = int(round(player.fighter.max_hp/6)) - player.fighter.transmutations
	def_bonus = int(round(player.fighter.transmutations*1.2))

	buff = Buff('Felid Form', defense_bonus=7 + def_bonus, max_hp_bonus=-hp_red, conjuring_bonus=-3, fighting_bonus=3, transm=True, end_time=dur)
	player.fighter.buff.append(buff)

	message('You gain ' + str(buff.defense_bonus) + ' Defense, ' + str(hp_red) + ' Max HP, ' + str(buff.conjuring_bonus) + ' Conjuring, ' + str(buff.fighting_bonus) + ' Fighting.', libtcod.light_blue)

def cast_bear_form():
	global game_time, spellbook

	if player.fighter.is_transformed():

		transm_list = []
		
		for buff in player.fighter.buff:
			if buff.transm == True:
				transm_list.append(buff.name)
				player.fighter.buff.remove(buff)

	message('Removed ' + str(', '.join(transm_list)), libtcod.red)

	dur_bonus = int(round(player.fighter.magic * 1.15)) + int(round(player.fighter.transmutations * 2.5))
	dur = game_time + dur_bonus + 3000

	message('You transform in to a bear! You gain thick hide and become much stronger!', libtcod.light_blue)
	hp_mod = int(round(player.fighter.max_hp * 0.25 + player.fighter.transmutations * 1.35))
	def_mod = -5 + int(round(player.fighter.transmutations * 1.26))
	pwr_mod = 1 + int(round(player.fighter.transmutations * 0.55))
	ac_mod = 1 + int(round(player.fighter.transmutations * 0.38))
	fighting_mod = +1
	shielding_mod = -1
	conjuring_mod = -4

	buff = Buff('Bear Form', power_bonus=pwr_mod, defense_bonus=def_mod, max_hp_bonus=hp_mod, conjuring_bonus=conjuring_mod, fighting_bonus=fighting_mod, shielding_bonus=shielding_mod, armor_bonus=ac_mod, transm=True, end_time=dur)
	player.fighter.buff.append(buff)

	message('You gain ' + str(buff.power_bonus) + ' Power, ' + str(buff.defense_bonus) + ' Defense, ' + str(hp_mod) + ' Max HP, ' + str(buff.conjuring_bonus) + ' Conjuring, ' + str(buff.fighting_bonus) + ' Fighting, ' + str(buff.shielding_bonus) + ' Shielding, ' + str(ac_mod) + ' AC.', libtcod.light_blue)

def cast_stone_skin():
	global game_time, spellbook

	if player.fighter.already_buffed('Stone Skin'):
		message('Already affected by Stone Skin!', libtcod.red)
		return 'cancelled'

	dur_bonus = int(round(player.fighter.magic * 0.85)) + int(round(player.fighter.transmutations * 2.5))
	dur = game_time + 14 + dur_bonus
	ac_mod = 2 + int(round(player.fighter.transmutations * 0.35))
	mr_mod = 0.25 + int(round(player.fighter.transmutations*0.0425))

	message('Your skin hardens! Gained ' + str(ac_mod) + ' AC and ' + str(100*mr_mod) + ' %% Magic Resistance.', libtcod.light_blue)
	buff = Buff('Stone Skin', armor_bonus=ac_mod, magic_resist_bonus=mr_mod, end_time=dur)
	player.fighter.buff.append(buff)

# Mineral transmutations

def transmute_item(equip, material):

	if material == 'albite':
		if transmute_item_check(1) is True:
			value = libtcod.random_get_int(0, 1, 5)
			equip.equipment.max_hp_bonus += value
			message('You successfully coalesced the ' + str(equip.name) + ' with the ' + material + '! Max HP increased by ' + str(value) + '.', libtcod.light_green)
		else:
			transmute_fail(material, equip)

	elif material == 'corundum':
		if transmute_item_check(1) is True:
			value = libtcod.random_get_int(0, 1, 3)
			equip.equipment.defense_bonus += value
			message('You successfully transmuted the ' + str(equip.name) + '! Defense increased by ' + str(value) + '.', libtcod.light_green)
		else:
			transmute_fail(material, equip)

	elif material == 'topaz':
		if transmute_item_check(4) is True:
			value_1 = libtcod.random_get_int(0, 1, 3)
			value_2 = libtcod.random_get_int(0, 1, 3)
			equip.equipment.accuracy_bonus += value_1
			equip.equipment.speed_bonus += value_2
			message('You successfully transmuted the ' + str(equip.name) + '! Accuracy increased by ' + str(value_1) + ', Speed increased by ' + str(value_2) + '.', libtcod.light_green)
		else:
			transmute_fail(material, equip)

	elif material == 'fluorite':
		if transmute_item_check(3) is True:
			value = int(round(libtcod.random_get_int(0, 1, 4) + 0.6*player.level))
			equip.equipment.defense_bonus += value
			message('You successfully transmuted the ' + str(equip.name) + '! Defense increased by ' + str(value) + '.', libtcod.light_green)
		else:
			transmute_fail(material, equip)

	elif material == 'euclase':
		if transmute_item_check(5) is True:
			equip.equipment.armor_bonus += 1
			equip.equipment.magic_resist_bonus += 0.05
			message('You successfully transmuted the ' + str(equip.name) + '! AC increased by 1, Magic Resistance increased by 5 %%.', libtcod.light_green)
		else:
			transmute_fail(material, equip)

	elif material == 'pyrite':
		if transmute_item_check(3) is True:
			value = -libtcod.random_get_int(0, 2, 4)
			equip.equipment.fighting_bonus += 1
			equip.equipment.defense_bonus += value
			message('You successfully transmuted the ' + str(equip.name) + '! Fighting increased by 1, Defense decreased by ' + str(value) + '.', libtcod.light_green)
		else:
			transmute_fail(material, equip)

	elif material == 'anatase':
		if transmute_item_check(4) is True:
			equip.equipment.magic_bonus += 1
			equip.equipment.evasion_bonus += 3
			message('You successfully transmuted the ' + str(equip.name) + '! Magic increased by 1, Evasion increased by 3.', libtcod.light_green)
		else:
			transmute_fail(material, equip)

	elif material == 'rutile':
		if transmute_item_check(1) is True:
			value = libtcod.random_get_int(0, 1, 3)
			equip.equipment.max_mana_bonus += value
			message('You successfully transmuted the ' + str(equip.name) + '! Max MP increased by ' + str(value) + '.', libtcod.light_green)
		else:
			transmute_fail(material, equip)

	elif material == 'leightonite':
		if transmute_item_check(6) is True:
			equip.equipment.power_bonus += 1
			equip.equipment.speed_bonus += 3
			message('You successfully transmuted the ' + str(equip.name) + '! Power increased by 1, Speed increased by 3.', libtcod.light_green)
		else:
			transmute_fail(material, equip)

	elif material == 'chalcanthite':
		if transmute_item_check(4) is True:
			value = libtcod.random_get_int(0, 3, 6)
			equip.equipment.defense_bonus += value
			message('You successfully transmuted the ' + str(equip.name) + '! Defense increased by ' + str(value) + '.', libtcod.light_green)
		else:
			transmute_fail(material, equip)

	elif material == 'malachite':
		if transmute_item_check(5) is True:
			value = libtcod.random_get_int(0, 1, 2)
			equip.equipment.magic_bonus += value
			message('You successfully transmuted the ' + str(equip.name) + '! Magic increased by ' + str(value) + '.', libtcod.light_green)
		else:
			transmute_fail(material, equip)

	elif material == 'azurite':
		if transmute_item_check(6) is True:
			equip.equipment.power_bonus += 1
			message('You successfully transmuted the ' + str(equip.name) + '! Power increased by 1.', libtcod.light_green)
		else:
			transmute_fail(material, equip)

	elif material == 'calcite':
		if transmute_item_check(5) is True:		
			value = libtcod.random_get_int(0, 1, 3)
			equip.equipment.evasion_bonus += value
			message('You successfully transmuted the ' + str(equip.name) + '! Evasion increased by ' + str(value) + '.', libtcod.light_green)
		else:
			transmute_fail(material, equip)

	elif material == 'star stone':
		if transmute_item_check(7) is True:
			equip.equipment.speed_bonus += 10
			message('You successfully transmuted the ' + str(equip.name) + '! Speed increased by 10.', libtcod.light_green)
		else:
			transmute_fail(material, equip)

	elif material == 'moon stone':
		if transmute_item_check(7) is True:
			equip.equipment.evasion_bonus += 10
			message('You successfully transmuted the ' + str(equip.name) + '! Evasion increased by 10.', libtcod.light_green)
		else:
			transmute_fail(material, equip)

	elif material == 'sun stone':
		if transmute_item_check(7) is True:
			equip.equipment.power_bonus += 3
			message('You successfully transmuted the ' + str(equip.name) + '! Power increased by 3.', libtcod.light_green)
		else:
			transmute_fail(material, equip)

def transmute_menu(header):

	material_list = []
	options = []

	for thing in inventory:
		if thing.item:
			if thing.item.material == True:
				text = thing.name	
				options.append(text)
				material_list.append(thing)


	if len(options) == 0:
		options = ['You have no suitable materials for transmuting.']

	index = menu(header, options, INVENTORY_WIDTH, recomp=False)
	if index is None or len(inventory) == 0:
 
		return None

	else:
		material = material_list[index].name
		libtcod.console_flush()
		render_all()
		chosen_item = equip_menu('Press the key next to a piece of equipment to transmute it, or any other key to cancel.', material)					

def equip_menu(header, material):

	equip_list = []
	options = []

	for thing in inventory:
		text = thing.name
		if thing.equipment and thing.equipment.is_equipped:
			text = text + ' (on ' + thing.equipment.slot + ')'	
			options.append(text)
			equip_list.append(thing)
		elif thing.equipment:
			options.append(text)
			equip_list.append(thing)

	if len(options) == 0:
		options = ['You have no suitable materials for transmuting.']

	index = menu(header, options, INVENTORY_WIDTH, recomp=False)
	if index is None or len(inventory) == 0:
 
		return None

	equip = equip_list[index]
	formula_check(material, equip)

def formula_check(material, equip):

	libtcod.console_flush()

	render_all()

	if material == 'albite':
		counter = 0
		for item in inventory:
			if item.name == 'albite':
				counter += 1
		
		if counter >= 2:
			
			counter = 2

			while True:
				for item in inventory:
					if counter == 0:
						break
					if item.name == 'albite':
						inventory.remove(item)
						counter -= 1
				else:
					continue
				break
			
			message('Transmuting...', libtcod.light_gray)
			transmute_item(equip, material)
		

		else:
			message('Not enough materials!', libtcod.red)

	elif material == 'corundum':
		counter = 0
		for item in inventory:
			if item.name == 'corundum':
				counter += 1

		if counter >= 2:
			
			counter = 2
			
			while True:
				for item in inventory:
					if counter == 0:
						break
					if item.name == 'corundum':
						inventory.remove(item)
						counter -= 1
				else:
					continue
				break
			
			message('Transmuting...', libtcod.light_gray)
			transmute_item(equip, material)
		

		else:
			message('Not enough materials!', libtcod.red)

	elif material == 'topaz' and equip.equipment.slot == 'right hand':

		for item in inventory:
			if item.name == 'topaz':
				transmute_item(equip, material)
				inventory.remove(item)
				break

		else:
			message('Not enough materials!', libtcod.red)

	elif material == 'euclase':

		for item in inventory:
			if item.name == 'euclase':
				transmute_item(equip, material)
				inventory.remove(item)

		else:
			message('Not enough materials!', libtcod.red)

	elif material == 'anatase' and (equip.equipment.slot == 'neck' or equip.equipment.slot == 'finger'):
		for item in inventory:
			if item.name == 'anatase':
				transmute_item(equip, material)
				inventory.remove(item)

		else:
			message('Not enough materials!', libtcod.red)

	elif material == 'rutile':
		counter = 0
		for item in inventory:
			if item.name == 'rutile':
				counter += 1
		
		if counter >= 2:
			
			counter = 2
			
			while True:
				for item in inventory:
					if counter == 0:
						break
					if item.name == 'rutile':
						inventory.remove(item)
						counter -= 1
				else:
					continue
				break
			
			message('Transmuting...', libtcod.light_gray)
			transmute_item(equip, material)
		

		else:
			message('Not enough materials!', libtcod.red)

	elif material == 'leightonite' and (equip.equipment.slot == 'neck' or equip.equipment.slot == 'finger'):

		for item in inventory:
			if item.name == 'leightonite':
				transmute_item(equip, material)
				inventory.remove(item)

		else:
			message('Not enough materials!', libtcod.red)

	elif material == 'chalcanthite' and equip.equipment.slot == 'head':
		counter = 0
		for item in inventory:
			if item.name == 'chalcanthite':
				counter += 1
	
		if counter >= 2:
			
			counter = 2
			
			while True:
				for item in inventory:
					if counter == 0:
						break
					if item.name == 'chalcanthite':
						inventory.remove(item)
						counter -= 1
				else:
					continue
				break
			
			message('Transmuting...', libtcod.light_gray)
			transmute_item(equip, material)
		

		else:
			message('Not enough materials!', libtcod.red)

	elif material == 'malachite':
		for item in inventory:
			if item.name == 'malachite':
				transmute_item(equip, material)
				inventory.remove(item)

		else:
			message('Not enough materials!', libtcod.red)

	elif material == 'azurite':
		for item in inventory:
			if item.name == 'azurite':			
				transmute_item(equip, material)
				inventory.remove(item)

		else:
			message('Not enough materials!', libtcod.red)

	elif material == 'calcite':
		counter = 0
		for item in inventory:
			if item.name == 'calcite':
				counter += 1
	
		if counter >= 2:
			
			counter = 2
			
			while True:
				for item in inventory:
					if counter == 0:
						break
					if item.name == 'calcite':
						inventory.remove(item)
						counter -= 1
				else:
					continue
				break
			
			message('Transmuting...', libtcod.light_gray)
			transmute_item(equip, material)
		

		else:
			message('Not enough materials!', libtcod.red)

	elif material == 'star stone':
		for item in inventory:
			if item.name == 'star stone':
				transmute_item(equip, material)
				inventory.remove(item)

		else:
			message('Not enough materials!', libtcod.red)	

	elif material == 'moon stone':
		for item in inventory:
			if item.name == 'moon stone':
				
				transmute_item(equip, material)
				inventory.remove(item)

		else:
			message('Not enough materials!', libtcod.red)

	elif material == 'sun stone':
		for item in inventory:
			if item.name == 'sun stone':
				transmute_item(equip, material)
				inventory.remove(item)
				break

		else:
			message('Not enough materials!', libtcod.red)

	elif material == 'pyrite':
		counter = 0
		for item in inventory:
			if item.name == 'pyrite':
				counter += 1

		if counter >= 2:
			counter = 2
			while True:
				for item in inventory:
					if counter == 0:
						break
					if item.name == 'pyrite':
						inventory.remove(item)
						counter -= 1
				else:
					continue
				break

			message('Transmuting...', libtcod.light_gray)
			transmute_item(equip, material)

		else:
			message('Not enough materials!', libtcod.red)
		

	elif material == 'fluorite':
		counter = 0
		for item in inventory:
			if item.name == 'fluorite':
				counter += 1
		if counter >= 2:
			counter = 2
			while True:
				for item in inventory:
					if counter == 0:
						break
					if item.name == 'fluorite':
						inventory.remove(item)
						counter -= 1
				else:
					continue
				break
			message('Transmuting...', libtcod.light_gray)
			transmute_item(equip, material)
		else:
			message('Not enough materials!', libtcod.red)
	
	else:
		message('Failed!', libtcod.red)

def transmute_item_check(level):
	chance = libtcod.random_get_int(0, 0, 20)
	factor = 10 - level*3
	difficulty = player.fighter.transmutations*2 + player.level + factor
	
	if difficulty >= 20:
		difficulty = 19

	if chance <= difficulty:
		return True
	return False

def transmute_fail(material, equip):
	fail_event = libtcod.random_get_int(0, 0, 20)
	if fail_event < 10:
		message('You attempt to coalesce the ' + str(equip.name) + ' with the ' + material + ', but it failed!', libtcod.red)
	else:
		if fail_event < 15:
			hp_loss = libtcod.random_get_int(0, 1, 2)
			player.fighter.max_hp -= hp_loss
			message('You attempt to coalesce the ' + str(equip.name) + ' with the ' + material + ', but it failed horribly! You feel weaker...Max HP reduced by ' + str(hp_loss) + '!', libtcod.red)
		else:
			player.fighter.max_mana -= 1
			message('You attempt to coalesce the ' + str(equip.name) + ' with the ' + material + ', but it failed horribly! You feel weaker...Max MP reduced by 1!', libtcod.red)

# Hexes

def cast_hibernation():
	global spellbook, game_time

	monster = target_monster(HIBERNATION_RANGE)

	if monster is None:
		return 'cancelled'

	if monster.fighter.already_buffed('Hibernation'):
		message(str(monster.name) + ' is already affected by hibernation!', libtcod.yellow)
		return 'cancelled'

	#spell effects
	resist_chance = int(round(monster.fighter.magic_resist*100 + monster.fighter.power/2))
	cast_mod = int(round(player.fighter.hexes*1.25)) + int(round(player.fighter.magic/2)) + libtcod.random_get_int(0, 0, 20)
	if  cast_mod > resist_chance:
		dur_bonus = int(round(player.fighter.hexes*0.5 + player.fighter.magic*0.3))
		dur = libtcod.random_get_int(0, 1, 3) + dur_bonus
		old_ai = monster.ai
		monster.ai = AsleepMonster(old_ai, num_turns=dur)
		monster.ai.owner = monster
		message('The ' + str(monster.name) + ' enters a deep slumber!', libtcod.light_blue)

		ac_mod = 1 + int(round(player.fighter.magic*0.22 + player.fighter.hexes*0.47))
		fight_mod = -5
		shielding_mod = -5
		def_mod = -25
		mod = game_time + 60

		buff = Buff('Asleep', armor_bonus=-ac_mod, fighting_bonus=fight_mod, shielding_bonus=shielding_mod, defense_bonus=def_mod, end_time=mod)
		monster.fighter.buff.append(buff)
	else:
		message('You attempt to hibernate ' + str(monster.name) + ', but ' + str(monster.name) + ' completely resists!', libtcod.red)

def cast_ritual_of_pacing():
	global game_time

	monster = target_monster(RITUAL_OF_PACING_RANGE)

	if monster is None:
		return 'cancelled'

	elif monster.fighter.already_buffed('Ritual of Pacing'):
		message(str(monster.name) + ' is already affected by Ritual of Pacing!', libtcod.red)
		return 'cancelled'

	
	resist_chance = monster.fighter.magic_resist * 100 + libtcod.random_get_int(0, 0, 100)
	castcheck = 90 + player.fighter.hexes*1.25 + player.fighter.magic*0.75
	if resist_chance < castcheck:
		dur = game_time + libtcod.random_get_int(0, 4, 7) + int(round(player.fighter.hexes*1.55))
		pwr_mod = int(round((0.25 + 0.02*player.fighter.hexes) * monster.fighter.power))
		speed_mod = -10 - player.level - int(round(player.fighter.hexes*2.25 + player.fighter.magic*1.15))
		buff = Buff('Ritual of Pacing', speed_bonus=speed_mod, power_bonus=-pwr_mod, end_time=dur)
		monster.fighter.buff.append(buff)
		message(str(monster.name) + ' is momentarily weakened, losing ' + str(pwr_mod) + ' Power and ' + str(-speed_mod) + ' speed!', libtcod.light_blue)
	else:
		message('You attempt to cast Ritual of Pacing but ' + str(monster.name) + ' resists completely!', libtcod.red)

def cast_spectral_gushes():
	global game_time

	monster = target_monster(SPECTRAL_GUSHES_RANGE)

	if monster is None:
		return 'cancelled'

	elif monster.fighter.already_buffed('Spectral Gushes'):
		message(str(monster.name) + ' is already affected by Spectral Gushes!', libtcod.red)
		return 'cancelled'

	resist_chance = monster.fighter.magic_resist * 100 + libtcod.random_get_int(0, 0, 100)
	castcheck = 90 + player.fighter.hexes*1.25 + player.fighter.magic*0.75
	if resist_chance < castcheck:
		dur = game_time + 6 + int(round(player.fighter.hexes*1.75))
		buff = Buff('Spectral Gushes', end_time=dur)
		monster.fighter.buff.append(buff)
		message('Waves of spectral energy starts to emit from ' + str(monster.name) + '. If you are close enough you can convert the energy into mana!', libtcod.light_blue)
	else:
		message('You attempt to cast Spectral Gushes but ' + str(monster.name) + ' resists completely!', libtcod.red)

def cast_hex_of_radiance():
	global spellbook, game_time

	message('Left-click a target, or right-click to cancel.', libtcod.light_cyan)
	monster = target_monster(HEX_OF_RADIANCE_RANGE)

	if monster is None:
		return 'cancelled'

	if monster.fighter.already_buffed('Hex Of Radiance'):
		message(str(monster.name) + ' is already affected by Hex Of Radiance!', libtcod.yellow)
		return 'cancelled'

	resist_chance = int(round(monster.fighter.magic_resist*100 + monster.fighter.power/2))
	cast_mod = int(round(player.fighter.hexes*1.25)) + int(round(player.fighter.magic/2)) + libtcod.random_get_int(0, 0, 20)
	if cast_mod > resist_chance:
		dur_bonus = int(round(player.fighter.hexes*0.8 + player.fighter.magic*0.4))
		dur = libtcod.random_get_int(0, 3, 6) + dur_bonus + game_time

		buff = Buff('Hex Of Radiance', end_time=dur)
		monster.fighter.buff.append(buff)
		message(str(monster.name) + ' begins to emit golden rays of light!', libtcod.light_blue)

		for y in range(MAP_HEIGHT):
			for x in range(MAP_WIDTH):
				if monster.distance(x, y) <= 5:
					visible = libtcod.map_is_in_fov(fov_map, x, y)
					wall = tilemap[x][y].block_sight
					if not visible:
						if tilemap[x][y].explored:
							if wall:
								libtcod.console_put_char_ex(con, x, y, wall_tile, libtcod.dark_yellow, libtcod.black)
							else:									
								libtcod.console_put_char_ex(con, x, y, floor_tile, libtcod.dark_yellow, libtcod.black)
					else:
						if wall:
							libtcod.console_put_char_ex(con, x, y, wall_tile, libtcod.light_yellow, libtcod.black)
						else:
							libtcod.console_put_char_ex(con, x, y, floor_tile, libtcod.light_yellow, libtcod.black)
						tilemap[x][y].explored = True
			
	else:
		message(str(monster.name) + ' resists your Hex Of Radiance completely!', libtcod.red)

#---MISC FUNCTIONS---#

def mana_well_use():
	if mana_well.name != 'mana well (depleted)':
		player.fighter.mana = player.fighter.max_mana
		message('You feel refreshed! Mana fully restored.', libtcod.light_violet)
		mana_well.name = 'mana well (depleted)'
	else:
		message('The mana well is depleted!', libtcod.red)

def health_shrine_use():
	if health_shrine.name != 'health shrine (depleted)':
		player.fighter.hp = player.fighter.max_hp
		message('You feel your strength return! Health fully restored.', libtcod.light_violet)
		health_shrine.name = 'health shrine (depleted)'
	else:
		message('The health shrine is depleted!', libtcod.red)

def no_thanks():
	message('Really? Okay then... <takes a big bite>. That was absolutely disgusting.', libtcod.light_gray)

def eat_apple():
	global game_time
	message('You quickly consume the apple. Delightful!')
	dur = 10 + libtcod.random_get_int(0, 2, 5) + game_time
	buff = Buff('Satiated', hp_regen_bonus=1, end_time=dur)
	player.fighter.buff.append(buff)

def eat_fry():
	message('You consume the french fry, enjoying the shortest meal of your life thus far.', libtcod.light_violet)
	value = libtcod.random_get_int(0, 1, 4)
	dice = libtcod.random_get_int(0, 0, 100)
	if dice < 50:
		player.fighter.hp += value
		message('You gain ' + str(value) + ' hit points.', libtcod.light_violet)
	else:
		player.fighter.mana += value
		message('You gain ' + str(value) + ' mana points.', libtcod.light_violet)

def eat_bread():
	message('You feast on the loaf of bread. It tastes great!', libtcod.light_violet)
	hp_value = libtcod.random_get_int(0, 1, 3)
	mp_value = libtcod.random_get_int(0, 1, 3)
	player.fighter.hp += hp_value
	player.fighter.mana += mp_value
	message('You gain ' + str(hp_value) + ' hit points and ' + str(mp_value) + ' mana points.', libtcod.light_green)

def stealth_roll(monster):
	if ((player.race == 'Green Elf') and (libtcod.map_is_in_fov(fov_map, monster.x, monster.y)) and (monster.distance_to(player) >= 2)):
		# roll for stealthiness
		roll = 2*player.fighter.stealthiness + player.level + libtcod.random_get_int(0, 0, 20)
		threshold = 0.6*monster.fighter.power + 16 + libtcod.random_get_int(0, 0, 20)
		if roll >= threshold:
			message('The ' + monster.name + ' loses vision of you for a moment.')
			return True
		return False

def fill_loot(name):

	loot = []

	if name == 'bookshelf':

		chances = {}

		chances['scroll'] = 20
		chances['spellbook'] = 10
		chances['text'] = 25
		chances['jewelry'] = 7
		chances['nothing'] = 38

		choice = random_choice(chances)

		if choice == 'scroll':

			scroll_chances = {}

			scroll_chances['lightning'] = from_dungeon_level([[20, 1], [23, 2], [25, 3], [28, 4], [30, 5], [33, 6]])
			scroll_chances['confuse'] = from_dungeon_level([[50, 1], [47, 2], [44, 3], [41, 4], [38, 5], [35, 6]])
			scroll_chances['fireball'] = from_dungeon_level([[5, 1], [7, 2], [9, 3], [12, 4], [15, 5], [18, 6]])
			scroll_chances['knowledge'] = from_dungeon_level([[5, 1], [6, 2], [7, 3], [8, 4], [9, 5], [10, 6]])

			scroll_choice = random_choice(scroll_chances)

			if scroll_choice == 'lightning':

				item_component = Item(use_function=cast_lightning)
				item = Object(0, 0, scroll_tile, 'scroll of lightning bolt', libtcod.white, item=item_component)
				loot.append(item)

			elif scroll_choice == 'confuse':

				item_component = Item(use_function=cast_confuse)
				item = Object(0, 0, scroll_tile, 'scroll of confusion', libtcod.white, item=item_component)
				loot.append(item)

			elif scroll_choice == 'fireball':

				item_component = Item(use_function=cast_fireball)
				item = Object(0, 0, scroll_tile, 'scroll of fireball', libtcod.white, item=item_component)
				loot.append(item)

			elif scroll_choice == 'knowledge':

				item_component = Item(use_function=gain_skill)
				item = Object(0, 0, scroll_tile, 'scroll of knowledge', libtcod.white, item=item_component)
				loot.append(item)

		elif choice == 'spellbook':

			book_chances = {}

			book_chances['ice conj'] = 22
			book_chances['fire conj'] = 22
			book_chances['hex'] = 28
			book_chances['transm'] = 28

			book_choice = random_choice(book_chances)

			if book_choice == 'ice conj':

				item_component = Item(use_function=learn_spell_ice_conj)
				item = Object(0, 0, 'B', 'Book of Ice Conjurations', libtcod.darker_lime, item=item_component)
				loot.append(item)

			elif book_choice == 'fire conj':

				item_component = Item(use_function=learn_spell_fire_conj)
				item = Object(0, 0, 'B', 'Book of Fire Conjurations', libtcod.darker_lime, item=item_component)
				loot.append(item)

			elif book_choice == 'transm':

				item_component = Item(use_function=learn_spell_transm)
				item = Object(0, 0, 'B', 'Book of Transmutations', libtcod.darker_lime, item=item_component)
				loot.append(item)

			elif book_choice == 'hex':

				item_component = Item(use_function=learn_spell_hex)
				item = Object(0, 0, 'B', 'Book of Hexes', libtcod.darker_lime, item=item_component)
				loot.append(item)

		elif choice == 'text':

			text_chances = {}

			text_chances['page1'] = 5
			text_chances['page2'] = 5
			text_chances['page3'] = 5
			text_chances['page4'] = 5
			text_chances['page5'] = 5
			text_chances['page6'] = 5
			text_chances['page7'] = 5

			text_choice = random_choice(text_chances)

			if text_choice == 'page1':

				item_component = Item(use_function=read_page_1)
				item = Object(0, 0, scroll_tile, 'loose page', libtcod.white, item=item_component)
				loot.append(item)

			if text_choice == 'page2':

				item_component = Item(use_function=read_page_2)
				item = Object(0, 0, scroll_tile, 'loose page', libtcod.white, item=item_component)
				loot.append(item)

			if text_choice == 'page3':

				item_component = Item(use_function=read_page_3)
				item = Object(0, 0, scroll_tile, 'loose page', libtcod.white, item=item_component)
				loot.append(item)

			if text_choice == 'page4':

				item_component = Item(use_function=read_page_4)
				item = Object(0, 0, scroll_tile, 'loose page', libtcod.white, item=item_component)
				loot.append(item)

			if text_choice == 'page5':

				item_component = Item(use_function=read_page_5)
				item = Object(0, 0, scroll_tile, 'a note', libtcod.white, item=item_component)
				loot.append(item)

			if text_choice == 'page6':

				item_component = Item(use_function=read_page_6)
				item = Object(0, 0, scroll_tile, 'piece of parchment', libtcod.white, item=item_component)
				loot.append(item)

			if text_choice == 'page7':

				item_component = Item(use_function=read_page_7)
				item = Object(0, 0, scroll_tile, 'piece of parchment', libtcod.white, item=item_component)
				loot.append(item)

			if text_choice == 'page8':

				item_component = Item(use_function=read_page_8)
				item = Object(0, 0, scroll_tile, 'a note', libtcod.white, item=item_component)

		elif choice == 'jewelry':

			jewelry_chances = {}

			jewelry_chances['arcane ring'] = 50
			jewelry_chances['ring of prot'] = 50
			jewelry_chances['ring of vigor'] = 50
			jewelry_chances['jade star ring'] = 50
			jewelry_chances['red-tinted jasper ring'] = 50

			jewelry_chances['crystal ring'] = 8
			jewelry_chances['tricellite ring'] = 8

			jewelry_chances['amulet of magic res'] = 50
			jewelry_chances['faint light'] = 50
			jewelry_chances['luminous stone necklace'] = 50

			jewelry_choice = random_choice(jewelry_chances)

			if jewelry_choice == 'arcane ring':

				equipment_component = Equipment(slot='finger', magic_bonus=1)
				item = Object(0, 0, 'Q', 'arcane ring', libtcod.light_violet, equipment=equipment_component)
				loot.append(item)

			elif jewelry_choice == 'ring of prot':

				equipment_component = Equipment(slot='finger', armor_bonus=1)
				item = Object(0, 0, 'Q', 'ring of protection', libtcod.copper, equipment=equipment_component)
				loot.append(item)

			elif jewelry_choice == 'ring of vigor':

				def_mod = item_rand(4)
				maxhp_mod = item_rand(4)

				quality = [def_mod, maxhp_mod]

				if sum(quality) > 5:
					name = 'ring of agility'
				else:
					name = 'ring of vigor'

				equipment_component = Equipment(slot='finger', defense_bonus=3+def_mod, max_hp_bonus=2+maxhp_mod, evasion_bonus=2)
				item = Object(0, 0, 'Q', name, libtcod.darker_yellow, equipment=equipment_component) 
				loot.append(item)

			elif jewelry_choice == 'jade star ring':

				dice = libtcod.random_get_int(0, 0, 100)

				transm_mod = 0
				hex_mod = 0

				if dice > 50:
					transm_mod += 1
				else:
					hex_mod += 1


				equipment_component = Equipment(slot='finger', defense_bonus=5, transmutations_bonus=0+transm_mod, hexes_bonus=0+hex_mod)
				item = Object(0, 0, 'Q', 'jade star ring', libtcod.dark_chartreuse, equipment=equipment_component)
				loot.append(item)

			elif jewelry_choice == 'red-tinted jasper ring':

				equipment_component = Equipment(slot='finger', speed_bonus=5, archery_bonus=1)
				item = Object(0, 0, 'Q', 'red-tinted jasper ring', libtcod.darker_magenta, equipment=equipment_component)
				loot.append(item)

			elif jewelry_choice == 'crystal ring':

				equipment_component = Equipment(slot='finger', fighting_bonus=1, shielding_bonus=1, archery_bonus=1, conjuring_bonus=1, transmutations_bonus=1, hexes_bonus=1)
				item = Object(0, 0, 'Q', 'crystal ring', libtcod.dark_yellow, equipment=equipment_component)
				loot.append(item)

			elif jewelry_choice == 'tricellite ring':

				equipment_component = Equipment(slot='finger', defense_bonus=10, fighting_bonus=1, shielding_bonus=1, magic_resist_bonus=0.05, prof_restriction=['Fighter'])
				item = Object(0, 0, 'Q', 'dazzling tricellite ring', libtcod.dark_azure, equipment=equipment_component)
				loot.append(item)

			elif jewelry_choice == 'amulet of magic res':

				mr_mod = item_rand(10) / 100
				maxhp_mod = 0

				if mr_mod > 0.08:
					maxhp_mod += 5
					name = 'amulet of spellshielding'
				else:
					name = 'amulet of magic protection'

				equipment_component = Equipment(slot='neck', magic_resist_bonus=0.15+mr_mod, max_hp_bonus=maxhp_mod)
				item = Object(0, 0, 'v', name, libtcod.dark_red, equipment=equipment_component)
				loot.append(item)

			elif jewelry_choice == 'faint light':

				equipment_component = Equipment(slot='neck', heal_kill_bonus=1)
				item = Object(0, 0, 'v', 'faint light', libtcod.darkest_yellow, equipment=equipment_component)
				loot.append(item)

			elif jewelry_choice == 'luminous stone necklace':

				equipment_component = Equipment(slot='neck', armor_bonus=1, defense_bonus=6, evasion_bonus=5, magic_resist_bonus=-0.05)
				item = Object(0, 0, 'v', 'luminous stone necklace', libtcod.dark_lime, equipment=equipment_component)
				loot.append(item)

	elif name == 'ore deposit':

		minerals = libtcod.random_get_int(0, 1, 2)

		chances = {}

		chances['albite'] = 10
		chances['corundum'] = 10
		chances['topaz'] = 2
		chances['fluorite'] = 10 
		chances['euclase'] = 2
		chances['pyrite'] = 9
		chances['anatase'] = 2
		chances['rutile'] = 8
		chances['leightonite'] = 1
		chances['chalcanthite'] = 6
		chances['malachite'] = 2
		chances['azurite'] = 2   
		chances['calcite'] = 7
		chances['star stone'] = 1 
		chances['moon stone'] = 1  
		chances['sun stone'] = 1

		for i in range(minerals): 
			choice = random_choice(chances)

			if choice == 'albite':

				item_component = Item(material=True)
				item = Object(0, 0, 'e', 'albite', libtcod.white, item=item_component)
				loot.append(item)

			elif choice == 'corundum':

				item_component = Item(material=True)
				item = Object(0, 0, 'e', 'corundum', libtcod.white, item=item_component)
				loot.append(item)

			elif choice == 'topaz':

				item_component = Item(material=True)
				item = Object(0, 0, 'e', 'topaz', libtcod.white, item=item_component)
				loot.append(item)

			elif choice == 'fluorite':

				item_component = Item(material=True)
				item = Object(0, 0, 'e', 'fluorite', libtcod.white, item=item_component)
				loot.append(item)

			elif choice == 'euclase':

				item_component = Item(material=True)
				item = Object(0, 0, 'e', 'euclase', libtcod.white, item=item_component)
				loot.append(item)

			elif choice == 'pyrite':

				item_component = Item(material=True)
				item = Object(0, 0, 'e', 'pyrite', libtcod.white, item=item_component)
				loot.append(item)

			elif choice == 'anatase':

				item_component = Item(material=True)
				item = Object(0, 0, 'e', 'anatase', libtcod.white, item=item_component)
				loot.append(item)

			elif choice == 'rutile':

				item_component = Item(material=True)
				item = Object(0, 0, 'e', 'rutile', libtcod.white, item=item_component)
				loot.append(item)

			elif choice == 'leightonite':

				item_component = Item(material=True)
				item = Object(0, 0, 'e', 'leightonite', libtcod.white, item=item_component)
				loot.append(item)

			elif choice == 'chalcanthite':

				item_component = Item(material=True)
				item = Object(0, 0, 'e', 'chalcanthite', libtcod.white, item=item_component)
				loot.append(item)

			elif choice == 'malachite':

				item_component = Item(material=True)
				item = Object(0, 0, 'e', 'malachite', libtcod.white, item=item_component)
				loot.append(item)

			elif choice == 'azurite':

				item_component = Item(material=True)
				item = Object(0, 0, 'e', 'azurite', libtcod.white, item=item_component)
				loot.append(item)

			elif choice == 'calcite':

				item_component = Item(material=True)
				item = Object(0, 0, 'e', 'calcite', libtcod.white, item=item_component)
				loot.append(item)

			elif choice == 'star stone':

				item_component = Item(material=True)
				item = Object(0, 0, 'e', 'star stone', libtcod.white, item=item_component)
				loot.append(item)

			elif choice == 'moon stone':

				item_component = Item(material=True)
				item = Object(0, 0, 'e', 'moon stone', libtcod.white, item=item_component)
				loot.append(item)

			elif choice == 'sun stone':

				item_component = Item(material=True)
				item = Object(0, 0, 'e', 'sun stone', libtcod.white, item=item_component)
				loot.append(item)

	return loot

def place_lootobj(value, name):

	if name == 'bookshelf':

		while True:
			for room in rooms:
				randgimp = libtcod.random_get_int(0, 0, 100)
				if randgimp >= 20:
					continue
				for (x, y) in room.inner_edges():

					if value <= 0:
						return

					if not is_blocked(x, y) and check_objects(x, y) is False and player.distance(x, y) > 10:

						chance = libtcod.random_get_int(0, 0, 100)
					
						if chance > 93:

							loot = fill_loot(name)

							loot_component = LootObj(name, loot=loot)
							shelf = Object(x, y, 'F', name, libtcod.darkest_amber, blocks=False, always_visible=True, loot=loot_component)
							objects.append(shelf)
							shelf.send_to_back()
							value -= 1
			break

	elif name == 'ore deposit':

		while True:
			for room in rooms:
				randgimp = libtcod.random_get_int(0, 0, 100)
				if randgimp >= 20:
					continue
				for (x, y) in room.inner_edges():

					if value <= 0:
						return

					if not is_blocked(x, y) and check_objects(x, y) is False and player.distance(x, y) > 10:

						chance = libtcod.random_get_int(0, 0, 100)
					
						if chance > 95:

							loot = fill_loot(name)

							loot_component = LootObj(name, loot=loot)
							deposit = Object(x, y, 'o', name, libtcod.dark_sepia, blocks=False, always_visible=True, loot=loot_component)
							objects.append(deposit)
							deposit.send_to_back()
							value -= 1
			break

#---TEXTS---#

def read_page_1():

	libtcod.console_flush()

	render_all()

	COLCTRL()

	text = """ %cThe Splitting of Perceptual Processing by Arcane Forces - Spelles Ledeuze%c 

 ...then the principles of sensations are the same time principles of 
 composition of magic; conversely, it is composite magic that are best 
 capable of revealing those conditions of sensibility. The task for magic
 is to push us out of our habits of perception into these conditions of 
 creation. When we percieve the properties of a substance, we see it with
 an all too stale eye, loaded with cliches... we order the world in 
 representation. What we are after is a spell that produces an effect 
 on the nervous system without affecting the brain. Something that cannot 
 be re-cognized, something imperceptible, that excludes the move to 
 conceptual ordering.

 Page 2""" % (libtcod.COLCTRL_1, libtcod.COLCTRL_2)

	transp_msgbox('%s' % text, width=80)

def read_page_2():

	libtcod.console_flush()

	render_all()

	COLCTRL()

	text = """ %cThe Splitting of Perceptual Processing by Arcane Forces - Spelles Ledeuze%c

 The Magician does not simply produce a fiction or semblance to the world, 
 but rather produces a new way of sensing the world, a new form of sensibility. 
 We can see something similar at work in evolutionary biology: The evolution 
 of a new species isn't simply the evolution of a new organism or body, but 
 also the evolution of the new form of sensibility and the differentiation 
 of the environment.
 A snake and a tortoise might well exist in the same spatial region of the 
 universe, but nonetheless have entirely different environments structured
 according to the system of relevancies pertaining to their specific organism.

 Page 3""" % (libtcod.COLCTRL_1, libtcod.COLCTRL_2)

	transp_msgbox('%s' % text, width=80)

def read_page_3():

	libtcod.console_flush()

	render_all()

	text=""" %cJuly 18th%c

 The limitation of the quantisation of qualia in a medium of communication 
 is the frustration of the mind that triggers deterritorializing 
 enactments in order to transcend itself.
	 
	 %cF.D.""" % (libtcod.COLCTRL_1, libtcod.COLCTRL_2, libtcod.COLCTRL_STOP)

	transp_msgbox('%s' % text, width=80)

def read_page_4():

	libtcod.console_flush()

	render_all()

	COLCTRL()

	text ="""   %cUnder summer%c
    be still, be

   unconscious of a surface
       to the evening, broadened
        by that more and different May:
          a behaved response, and the sun
   - in and out of its substances -
   waves at
          them for dinner...

             May made to June
          the
              exposure into its
          existence in text:

    beauty, beam, these are,
              summarised by the
       mind,
             an activity, an attractive part, and
         against them with their bodies,
      between
            an objects metaphor of
          the dazzling
     surface

        February, March, April

    be boundary and still
   under summer""" % (libtcod.COLCTRL_1, libtcod.COLCTRL_2)

	transp_msgbox('%s' % text, width=80)

def read_page_5():

	libtcod.console_flush()

	render_all()

	COLCTRL()	

	text = """ %cunknown title - unknown author%c

 A dream I once had. I documented it in the morning during which I still 
 felt innervated by its sensations. The intensity of the colors, forms and 
 shapes dwelled at the back of my head for several weeks' time... 

 In a world where time stands still. A world where one simultaneously 
 experiences the gentle light of dawn and the silent onset of nightfall. 
 A world where the ground is bestowed with a canvas of variegated crimson, 
 illuminated by the refractions of an infinite sky. 

 There is a city that grows vertically. It has existed for so long and grown 
 so tall that even on a clear day its height was far beyond the limits of 
 visibility. The reason time has stopped is that the world has no memories. 
 There is no experience of a beginning, and there will be no experience of 
 an end. 

 There are no books, no stories, and no songs. There are no statues, 
 no gardens, no newspapers, and no festivals. There are no research, no 
 science, no philosophy or theatres, and no concert halls. Neither are there 
 any money, social hierarchies or legal systems. There are no graveyards. 
 Nobody is close, and nobody is lonely. """ % (libtcod.COLCTRL_1, libtcod.COLCTRL_2)

	transp_msgbox('%s' % text, width=80)

def read_page_6():

	libtcod.console_flush()

	render_all()

	COLCTRL()

	text = """ %cThe joy is gone from your voice...%c

 said a very nice old lady who I know in passing. She is the only person
 in my life who has noticed, who had the balls to say it, and who had a
 beautiful way of saying something that breaks my heart in its honesty.

 My family has said nothing. My friends have said nothing. Nobody notices 
 or cares. The only one who does is a woman that I see maybe once a month
 at my job... and she can look at me and listen to me and see it instantly.

 It was different when I was 15. 'Oh, it's a hard phase. You're finding 
 your place.'
 It was different when I was 20. 'Oh, you're figuring out how to be an adult.'
 It was different when I was 25. 'Well, pick yourself up and dust 
 yourself off.'
 It was different at 30. 'Uhh, well, here, have another drink.'
 It was different at 35. 'Uh, aren't you supposed to be over this by now?'
 The joy is gone from my voice. I'll just sit here at work, trying to 
 live another day, a fifth of vodka under my desk, waiting for a knock
 at the door or a phone call telling me when I'm done. """ % (libtcod.COLCTRL_1, libtcod.COLCTRL_2)

	transp_msgbox('%s' % text, 80)

def read_page_7():

	libtcod.console_flush()

	render_all()

	COLCTRL()

	text = """ %cUnknown title - unknown author%c

 I have a childlike fascination with everything. I am delighted by the natural
 world - discovering a plant or beetle I've never seen before, walking in the
 forest, sitting by the ocean, gazing at the moon and stars, listening to 
 music and language - these things fill me with such intense awe and joy. 
 I feel a purpose and a connection to this planet.

 Half my people died this summer. A new sun rises never to return, having 
 become fed-up with our misery... We don't do anything about suffering and
 inequality. We fill our brains with bullshit, disposable coffee cups, 
 fake pleasures, fake conversations, fake personalities, fake emotions,
 instant gratification, bullshit new, bullshit fucking everything.

 How can humans be so great, so miraculous, so talented, so capable yet
 so completely selfish, shallow, robotic and consumerist? It's like a 
 shitty dystopian fantasy novel. Everything I love is being destroyed. """ % (libtcod.COLCTRL_1, libtcod.COLCTRL_2)

	transp_msgbox('%s' % text, 80)

def read_page_8():

	libtcod.console_flush()

	render_all()

	COLCTRL()

	text = """ %cAdam Dalia Entente%c

      Swerve, malign, to the beat

      Sudden incalibration woven by angst
      We are plastic containers in this world

      Dyed up in principled malfunction
      When no body finds intent

      And far as they go in bliss
      Uncompromising as the vanguard of that held dear

      One shall step down from covering the faint """

	transp_msgbox('%s' % text, 80)

#---race FUNCTIONS---#

def cast_freeze(target):
	dice = libtcod.random_get_int(0, 2, 4)
	dur = dice + 1
	old_ai = target.ai
	target.ai = FrozenMonster(old_ai, target.color, dur)
	target.color = libtcod.sky
	target.ai.owner = target
	message('The ' + str(target.name) + ' is frozen solid!', libtcod.violet)

def cast_explosive(target):
	damage = int(round(((libtcod.random_get_int(0, 10, 17) + player.fighter.magic*0.8) * (1 + player.fighter.conjuring*0.03))))
	message('The explosive trap is triggered! It burns anyone within 4 tiles for ' + str(damage) + ' points of damage!', libtcod.light_violet)
	for obj in objects:
		if obj.fighter and obj.distance(target.x, target.y) <= 4:
			message('The ' + obj.name + ' burns for ' + str(damage) + ' hit points.', libtcod.light_blue)
			obj.fighter.take_damage(damage)

def cast_stealth():
	global spellbook, game_time

	if player.fighter.already_buffed('Stealth cd'):
		message('Skill still on cooldown! You must wait before using this ability again.', libtcod.red)
		return 'cancelled'

	(x, y) = (player.x, player.y)
	for obj in objects:
		if obj.distance(x, y) <= 12 and libtcod.map_is_in_fov(fov_map, obj.x, obj.y):
			if obj.fighter and obj != player:
				dice = libtcod.random_get_int(0, 0, 20)
				break_chance = int(round(obj.fighter.power/2)) + libtcod.random_get_int(0, 0, 20)
				cast_mod = int(round((player.level*1.5 + player.fighter.stealthiness*2))) + libtcod.random_get_int(0, 0, 20)
				if cast_mod > break_chance and (obj.fighter.hp >= int(round((obj.fighter.max_hp*0.8)))):
					stealth_mod = 6 + int(round(((player.level*1.5) + (player.fighter.transmutations*0.5))))
					old_ai = obj.ai
					obj.ai = StealthMonster(old_ai, num_turns=stealth_mod)
					obj.ai.owner = obj
				else:
					message('The ' + obj.name + ' is unaffected by Stealth!', libtcod.red)

	message('You fade into the shadows, becoming transparent to enemies!', libtcod.light_blue)
	dur = 60 + game_time
	buff = Buff('Stealth cd', end_time=dur, displays=False)
	player.fighter.buff.append(buff)

def cast_shield_block():
	global spellbook, game_time

	if player.fighter.already_buffed('Shield Block') is True:
		message('Shield block is already active!', libtcod.red)
		return 'cancelled'

	amount = int(round(5 + 0.25*player.fighter.shielding))
	defense = int(round(5 + 0.25*player.fighter.defense))
	dur = game_time + 30
	buff = Buff('Shield Block', shielding_bonus=amount, defense_bonus=defense, end_time=dur)
	player.fighter.buff.append(buff)
	message('You gain + ' + str(amount) + ' shielding and + ' + str(defense) + ' defense!', libtcod.light_violet)

def cast_freezing_trap():
	global spellbook, game_time

	(x, y) = target_tile(1)
	message('Click an adjacent tile to lay the trap.', libtcod.light_cyan)
	if (x, y) is None:
		return 'cancelled'

	for obj in objects:
		if obj.x == x and obj.y == y and obj.fighter:
			message('You have to place traps on empty tiles!', libtcod.yellow)
			return 'cancelled'

	dur = game_time + 120
	trap_component = Trap('Freezing Trap', cast_freeze, dur)	
	obj = Object(x, y, floor_tile, 'freezing trap', libtcod.azure, blocks=False, trap=trap_component)
	objects.append(obj)
	message('You placed a freezing trap. Now lure the enemy into it!', libtcod.light_blue)

def cast_explosive_trap():
	global spellbook, game_time

	(x, y) = target_tile(1)
	message('Click an adjacent tile to lay the trap.', libtcod.light_cyan)
	if (x, y) is None:
		return 'cancelled'
	for obj in objects:
		if obj.x == x and obj.y == y and obj.fighter:
			message('You have to place traps on empty tiles!', libtcod.yellow)
			return 'cancelled'

	dur = game_time + 120
	trap_component = Trap('Explosive Trap', cast_explosive, dur)	
	obj = Object(x, y, floor_tile, 'explosive trap', libtcod.orange, blocks=False, trap=trap_component)
	objects.append(obj)
	message('You placed an explosive trap. Now lure the enemy into it!', libtcod.light_blue)

#---LEARNING SPELLS---#

# def append_magic_dart():
# 	spell = Spell('Magic Dart', 2, use_function=cast_magic_dart, level=1)
# 	if spell not in spellbook:
# 		spellbook.append(spell)
# 		message('You have learned a new spell!', libtcod.light_green)
# 	else:
# 		message('You have already learned this spell!', libtcod.red)

# def append_life_tap():
# 	spell = Spell('Life Tap', 0, use_function=cast_life_tap, level=1)
# 	if spell not in spellbook:
# 		spellbook.append(spell)
# 		message('You have learned a new spell!', libtcod.light_green)
# 	else:
# 		message('You have already learned this spell!', libtcod.red)

# def append_ice_barrier():
# 	spell = Spell('Ice Barrier', 4, use_function=cast_ice_barrier, level=3)
# 	if spell not in spellbook:
# 		spellbook.append(spell)
# 		message('You have learned a new spell!', libtcod.light_green)
# 	else:
# 		message('You have already learned this spell!', libtcod.red)

# def append_lesser_heal():
# 	spell = Spell('Lesser Heal', 3, use_function=cast_lesser_heal, level=2)
# 	if spell not in spellbook:
# 		spellbook.append(spell)
# 		message('You have learned a new spell!', libtcod.light_green)
# 	else:
# 		message('You have already learned this spell!', libtcod.red)

# def append_rain_of_ice():
# 	spell = Spell('Rain of Ice', 6, use_function=cast_rain_of_ice, level=6)
# 	if spell not in spellbook:
# 		spellbook.append(spell)
# 		message('You have learned a new spell!', libtcod.light_green)
# 	else:
# 		message('You have already learned this spell!', libtcod.red)

# def append_chain_lightning():
# 	global spellbook
# 	spell = Spell('Chain Lightning', 6, use_function=cast_chain_lightning, level=5)
# 	if spell not in spellbook:
# 		spellbook.append(spell)
# 		message('You have learned a new spell!', libtcod.light_green)
# 	else:
# 		message('You have already learned this spell!', libtcod.red)

# def append_fire_blast():
# 	global spellbook
# 	spell = Spell('Fire Blast', 7, use_function=cast_fire_blast, level=7)
# 	if spell not in spellbook:
# 		spellbook.append(spell)
# 		message('You have learned a new spell!', libtcod.light_green)
# 	else:
# 		message('You have already learned this spell!', libtcod.red)

# def append_conjure_food():
# 	global spellbook
# 	spell = Spell('Conjure Food', 2, use_function=cast_conjure_food, level=2)
# 	if spell not in spellbook:
# 		spellbook.append(spell)
# 		message('You have learned a new spell!', libtcod.light_green)
# 	else:
# 		message('You have already learned this spell!', libtcod.red)

# def append_bolt_of_ice():
# 	global spellbook
# 	spell = Spell('Bolt of Ice', 3, use_function=cast_bolt_of_ice, level=2)
# 	if spell not in spellbook:
# 		spellbook.append(spell)
# 		message('You have learned a new spell!', libtcod.light_green)
# 	else:
# 		message('You have already learned this spell!', libtcod.red)

# def append_shield_block():
# 	global spellbook
# 	spell = Spell('Shield Block', 3, use_function=cast_shield_block, level=3)
# 	if spell not in spellbook:
# 		spellbook.append(spell)
# 		message('You have learned a new spell!', libtcod.light_green)
# 	else:
# 		message('You have already learned this spell!', libtcod.red)

# def append_freezing_trap():
# 	global spellbook
# 	spell = Spell('Freezing Trap', 3, use_function=cast_freezing_trap, level=1)
# 	if spell not in spellbook:
# 		spellbook.append(spell)
# 		message('You have learned a new spell!', libtcod.light_green)
# 	else:
# 		message('You have already learned this spell!', libtcod.red)

# def append_explosive_trap():
# 	global spellbook
# 	spell = Spell('Freezing Trap', 3, use_function=cast_explosive_trap, level=1)
# 	if spell not in spellbook:
# 		spellbook.append(spell)
# 		message('You have learned a new spell!', libtcod.light_green)
# 	else:
# 		message('You have already learned this spell!', libtcod.red)

# def append_beastly_talons():
# 	global spellbook
# 	spell = Spell('Beastly Talons', 3, use_function=cast_beastly_talons, level=1)
# 	if spell not in spellbook:
# 		spellbook.append(spell)
# 		message('You have learned a new spell!', libtcod.light_green)
# 	else:
# 		message('You have already learned this spell!', libtcod.red)

# def append_unholy_rage():
# 	spell = Spell('Unholy Rage', 5, use_function=cast_unholy_rage, level=3)
# 	if spell not in spellbook:
# 		spellbook.append(spell)
# 		message('You have learned a new spell!', libtcod.light_green)
# 	else:
# 		message('You have already learned this spell!', libtcod.red)

# def append_immolate():
# 	global spellbook
# 	spell = Spell('Immolate', 3, use_function=cast_immolate, level=2)
# 	if spell not in spellbook:
# 		spellbook.append(spell)
# 		message('You have learned a new spell!', libtcod.light_green)
# 	else:
# 		message('You have already learned this spell!', libtcod.red)

# def append_felid_form():
# 	global spellbook
# 	spell = Spell('Felid Form', 6, use_function=cast_felid_form, level=4)
# 	if spell not in spellbook:
# 		spellbook.append(spell)
# 		message('You have learned a new spell!', libtcod.light_green)
# 	else:
# 		message('You have already learned this spell!', libtcod.red)

# def append_bear_form():
# 	global spellbook
# 	spell = Spell('Bear Form', 4, use_function=cast_bear_form, level=5)
# 	if spell not in spellbook:
# 		spellbook.append(spell)
# 		message('You have learned a new spell!', libtcod.light_green)
# 	else:
# 		message('You have already learned this spell!', libtcod.red)

# def append_stone_skin():
# 	global spellbook
# 	spell = Spell('Stone Skin', 2, use_function=cast_bear_form, level=2)
# 	if spell not in spellbook:
# 		spellbook.append(spell)
# 		message('You have learned a new spell!', libtcod.light_green)
# 	else:
# 		message('You have already learned this spell!', libtcod.red)

# def append_stealth():
# 	global spellbook
# 	spell = Spell('Stealth', 2, use_function=cast_stealth, level=2)
# 	if spell not in spellbook:
# 		spellbook.append(spell)
# 		message('You have learned a new spell!', libtcod.light_green)
# 	else:
# 		message('You have already learned this spell!', libtcod.red)

# def append_hibernation():
# 	global spellbook
# 	spell = Spell('Hibernation', 2, use_function=cast_hibernation, level=2)
# 	if spell not in spellbook:
# 		spellbook.append(spell)
# 		message('You have learned a new spell!', libtcod.light_green)
# 	else:
# 		message('You have already learned this spell!', libtcod.red)

def learn_spell():
	return 'spell'

def learn_spell_ice_conj():
	global spellbook

	render_all()

	libtcod.console_flush()

	choice = None

	while choice == None:
		choice = menu('Book of Ice Conjurations\n\nYou may memorize one of the following spells:\n\n',
		['Ice Barrier\t (requires level 2)',
		'Bolt of Ice\t (requires level 3)', 
		'Rain of Ice\t (requires level 6)',
		'Summon Ice Beast\t (requires level 8)'], LEVEL_SCREEN_WIDTH)

	if choice == 0:
		if player.level >= 2:
			append_spell('Ice Barrier')
		else:
			message('You are too inexperienced to memorize this spell.', libtcod.yellow)
	elif choice == 1:
		if player.level >= 3:
			append_spell('Bolt of Ice')
		else:
			message('You are too inexperienced to memorize this spell.', libtcod.yellow)
	elif choice == 2:
		if player.level >= 6:
			append_spell('Rain of Ice')
		else:
			message('You are too inexperienced to memorize this spell.', libtcod.yellow)
	elif choice == 3:
		if player.level >= 8:
			append_spell('Summon Ice Beast')
		else:
			message('You are too inexperienced to memorize this spell.', libtcod.yellow)

def learn_spell_fire_conj():
	global spellbook

	render_all()

	libtcod.console_flush()

	choice = None

	while choice == None:
		choice = menu('Book of Fire Conjurations\n\nYou may memorize one of the following spells:\n\n',
		['Immolate\t (requires lvl 2)',
		'Divination of Warmth\t (requires lvl 4)', 
		'Fire Blast\t (requires lvl 6)',
		'White Light\t (requires lvl 8)'], LEVEL_SCREEN_WIDTH)

	if choice == 0:
		if player.level >= 2:
			append_spell('Immolate')
		else:
			message('You are too inexperienced to memorize this spell.', libtcod.yellow)
	elif choice == 1:
		if player.level >= 4:
			append_spell('Divination of Warmth')
		else:
			message('You are too inexperienced to memorize this spell.', libtcod.yellow)
	elif choice == 2:
		if player.level >= 6:
			append_spell('Fire Blast')
		else:
			message('You are too inexperienced to memorize this spell.', libtcod.yellow)
	elif choice == 3:
		if player.level >= 8:
			append_spell('White Light'
				)
		else:
			message('You are too inexperienced to memorize this spell.', libtcod.yellow)

def learn_spell_transm():
	global spellbook

	render_all()

	libtcod.console_flush()

	choice = None

	while choice == None:
		choice = menu('Book of Transmutations\n\nYou may memorize one of the following spells:\n\n',
		['Beastly Talons',
		'Stone Skin', 
		'Unholy Rage',
		'Bear Form',
		'Felid Form'], LEVEL_SCREEN_WIDTH)

	if choice == 0:
		append_spell('Beastly Talons')
	elif choice == 1:
		append_spell('Stone Skin')
	elif choice == 2:
		append_spell('Unholy Rage')
	elif choice == 3:
		append_spell('Bear Form')
	elif choice == 4:
		append_spell('Felid Form')

def learn_spell_hex():
	global spellbook

	render_all()

	libtcod.console_flush()

	choice = None

	while choice == None:
		choice = menu('Book of Hexes\n\nYou may memorize one of the following spells:\n\n',
		['Hibernation',
		'Ritual of Pacing',
		'Hex of Radiance', ], LEVEL_SCREEN_WIDTH)

	if choice == 0:
		append_spell('Hibernation')
	elif choice == 1:
		append_spell('Ritual of Pacing')
	elif choice == 2:
		append_spell('Hex of Radiance')

def learn_spell_assorted():
	global spellbook

	render_all()
	libtcod.console_flush()

	choice = None

	while choice == None:
		choice = menu('Gustor\'s lost magicbook\n\nYou may memorize one of the following spells:\n\n',
			['Conjure Food\t (no requirement)',
			'Magic Dart\t (no requirement)',
			'Chain Lightning\t (requires lvl 5)',
			'Lesser Heal\t (requires lvl 3)',
			'Shield Block\t (requires lvl 4)'], LEVEL_SCREEN_WIDTH)

		if choice == 0:
			append_spell('Conjure Food')
		elif choice == 1:
			append_spell('Magic Dart')
		elif choice == 2:
			if player.level >= 5:
				append_spell('Chain Lightning')
			else:
				message('You are too inexperienced to memorize this spell.', libtcod.yellow)
		elif choice == 3:
			if player.level >= 3:
				append_spell('Lesser Heal')
			else:
				message('You are too inexperienced to memorize this spell.', libtcod.yellow)
		elif choice == 4:
			if player.level >= 4:
				append_spell('Shield Block')
			else:
				message('You are too inexperienced to memorize this spell.', libtcod.yellow)




def append_spell(name):
	global spellbook

	spell = None

	#Conjurations
	if name == 'Magic Dart':
		spell = Spell('Magic Dart', 2, cast_magic_dart, 'Conjurations', 1)
	elif name == 'Ice Barrier':
		spell = Spell('Ice Barrier', 3, cast_ice_barrier, 'Conjurations', 3)
	elif name == 'Rain of Ice':
		spell = Spell('Rain of Ice', 6, cast_rain_of_ice, 'Conjurations', 6)
	elif name == 'Chain Lightning':
		spell = Spell('Chain Lightning', 5, cast_chain_lightning, 'Conjurations', 5)
	elif name == 'Fire Blast':
		spell = Spell('Fire Blast', 7, cast_fire_blast, 'Conjurations', 7)
	elif name == 'Conjure Food':
		spell = Spell('Conjure Food', 3, cast_conjure_food, 'Conjurations', 2)
	elif name == 'Bolt of Ice':
		spell = Spell('Bolt of Ice', 3, cast_bolt_of_ice, 'Conjurations', 3)
	elif name == 'Immolate':
		spell = Spell('Immolate', 2, cast_immolate, 'Conjurations', 2)
	elif name == 'Divination of Warmth':
		spell = Spell('Divination of Warmth', 4, cast_divination_of_warmth, 'Conjurations', 1)
	elif name == 'White Light':
		spell = Spell('White Light', 8, cast_white_light, 'Conjurations', 7)
	elif name == 'Summon Ice Beast':
		spell = Spell('Summon Ice Beast', 8, summon_ice_beast, 'Conjurations', 8)

	#Transmutations
	elif name == 'Beastly Talons':
		spell = Spell('Beastly Talons', 3, cast_beastly_talons, 'Transmutations', 1)
	elif name == 'Felid Form':
		spell = Spell('Felid Form', 5, cast_felid_form, 'Transmutations', 4)
	elif name == 'Bear Form':
		spell = Spell('Bear Form', 5, cast_bear_form, 'Transmutations', 5)
	elif name == 'Stone Skin':
		spell = Spell('Stone Skin', 2, cast_stone_skin, 'Transmutations', 2)
	elif name == 'Unholy Rage':
		spell = Spell('Unholy Rage', 3, cast_unholy_rage, 'Transmutations', 3)

	#Hexes
	elif name == 'Hex of Radiance':
		spell = Spell('Hex Of Radiance', 5, cast_hex_of_radiance, 'Hexes', 5)
	elif name == 'Hibernation':
		spell = Spell('Hibernation', 2, cast_hibernation, 'Hexes', 1)
	elif name == 'Ritual of Pacing':
		spell = Spell('Ritual of Pacing', 2, cast_ritual_of_pacing, 'Hexes', 2)
	elif name == 'Spectral Gushes':
		spell = Spell('Spectral Gushes', 5, cast_spectral_gushes, 'Hexes', 3)

	#Race&Class specific
	elif name == 'Stealth':
		spell = Spell('Stealth', 2, cast_stealth, None, 2)
	elif name == 'Shield Block':
		spell = Spell('Shield Block', 3, cast_shield_block, None, 1)
	#Other
	elif name == 'Life Tap':
		spell = Spell('Life Tap', 0, cast_life_tap, None, 1)		
	elif name == 'Lesser Heal':
		spell = Spell('Lesser Heal', 3, cast_lesser_heal, None, 2)

	if spell != None:
		if spell not in spellbook:
			spellbook.append(spell)
			message('You have learned a new spell!', libtcod.light_green)
	else:
		message('You have already learned this spell')
		return 'cancelled'

#---MAIN LOOP AND INITIALIZATION---#

libtcod.console_set_custom_font('TiledFont4.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD, 32, 10)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'The Game', False, libtcod.RENDERER_SDL)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
libtcod.sys_set_fps(LIMIT_FPS)

panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)

mouse = libtcod.Mouse()
key = libtcod.Key()
load_customfont()
main_menu()



