from races import Race
from characters import Stats


class GoblinRace(Race):
    def __init__(self):
        base_stats = Stats(-2, 2, -1)
        super().__init__("Goblin", base_stats)
