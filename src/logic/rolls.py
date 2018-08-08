import libtcodpy as libtcod


class Rolls:

    @staticmethod
    def wake_up_roll(entity, entity_other):
        dist = entity.distance_to_entity(entity_other)
        if dist + entity_other.fighter.stealthiness >= 10:
            return False
        if libtcod.random_get_int(0, 0, 100) <= (100 - dist**(2 + 0.1 * entity_other.fighter.stealthiness)):
            return True
        return False


