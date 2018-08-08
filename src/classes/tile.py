

class Tile:

    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked
        self.explored = False
        if block_sight is None: # default is a tile blocks sight if it blocks movement
            block_sight = blocked
        self.block_sight = block_sight
