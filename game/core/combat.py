def initiate_combat(player, monster):
    player.attack(monster)
    if monster.is_alive():
        monster.attack(player)


def calculate_damage(attacker, defender):
    return attacker.attack_power - defender.attributes.health
