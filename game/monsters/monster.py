from entities import Entity


class Monster(Entity):
    def __init__(self, name, health, attack_power):
        super().__init__(name)
        self.health = health
        self.attack_power = attack_power

    def die(self):
        print(f"{self.name} umiera!")
