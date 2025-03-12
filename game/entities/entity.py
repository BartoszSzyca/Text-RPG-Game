class Entity:
    def __init__(self, name):
        self.name = name
        self.health = 100  # Domyślna wartość zdrowia
        self.attack_power = 10 # Domyślna siła ataku

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        print(f"{self.name} otrzymuje {damage} obrażeń. Pozostałe zdrowie: {self.health}")

    def attack(self, target):
        print(f"{self.name} atakuje {target.name}!")
        target.take_damage(self.attack_power)

    def is_alive(self):
        return self.health > 0

    def __str__(self):
        return f"{self.name} (Health: {self.health}, Attack: {self.attack_power})"