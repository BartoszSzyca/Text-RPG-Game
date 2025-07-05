from .entity import Entity
from races import Race
from game.definitions.profession import Profession
from items import Item
from items.item import Weapon
# import uuid

reka = Weapon(
    "Pusta ręka",
    "Nic w niej nie trzymasz.",
    damage=0,
    slot="main_hand",
)


class Stats:
    def __init__(self, strength=1, agility=1, endurance=1):
        self.strength = strength
        self.agility = agility
        self.endurance = endurance


class Attributes:
    def __init__(self, health=100, attack_power=10, dodge_chance=1):
        self.health = health
        self.attack_power = attack_power
        self.dodge_chance = dodge_chance


class Character(Entity):
    """
    Klasa bazowa dla wszystkich 'żywych' i interaktywnych bytów w grze,
    takich jak Gracz, Potwory i NPC. Dziedziczy po Entity i dodaje
    mechaniki statystyk, rasy, profesji, ekwipunku i umiejętności.
    """
    def __init__(self, name="_", description=None, max_health=100,
                 race_obj: Race = None, profession_obj: Profession = None,
                 base_strength=1, base_agility=1, base_endurance=1,
                 base_intelligence=1, base_wisdom=1):
        """
        Inicjalizuje nową postać.

        Args:
            name (str): Nazwa postaci.
            description (str): Opis postaci.
            max_health (int): Maksymalne bazowe HP postaci.
            race_obj (Race): Obiekt rasy (np. Human(), Goblin()).
            profession_obj (Profession): Obiekt profesji (np. Warrior(), Mage()).
            base_strength (int): Bazowa siła przed bonusami.
            base_agility (int): Bazowa zręczność przed bonusami.
            base_endurance (int): Bazowa wytrzymałość przed bonusami.
            base_intelligence (int): Bazowa inteligencja przed bonusami.
            base_wisdom (int): Bazowa mądrość przed bonusami.
        """
        super().__init__(name, description, max_health)

        stats = Stats()
        attributes = Attributes()

        self.race = race_obj
        self.profession = profession_obj

        # Bazowe statystyki główne (surowe punkty)
        self.base_strength = base_strength
        self.base_agility = base_agility
        self.base_endurance = base_endurance
        self.base_intelligence = base_intelligence
        self.base_wisdom = base_wisdom
        self.base_max_health = max_health

        # Efektywne statystyki (obliczane po zastosowaniu bonusów)
        # Te statystyki będą używane w obliczeniach w grze.
        self.strength = 0
        self.agility = 0
        self.endurance = 0
        self.intelligence = 0
        self.wisdom = 0

        # Wyprowadzane atrybuty (obliczane na podstawie efektywnych statystyk)
        self.attack_power = 0
        self.dodge_chance = 0.0  # Szansa na unik jako float (np. 0.05 dla 5%)
        self.carry_capacity = 0  # Np. udźwig

        self.inventory = []
        self.equipment = {
            "head": None,
            "chest": None,
            "hands": None,
            "legs": None,
            "feet": None,
            "main_hand": None,
            "off_hand": None,
            "ring1": None,
            "ring2": None,
            "amulet": None
        }

        self._total_hp_percent_modifier = 0.0
        # Umiejętności i zdolności
        # self.abilities = []
        # self.level = 1
        # self.experience = 0

        # Wywołanie metod do inicjalizacji statystyk i atrybutów po wszystkich ustawieniach
        self._recalculate_stats_and_attributes()
        self.health = self.max_health

    def _recalculate_stats_and_attributes(self):
        """
        Oblicza efektywne statystyki i wyprowadzane atrybuty postaci
        na podstawie bazowych statystyk, bonusów z rasy, profesji
        oraz wyposażonych przedmiotów. Wywoływane po każdej zmianie ekwipunku,
        awansie na poziom, itp.
        """
        self._race_hp_modifier = 0
        self._profession_hp_modifier = 0
        self._item_hp_modifier = 0 # bonusy HP z przedmiotów
        self._total_hp_percent_modifier = 0.0 # procentowe bonusy

        self.strength = self.base_strength
        self.agility = self.base_agility
        self.endurance = self.base_endurance
        self.intelligence = self.base_intelligence
        self.wisdom = self.base_wisdom

        if self.race:
            for stat, bonus in self.race.stat_bonuses.items():
                if hasattr(self, stat):
                    setattr(self, stat, getattr(self, stat) + bonus)
            self._race_hp_modifier += self.race.stat_bonuses["hp_modifier"]
            # Dodaj umiejętności rasowe
            # self.abilities.extend(self.race.racial_abilities)

        # Dodaj bonusy z profesji
        if self.profession:
            for stat, bonus in self.profession.stat_bonuses.items():
                if hasattr(self, stat):
                    setattr(self, stat, getattr(self, stat) + bonus)
            self._profession_hp_modifier += self.profession.stat_bonuses["hp_modifier"]
            # Dodaj umiejętności profesyjne
            # self.abilities.extend(self.profession.abilities)

        # Dodaj bonusy z wyposażonych przedmiotów
        for slot, item in self.equipment.items():
            if item and item.stat_modifiers: # Item musi mieć atrybut stat_modifiers (z Item klasy)
                for stat, bonus in item.stat_modifiers.items():
                    if hasattr(self, stat):
                        setattr(self, stat, getattr(self, stat) + bonus)
                    # Modyfikatory HP z przedmiotów
                if hasattr(item, 'hp_modifier'):
                    self._item_hp_modifier += item.hp_modifier
                    # Procentowe modyfikatory HP z przedmiotów
                if hasattr(item, 'hp_percent_modifier'):
                    self._total_hp_percent_modifier += item.hp_percent_modifier

        # Oblicz wyprowadzane atrybuty na podstawie finalnych, efektywnych statystyk
        total_base_health = self.base_max_health + self.endurance #+ (self.level * 5) # HP skaluje się z wytrzymałością i poziomem
        total_base_health += self._race_hp_modifier
        total_base_health += self._profession_hp_modifier
        total_base_health += self._item_hp_modifier

        # Zastosuj procentowe modyfikatory do total_base_health
        # np. 1.10 dla +10%, 1.05 dla +5%, razem 1.15 dla +15%
        self.max_health = int(total_base_health * (1 + self._total_hp_percent_modifier))
        self.max_health = max(1, self.max_health)
        # Tutaj dodać inne bonusy z pasywnych atrybutów

        self.attack_power = self.strength * 0.5 #+ self.level # Siła ataku skaluje się z siłą i poziomem
        self.dodge_chance = min(self.agility * 0.005, 0.75) # Szansa na unik (np. 0.5% za zręczność, max 75%)
        self.magic_power = self.intelligence * 2 #+ self.level
        self.carry_capacity = 10 + self.strength * 2 # Udźwig (np. bazowy + z siły)

        # Dodaj attack_power z wyposażonej broni
        # Musimy sprawdzić sloty, w których trzymana jest broń.
        # Założenie: broń główna jest w 'main_hand' lub 'two_hand'.
        equipped_weapon = None
        if self.equipment.get("main_hand") and self.equipment["main_hand"].item_type == "weapon":
            equipped_weapon = self.equipment["main_hand"]
        elif self.equipment.get("two_hand") and self.equipment["two_hand"].item_type == "weapon":
            equipped_weapon = self.equipment["two_hand"]

        if equipped_weapon:
            # Jeśli jest wyposażona broń, dodaj jej attack_power
            self.attack_power += equipped_weapon.damage

        # Upewnij się, że health nie przekracza nowego max_health po przeliczeniu
        self.health = min(self.health, self.max_health)
        # Po zmianie statystyk HP zawsze było pełne:
        # self.health = self.max_health

    def heal(self, amount):
        super().heal(amount)
        print(f"{self.name} leczy się o {amount} punktów zdrowia. "
              f"Aktualne zdrowie: {self.health}")

    def attack(self, target: Entity):
        """Wykonuje atak na inny byt."""
        if not self.is_alive:
            print(f"{self.name} jest martwy i nie może atakować.")
            return

        print(f"{self.name} atakuje {target.name} zadając {self.attack_power} obrażeń!")
        target.take_damage(self.attack_power)

    # def add_item(self, item):
    #     """Dodaje przedmiot do ekwipunku."""
    #     self.inventory.append(item)

    def add_item_to_inventory(self, item: Item):
        """Dodaje przedmiot do inwentarza."""
        self.inventory.append(item)
        print(f"{self.name} dodaje {item.name} do inwentarza.")

    def remove_item_from_inventory(self, item: Item):
        """Usuwa przedmiot z ekwipunku."""
        if item in self.inventory:
            self.inventory.remove(item)
            print(f"{self.name} usuwa {item.name} z inwentarza.")
        else:
            print(f"{self.name} nie ma {item.name} w inwentarzu.")

    def equip_item(self, item: Item):
        """
        Wyposaża przedmiot w odpowiednim slocie.
        Args:
            item (Item): Przedmiot do wyposażenia.
        """
        # Sprawdź, czy przedmiot ma slot i czy slot jest jednym z dostępnych
        if not hasattr(item, 'slot') or item.slot not in self.equipment:
            print(
                f"{item.name} nie może zostać wyposażony lub ma nieprawidłowy slot.")
            return

        target_slot = item.slot

        # Obsługa broni dwuręcznej: jeśli to broń dwuręczna, blokujemy oba sloty dłoni
        if target_slot == "two_hand":
            if self.equipment["main_hand"] is not None:
                self.unequip_item("main_hand")
            if self.equipment["off_hand"] is not None:
                self.unequip_item("off_hand")
        # # Jeśli wyposażamy w główną rękę, upewnij się, że nie ma broni dwuręcznej
        # elif target_slot == "main_hand" and self.equipment[
        #     "two_hand"] is not None:
        #     self.unequip_item("two_hand")
        # # Jeśli wyposażamy w drugą rękę, upewnij się, że nie ma broni dwuręcznej
        # elif target_slot == "off_hand" and self.equipment[
        #     "two_hand"] is not None:
        #     self.unequip_item("two_hand")

        # Jeśli coś już jest w docelowym slocie (i nie jest to broń dwuręczna obsługiwana powyżej)
        if self.equipment[target_slot] is not None:
            self.unequip_item(target_slot)  # Zdejmij stary przedmiot

        # Usuń przedmiot z inwentarza, jeśli tam był
        if item in self.inventory:
            self.inventory.remove(item)

        # Wyposaż przedmiot
        self.equipment[target_slot] = item
        print(f"{self.name} wyposaża: {item.name}.")

        # Przelicz statystyki po zmianie ekwipunku
        self._recalculate_stats_and_attributes()

    def unequip_item(self, slot: str):
        """
        Zdejmuje przedmiot z danego slotu ekwipunku i umieszcza go w inwentarzu.
        Args:
            slot (str): Nazwa slotu, z którego ma być zdjęty przedmiot.
        """
        if slot not in self.equipment or self.equipment[slot] is None:
            print(f"Brak przedmiotu w slocie {slot}.")
            return

        item_to_unequip = self.equipment[slot]
        self.equipment[slot] = None
        self.inventory.append(item_to_unequip)

        print(f"{self.name} zdejmuje: {item_to_unequip.name}.")
        # Po zdjęciu przedmiotu również przelicz statystyki
        self._recalculate_stats_and_attributes()

    # def add_xp(self, amount: int):
    #     """Dodaje punkty doświadczenia do postaci."""
    #     self.experience += amount
    #     print(f"{self.name} zdobywa {amount} PD. Ma {self.experience} PD.")
    #     # Tutaj dodać logikę awansu na poziom, np. self._check_level_up()

    def get_info(self):
        """
        Zwraca szczegółowe informacje o postaci, w tym statystyki, rasę, profesję i ekwipunek.
        """
        info = super().get_info()  # Pobiera podstawowe info z Entity
        info += (f"\n  Typ: Postać\n"
                 # f"  Poziom: {self.level}, PD: {self.experience}\n"
                 f"  Rasa: {self.race.name if self.race else 'Brak'}, "
                 f"Profesja: {self.profession.name if self.profession else 'Brak'}\n"
                 f"\n  --- Statystyki --- \n"
                 f"  Siła: {self.strength} (Bazowa: {self.base_strength})\n"
                 f"  Zręczność: {self.agility} (Bazowa: {self.base_agility})\n"
                 f"  Wytrzymałość: {self.endurance} (Bazowa: {self.base_endurance})\n"
                 f"  Inteligencja: {self.intelligence} (Bazowa: {self.base_intelligence})\n"
                 f"  Mądrość: {self.wisdom} (Bazowa: {self.base_wisdom})\n"
                 f"\n  --- Atrybuty Bojowe --- \n"
                 f"  Maks. HP: {self.max_health}\n"
                 f"  Siła Ataku: {self.attack_power}\n"
                 f"  Szansa na Unik: {self.dodge_chance:.2%}\n"
                 f"  Siła Magii: {self.magic_power}\n"
                 f"  Udźwig: {self.carry_capacity}\n"
                 f"\n  --- Ekwipunek ---\n")

        equipped_items = []
        for slot, item in self.equipment.items():
            equipped_items.append(
                f"  {slot.replace('_', ' ').title()}: {item.name if item else 'Puste'}")
        info += "\n".join(equipped_items)

        info += (
            f"\n\n  --- Inwentarz ({len(self.inventory)} przedmiotów) ---\n"
            f"  {[item.name for item in self.inventory] if self.inventory else 'Pusty'}\n"
            f"\n  --- Umiejętności ---\n")
            # f"  {', '.join(self.abilities) if self.abilities else 'Brak'}")

        return info

    def __str__(self):
        return (f"{self.name} (Health: {self.health}, "
                f"Attack: {self.attack_power}, "
                f"Dodge: {self.dodge_chance})")

