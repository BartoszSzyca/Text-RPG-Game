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

    while player.is_alive() and goblin.is_alive():
        action = input("Co robisz? (Atak/Ucieczka): ").lower()
        if action == "atak":
            initiate_combat(player, goblin)
        elif action == "ucieczka":
            print("Uciekasz z pola walki.")
            break
        else:
            print("Nieznana akcja.")

    if player.is_alive():
        print(f"{player.name} zwycięża!")
    else:
        print(f"{player.name} poległ.")


if __name__ == "__main__":
    main()
