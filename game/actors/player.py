from .character import Character
from races import Race
from game.definitions.profession import Profession

class Player(Character):
    """
    Klasa reprezentująca postać gracza. Dziedziczy po Character, dodając
    specyficzne dla gracza mechaniki, takie jak złoto, postęp zadań,
    i obsługa interakcji z użytkownikiem.
    """
    def __init__(self, name: str, race_obj: Race, profession_obj: Profession):
        """
        Inicjalizuje nową postać gracza.

        Args:
            name (str): Nazwa gracza.
            race_obj (Race): Obiekt rasy wybranej przez gracza.
            profession_obj (Profession): Obiekt profesji wybranej przez gracza.
            initial_location (str/Location object): Początkowa lokacja gracza.
        """
        super().__init__(
            name=name,
            description=f"Postać gracza: {name}",
            race_obj=race_obj,
            profession_obj=profession_obj,
        )
        # Specyficzne atrybuty dla gracza
        # self.gold = 0            # Waluta gracza
        # self.quests = {}         # Aktywne zadania (np. {quest_id: quest_status})
        # self.dialog_history = [] # Historia przeprowadzonych dialogów

    # def add_gold(self, amount: int):
    #     """Dodaje złoto do inwentarza gracza."""
    #     if amount > 0:
    #         self.gold += amount
    #         print(f"{self.name} zdobywa {amount} złota. Obecnie ma {self.gold} złota.")
    #     else:
    #         print("Nie można dodać ujemnej ilości złota.")
    #
    # def spend_gold(self, amount: int) -> bool:
    #     """Odejmuje złoto od gracza, jeśli ma wystarczającą ilość. Zwraca True/False."""
    #     if self.gold >= amount:
    #         self.gold -= amount
    #         print(f"{self.name} wydaje {amount} złota. Zostało mu {self.gold} złota.")
    #         return True
    #     else:
    #         print(f"{self.name} nie ma wystarczającej ilości złota (potrzeba {amount}, ma {self.gold}).")
    #         return False

    def show_inventory(self):
        if not self.inventory:
            print("Nie masz żadnych przedmiotów w ekwipunku.")
            return

        print("Ekwipunek:")
        for i, item in enumerate(self.inventory):
            print(f"{i + 1}. {item.name} - {item.description}")

    def add_item(self, item):
        """Dodaje przedmiot do ekwipunku gracza."""
        self.inventory.append(item)
        print(f"{self.name} dodaje {item} do ekwipunku.")
        # print(f"{self.name} dodaje {item.name} do ekwipunku.")

    def heal(self, amount):
        super().heal(amount)
        print(f"{self.name} leczy się o {amount} punktów zdrowia.Aktualne zdrowie: {self.health}")

    def on_death(self):
        """
        Nadpisuje metodę on_death z Entity/Character.
        Logika specyficzna dla śmierci gracza (np. Game Over, powrót do ostatniego zapisu).
        """
        print(f"\n!!! {self.name} umarł! Koniec Gry. !!!")
        # Tutaj dodać logikę zakończenia gry, np.
        input("Naciśnij Enter, aby kontynuować do ekranu głównego...")
        # sys.exit() # zakończyć program po śmierci?

    # def equip_item(self, item):
    #     # Logika wyposażania przedmiotu
    #     # print(f"{self.name} wyposażył {item["name"]}.")
    #     print(f"{self.name} wyposażył {item.name}.")
    #     self.equipment[item.slot] = item
    #     self.inventory.remove(item)

    # def save_game(self):
    #     """Zapisuje bieżący stan gry dla gracza."""
    #     # W przyszłości: Wywołaj system zapisu gry z game/core/game_state.py
    #     print(f"Zapisywanie gry dla gracza {self.name}...")
    #     # game_state.save_player_data(self) # Przykładowe wywołanie
    #     print("Gra zapisana.")
    #
    # def load_game(self):
    #     """Wczytuje stan gry dla gracza."""
    #     # W przyszłości: Wywołaj system wczytywania gry z game/core/game_state.py
    #     print(f"Wczytywanie gry dla gracza {self.name}...")
    #     # loaded_data = game_state.load_player_data() # Przykładowe wywołanie
    #     # self._apply_loaded_data(loaded_data) # Metoda do zastosowania wczytanych danych
    #     print("Gra wczytana.")
    #
    # def handle_input(self, command: str):
    #     """
    #     Przetwarza komendy tekstowe wprowadzane przez gracza.
    #     To będzie główne miejsce interakcji.
    #     """
    #     command = command.lower().strip() # Normalizacja komendy
    #
    #     if command == "status":
    #         print(self.get_info())
    #     elif command.startswith("idz do "):
    #         location_name = command[7:].strip()
    #         print(f"Próbujesz iść do {location_name}...")
    #         # Tutaj będzie integracja z systemem mapy i lokacji
    #         # self.move_to(location_name) # Wywołanie metody z Entity
    #     elif command == "inwentarz":
    #         if self.inventory:
    #             print("Twój inwentarz:")
    #             for item in self.inventory:
    #                 print(f"- {item.name} ({item.item_type})")
    #         else:
    #             print("Twój inwentarz jest pusty.")
    #     elif command == "ekwipunek":
    #         print("Twój ekwipunek:")
    #         for slot, item in self.equipment.items():
    #             print(f"- {slot.replace('_', ' ').title()}: {item.name if item else 'Pusto'}")
    #     # Możesz dodać więcej komend: atakuj, użyj, porozmawiaj itp.
    #     else:
    #         print("Nieznana komenda. Spróbuj 'status', 'inwentarz', 'ekwipunek' lub 'idz do [nazwa lokacji]'.")
    #
    #
    # def get_info(self):
    #     """
    #     Nadpisuje metodę get_info z Character, dodając specyficzne dla gracza dane.
    #     """
    #     info = super().get_info() # Pobiera wszystkie szczegóły z Character
    #     info += f"\n  Złoto: {self.gold}\n"
    #     info += f"  Aktywne zadania: {list(self.quests.keys()) if self.quests else 'Brak'}"
    #     return info

    def __str__(self):
        return super().__str__() + f" Ekwipunek: {', '.join(
            [item.name for item in self.inventory])}"
