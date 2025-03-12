from characters import Player, Stats
from races import Human


class Warrior(Player):
    def __init__(self, name):
        race = Human()
        stats = Stats(10, 5, 8)
        super().__init__(name, stats, race)
