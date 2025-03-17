from utils.helpers import load_json
import random


class Entity:
    def __init__(self, name, stats ,health=100):
        self.name = name
        self.current_health = health
        self.max_health = health
        self.stats = stats

        self.inventory = []
        self.equipment = Equipment()

    # def take_damage(self, damage):
    #     self.health -= damage
    #     if self.health < 0:
    #         self.health = 0
    #     print(f"{self.name} otrzymuje {damage} obrażeń. Pozostałe zdrowie: "
    #           f"{self.health}")
    #
    # def attack(self, target):
    #     print(f"{self.name} atakuje {target.name}!")
    #     target.take_damage(self.attack_power)

    def heal(self, amount):
        self.current_health += amount

    def is_alive(self):
        return self.current_health > 0

    def __str__(self):
        return (f"{self.name} (Health: {self.current_health}")
                # f", Attack: {self.attack_power})")


class Player:
    def __init__(self, stats, name="Aragorn"):
        self.name = name
        self.current_health = 100
        self.max_health = 100
        self.stats = stats

        self.inventory = []
        self.equipment = Equipment()

    def __str__(self):
        return (f"Gracz {self.name}:\n\t"
                f"Życie: {self.current_health}/{self.max_health}")

    def attack(self):
        item_in_right_hand = self.equipment.get_equipped_item("right_hand")
        return self.stats.calculate_attack_power(item_in_right_hand)

    def show_inventory(self):
        print("Ekwipunek:")
        if not self.inventory:
            print("Nie masz żadnych przedmiotów w ekwipunku.")
            return None

        for i, item in enumerate(self.inventory):
            print(f"{i + 1}. {item.name} - {item.description}")
        return True

    def add_item(self, item):
        """Dodaje przedmiot do ekwipunku gracza."""
        self.inventory.append(item)
        print(f"{self.name} dodaje {item.name} do ekwipunku.")

    def heal(self, amount):
        """Leczy gracza o podaną ilość punktów zdrowia."""
        self.current_health = min(self.max_health, self.current_health + amount)
        print(f"{self.name} uleczony o {amount} punktów zdrowia. "
              f"Aktualne zdrowie: {self.current_health}")

    def equip(self, item, slot):
        self.equipment.equip_item(item, slot)

    def unequip(self, slot):
        self.equipment.unequip_item(slot)

    def get_equipped(self, slot):
        self.equipment.get_equipped_item(slot)


class Monster:
    def __init__(self, data):
        self.name = data["name"]
        self.current_health = data["health"]
        self.max_health = data["health"]
        self.attack_power = data["attack_power"]

    def __str__(self):
        return (f"Potwór {self.name}:\n\t"
                f"Życie: {self.current_health}/{self.max_health}")


class Stats:
    def __init__(self, data):
        self.strength = data.get("strength", 1)
        self.endurance = data.get("endurance", 1)
        self.agility = data.get("agility", 1)
        self.intelligence = data.get("intelligence", 1)

        self.attack_power = self.calculate_attack_power()
        self.fatigue = 0

    def calculate_attack_power(self, item=None):
        """
        Oblicza moc ataku na podstawie siły i opcjonalnego bonusu z przedmiotu.
        """
        base_attack = self.strength * 2

        if item:
            item_bonus = item.attack_bonus
            attack_power = base_attack * (1 + item_bonus / 10)
        else:
            attack_power = base_attack

        return attack_power

    # def equip_item(self, item):
    #     self.item = item
    #
    # def unequip_item(self):
    #     self.item = None

    def increase_fatigue(self, amount):
        self.fatigue += amount - self.endurance * 0.1
        if self.fatigue < 0:
            self.fatigue = 0


class Item:
    def __init__(self, data):
        self.name = data["name"]
        self.description = data["description"]
        self.value = data["value"]
        self.attack_bonus = data.get("attack_bonus", 0)
        self.defense_bonus = data.get("defense_bonus", 0)
        self.health_bonus = data.get("health_bonus", 0)

    def __str__(self):
        return f"{self.name} - {self.description} (Wartość: {self.value})"


class Equipment:
    def __init__(self):
        self.slots = {
            "head": None,
            "torso": None,
            "left_hand": None,
            "right_hand": None,
            "legs": None,
            "feet": None,
        }

    def equip_item(self, item, slot):
        if slot in self.slots:
            self.slots[slot] = item
        else:
            print(f"Nieprawidłowy slot: {slot}")

    def unequip_item(self, slot):
        if slot in self.slots:
            self.slots[slot] = None
        else:
            print(f"Nieprawidłowy slot: {slot}")

    def get_equipped_item(self, slot):
        if slot in self.slots:
            return self.slots[slot]
        else:
            print(f"Nieprawidłowy slot: {slot}")
            return None


