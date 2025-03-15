from .character import Character


class Player(Character):
    def __init__(self, name, stats, race):
        super().__init__(name, stats, race)
        self.inventory = []

    def show_inventory(self):
        if not self.inventory:
            print("Nie masz żadnych przedmiotów w ekwipunku.")
            return

        print("Ekwipunek:")
        for i, item in enumerate(self.inventory):
            print(f"{i + 1}. {item.name} - {item.description}")

    def add_item(self, item):
        self.inventory.append(item)
        print(f"{self.name} dodaje {item.name} do ekwipunku.")

    def __str__(self):
        return super().__str__() + f" Ekwipunek: {', '.join(
            [item.name for item in self.inventory])}"
