from races import Race
from characters import Stats


class Human(Race):
    def __init__(self):
        base_stats = Stats(0, 0, 0)
        super().__init__("Human", base_stats)
