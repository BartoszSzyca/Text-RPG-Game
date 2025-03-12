from characters import Warrior
from monsters import Goblin


def initiate_combat(player, monster):
    print("Rozpoczyna się walka!")
    while player.is_alive() and monster.is_alive():
        player.attack(monster)
        if monster.is_alive():
            monster.attack(player)


def main():
    player = Warrior("Aragorn")
    goblin = Goblin("Goblin")

    print(f"Spotykasz {goblin.name}!")

    initiate_combat(player, goblin)

    if player.is_alive():
        print(f"{player.name} zwycięża!")
    else:
        print(f"{player.name} poległ.")


if __name__ == "__main__":
    main()
