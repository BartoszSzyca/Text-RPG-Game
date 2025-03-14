from entities import Entity


class Stats:
    def __init__(self, strength, agility, endurance):
        self.strength = strength
        self.agility = agility
        self.endurance = endurance


class Attributes:
    def __init__(self, health, attack_power, dodge_chance):
        self.health = health
        self.attack_power = attack_power
        self.dodge_chance = dodge_chance


class Character(Entity):
    def __init__(self, name, stats, race):
        super().__init__(name)
        self.stats = stats
        self.race = race
        self.attributes = self.calculate_attributes()

    def calculate_attributes(self):
        health = 100 + self.stats.endurance * 10
        attack_power = self.stats.strength * 5
        dodge_chance = self.stats.agility * 0.1
        return Attributes(health, attack_power, dodge_chance)

    def __str__(self):
        return (f"{self.name} (Health: {self.attributes.health}, "
                f"Attack: {self.attributes.attack_power}, "
                f"Dodge: {self.attributes.dodge_chance})")
