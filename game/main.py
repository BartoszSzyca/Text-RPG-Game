from characters import Warrior
from monsters import Goblin
from core import initiate_combat
from locations import Forest


def main():
    player = Warrior("Aragorn")
    goblin = Goblin("Goblin")
    location = Forest()

    print(f"Witaj w {location.name}!")
    print(f"Spotykasz {goblin.name}!")

    initiate_combat(player, goblin)

    if player.is_alive():
        print(f"{player.name} zwycięża!")
    else:
        print(f"{player.name} poległ.")


if __name__ == "__main__":
    main()
