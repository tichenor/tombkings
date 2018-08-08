

class Inventory:

    def __init__(self):
        self.max_length = 26
        self.items = []

    def get_all_equipped(self):
        equipped_list = []
        for item in self.items:
            if item.equipment and item.equipment.is_equipped:
                equipped_list.append(item.equipment)
        return equipped_list

    def get_equipped_in_slot(self, slot):
        for item in self.items:
            if item.equipment and item.equipment.slot == slot and item.equipment.is_equipped:
                return item.equipment
        return None
