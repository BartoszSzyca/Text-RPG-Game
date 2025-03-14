from .character import Character


class Player(Character):
    def __init__(self, name, stats, race):
        super().__init__(name, stats, race)
        self.inventory = []

    def add_item(self, item):
        self.inventory.append(item)
        print(f"{self.name} dodaje {item.name} do ekwipunku.")

    def __str__(self):
        return super().__str__() + f" Ekwipunek: {', '.join(
            [item.name for item in self.inventory])}"
