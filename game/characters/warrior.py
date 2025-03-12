from characters.player import Player
from characters.character import Stats
from races.human import Human

class Warrior(Player):
    def __init__(self, name):
        race = Human()
        stats = Stats(10, 5, 8)
        super().__init__(name, stats, race)