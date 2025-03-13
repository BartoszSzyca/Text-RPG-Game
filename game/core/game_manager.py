from characters.warrior import Warrior
from monsters.goblin import Goblin
from locations.forest import Forest
from core.combat import initiate_combat

class GameManager:
    def __init__(self):
        self.player = Warrior("Aragorn")
        self.goblin = Goblin("Goblin")
        self.location = Forest()

    def start_game(self):
        print(f"Witaj w {self.location.name}!")
        print(f"Spotykasz {self.goblin.name}!")

        self.handle_combat()

        if self.player.is_alive():
            print(f"{self.player.name} zwycięża!")
        else:
            print(f"{self.player.name} poległ.")

    def handle_combat(self):
        initiate_combat(self.player, self.goblin)