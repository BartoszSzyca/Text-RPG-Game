import json
from characters import Warrior, NPC
from monsters import Goblin
from locations import Forest
from .combat import initiate_combat
from items import Item


class GameManager:
    def __init__(self):
        self.load_config()
        self.player = Warrior(self.config["player_name"])
        self.goblin = Goblin(self.config["enemy_name"])
        self.location = Forest()
        self.load_items()
        self.npc = NPC("Stary Mędrzec", "Witaj, podróżniku!")
        self.location.add_npc(self.npc)

    def load_config(self):
        with open("data/config.json", "r") as f:
            self.config = json.load(f)

    def load_items(self):
        with open("data/items.json", "r", encoding="utf-8") as f:
            items_data = json.load(f)
            self.items = [Item(**item) for item in items_data]

    def start_game(self):
        print(f"Witaj w {self.location.name}!")
        print(f"Napotkałeś {self.goblin.name}!")
        print(f"Spotykasz {self.npc.name}.")

        item_name = "Mikstura życia"
        item = self.get_item(item_name)
        self.player.add_item(item)

        while self.player.is_alive() and self.goblin.is_alive():
            action = input(
                "Co robisz? (Atak/Rozmawiaj/Ekwipunek/Ucieczka): ").lower()
            if action == "atak":
                self.handle_combat()
            elif action == "rozmawiaj":
                for npc in self.location.get_npcs():
                    npc.talk()
            elif action == "ekwipunek":
                self.player.show_inventory()
                choice = int(input("Wybierz numer przedmiotu: ")) - 1
                item = self.player.inventory[choice]
                if item:
                    self.use_item(choice)
                else:
                    print("Nie ma takiego przedmiotu.")
            elif action == "ucieczka":
                print(f"{self.player.name} ucieka przed {self.goblin.name}!")
                break
            else:
                print("Nieznana komenda.")

        if self.player.is_alive():
            print(f"{self.player.name} zwycięża!")
        else:
            print(f"{self.player.name} poległ.")

    def use_item(self, choice):
        try:
            selected_item = self.player.inventory[choice]
            if selected_item.health_bonus > 0:
                print(f"Używasz {selected_item.name}.")
                self.player.heal(selected_item.health_bonus)
                self.player.inventory.pop(choice)
        except (ValueError, IndexError):
            print("Nieprawidłowy wybór.")

    def handle_combat(self):
        initiate_combat(self.player, self.goblin)

    def get_item(self, item_name):
        for item in self.items:
            if item.name.lower() == item_name.lower():
                return item
        return None
