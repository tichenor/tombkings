from abc import ABC, abstractmethod


class MonsterAi(ABC):

    def __init__(self):

        self.owner = None

    @abstractmethod
    def take_turn(self):
        pass
