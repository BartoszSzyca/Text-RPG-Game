def initiate_combat(player, monster):
    player.attack(monster)
    if monster.is_alive():
        monster.attack(player)


def calculate_damage(attacker, defender):
    return attacker.attack_power - defender.attributes.health


def handle_player_turn(game_manager):
    player = game_manager.player
    goblin = game_manager.goblin
    while player.is_alive() and goblin.is_alive():
        action = input(
            "Co robisz? (Atak/Rozmawiaj/Ekwipunek/Ucieczka): ").lower()
        if action == "atak":
            initiate_combat(player, goblin)
        elif action == "rozmawiaj":
            for npc in game_manager.location.get_npcs():
                npc.talk()
        elif action == "ekwipunek":
            player.show_inventory()
            choice = int(input("Wybierz numer przedmiotu: ")) - 1
            item = player.inventory[choice]
            if item:
                game_manager.use_item(choice)
            else:
                print("Nie ma takiego przedmiotu.")
        elif action == "ucieczka":
            print(
                f"{player.name} ucieka przed {goblin.name}!")
            break
        else:
            print("Nieznana komenda.")

    if player.is_alive() and not goblin.is_alive():
        print(f"{player.name} zwycięża!")
        goblin.heal(50)
    else:
        print(f"{player.name} poległ.")
