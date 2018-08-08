import libtcodpy as libtcod
from game.action_type import ActionType
from gui.messages import Messages


class EventHandler:

    death_events = []
    combat_events = []
    inventory_events = []
    move_events = []
    entity_events = []

    @staticmethod
    def update():

        for event in EventHandler.combat_events[:]:

            if event.key == ActionType.MELEE_COMBAT or event.key == ActionType.RANGED_COMBAT:
                attacker, target, result = event.value
                Messages.new_combat_msg(event.key, attacker, target, result)

            EventHandler.combat_events.remove(event)

        for event in EventHandler.inventory_events[:]:

            if event.key == ActionType.PICK_UP_GAIN or event.key == ActionType.PICK_UP_FAIL:
                item, player = event.value
                Messages.new_item_msg(event.key, player, item)

            EventHandler.inventory_events.remove(event)

        for event in EventHandler.entity_events[:]:

            if event.key == 'spotted':
                Messages.new('The ' + event.value.name + ' spots you.', libtcod.light_red)

            elif event.key == 'wake_up':
                Messages.new('The ' + event.value.name + ' wakes up.', libtcod.light_gray)

            EventHandler.entity_events.remove(event)

        for event in EventHandler.death_events[:]:

            if event.key == 'death':
                death_function, monster = event.value
                death_function(monster)

            EventHandler.death_events.remove(event)

        EventHandler.move_events = []




    @staticmethod
    def add_combat_event(key, value):
        EventHandler.combat_events.append(Event(key, value))

    @staticmethod
    def add_death_event(key, value):
        EventHandler.death_events.append(Event(key, value))

    @staticmethod
    def add_move_event(key, value):
        EventHandler.move_events.append(Event(key, value))

    @staticmethod
    def add_inventory_event(key, value):
        EventHandler.inventory_events.append(Event(key, value))

    @staticmethod
    def add_entity_event(key, value):
        EventHandler.entity_events.append(Event(key, value))


class Event:

    def __init__(self, key, value):
        self.key = key
        self.value = value
