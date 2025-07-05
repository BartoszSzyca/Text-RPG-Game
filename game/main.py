from core import GameManager
from core import menu
from core import scenes


def main():
    menu.new_game = scenes.new_game
    menu.show_menu()
    # game = GameManager()
    # game.start_game()


if __name__ == "__main__":
    from game.characters import Character
    from .race import Race
    from .warrior import Warrior

    print("--- Testowanie HumanRace ---")
    human_warrior_test = Character(
        name="Testowy Człowiek",
        race_obj=Race(),
        profession_obj=Warrior(),
        base_strength=5,
        base_agility=5,
        base_endurance=5,
        base_intelligence=5,
        base_wisdom=5
    )
    print(human_warrior_test.get_info())

    print("\n--- Testowanie GoblinRace ---")
    goblin_scout_test = Character(
        name="Testowy Goblin",
        race_obj=Race(),
        profession_obj=Warrior(),
        base_strength=5,
        base_agility=5,
        base_endurance=5,
        base_intelligence=5,
        base_wisdom=5
    )
    print(goblin_scout_test.get_info())

# if __name__ == "__main__":
#     main()
