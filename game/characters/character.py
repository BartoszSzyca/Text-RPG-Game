from entities.entity import Entity


class Stats:
    def __init__(self, strength, agility, endurance):
        self.strength = strength
        self.agility = agility
        self.endurance = endurance


class Attributes:
    def __init__(self, health, attack_power):
        self.health = health
        self.attack_power = attack_power


class Character(Entity):
    def __init__(self, name, stats, race):
        super().__init__(name)
        self.stats = stats
        self.race = race
        self.attributes = self.calculate_attributes()

    def calculate_attributes(self):
        health = 100 + self.stats.endurance * 10
        attack_power = self.stats.strength * 5
        return Attributes(health, attack_power)

    def __str__(self):
        return (f"{self.name} (Health: {self.attributes.health}, Attack: "
                f"{self.attributes.attack_power})")
