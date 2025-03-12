from characters.character import Character

class Player(Character):
    def __init__(self, name, stats, race):
        super().__init__(name, stats, race)