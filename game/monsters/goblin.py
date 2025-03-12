from monsters import Monster
from races import GoblinRace


class Goblin(Monster):
    def __init__(self, name):
        race = GoblinRace()
        super().__init__(name, 50, 5)
        self.race = race