class Combat:
    def attack(self, attacker, defender):
        defender.current_health -= attacker.attack()
        if defender.current_health > 0:
            attacker.current_health -= defender.attack_power
        return

    def calculate_dodge_chance(self, agility):
        return agility * 0.01

    def fight(self, player, monster):
        action = None
        print(f"Rozpoczołeś walke przeciwko {monster.name}!")
        while (action != "koniec" and player.current_health > 0 and
               monster.current_health > 0):
            print(player)
            print(monster)
            action = game.user_choice()
            if action == "atak":
                self.attack(player, monster)
            elif action == "ekwipunek":
                if player.show_inventory():
                    user_choice = int(
                        input("Wybierz przedmiot z ekwipunku (Numer): "))
                    game.use_item(user_choice - 1)
            elif action == "ucieczka":
                print(f"Cudem udało ci się uciec przed {monster.name}")
                break

        if (player.current_health > 0 and action != "ucieczka" and
                action != "koniec"):
            print("Zwyciężyłeś")
        elif (monster.current_health > 0 and action != "ucieczka" and
              action != "koniec"):
            print("Przegrałeś.")


class Location:
    pass


class Move:
    pass


class GameManager:
    def __init__(self):
        player_stats = {"strength": 5}
        self.stats = Stats(player_stats)
        self.player = None
        self.items = [Item(item) for item in load_json(Item)]
        self.combat = Combat()
        self.monsters = self.generate_monster_list()
        self.action = None

    def user_choice(self):
        return input("Co robisz? (Atak/Rozmawiaj/Ekwipunek/Ucieczka): ").lower()

    def start_game(self):
        print("Witaj w grze tekstowej RPG.")
        name = input("Podaj swoje imię poszukiwaczu.\n"
                     "Imię: ")
        self.player = Player(self.stats, name)
        while self.action != "koniec" and self.player.current_health > 0:
            self.generate_encounter()
        print("Koniec gry!")

    def generate_monster_count(self, a=1, b=5):
        """
        Generuje losową liczbę potworów z przedziału [a, b].

        Args:
            a (int): Dolna granica przedziału (włącznie).
            b (int): Górna granica przedziału (włącznie).

        Returns:
            int: Losowa liczba potworów.
        """
        return random.randint(a, b)

    def select_monster_types(self, monster_count):
        """
        Wybiera losowe typy potworów z dostępnej listy.

        Args:
            monster_count (int): Liczba potworów do wybrania.

        Returns:
            list[Monster]: Lista instancji potworów wybranych losowo.
        """
        all_monsters = load_json(Monster)
        return random.sample(all_monsters, monster_count)

    def generate_monster_list(self):
        """
        Generuje listę instancji potworów na podstawie losowo wybranych typów i
        liczby.

        Returns:
            list[Monster]: Lista instancji potworów.
        """
        monster_count = self.generate_monster_count()
        selected_monsters = self.select_monster_types(monster_count)
        monsters = random.choices(selected_monsters, k=monster_count)
        return [Monster(monster) for monster in monsters]

    def get_item(self, item_name):
        for item in self.items:
            if item.name.lower() == item_name.lower():
                return item
        return None

    def find_item(self):
        if self.items:
            item = random.choice(self.items)
            print(f"Znajdujesz {item.name}!")
            self.player.add_item(item)

    def use_item(self, choice):
        try:
            selected_item = self.player.inventory[choice]
            if selected_item.health_bonus > 0:
                print(f"Używasz {selected_item.name}.")
                self.player.heal(selected_item.health_bonus)
                self.player.inventory.pop(choice)
            else:
                self.player.equip(selected_item, "right_hand")
                print(f"Ubrałeś: {selected_item.name}")
        except (ValueError, IndexError):
            print("Nieprawidłowy wybór.")

    def generate_encounter(self):
        encounter_chance = random.randint(1, 10)
        if encounter_chance <= 6:
            self.encounter_monster()
        elif 7 <= encounter_chance <= 8:
            self.find_item()
        elif 8 <= encounter_chance <= 9:
            print("Słyszysz tylko szum wiatru.")
        else:
            print("Coś jest w pobliżu")

    def encounter_monster(self):
        for i, monster in enumerate(self.monsters):
            print(f"Potwór {i + 1}/{len(self.monsters)}: {monster.name}")
            self.combat.fight(self.player, monster)


if __name__ == "__main__":
    game = GameManager()
    game.start_game()
