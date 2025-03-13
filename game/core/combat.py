def initiate_combat(player, monster):
    print("Rozpoczyna się walka!")
    while player.is_alive() and monster.is_alive():
        player.attack(monster)
        if monster.is_alive():
            monster.attack(player)

def calculate_damage(attacker, defender):
    return attacker.attack_power - defender.attributes.health