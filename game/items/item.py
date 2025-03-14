class Item:
    def __init__(self, name, description, value, attack_bonus=0, defense_bonus=0, health_bonus=0):
        self.name = name
        self.description = description
        self.value = value
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.health_bonus = health_bonus

    def __str__(self):
        return f"{self.name} - {self.description} (Wartość: {self.value})"