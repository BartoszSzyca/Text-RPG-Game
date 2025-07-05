import uuid


class Entity:
    """
    Klasa bazowa dla wszystkich bytów w świecie gry.
    Zawiera podstawowe atrybuty i metody, które są wspólne dla każdego obiektu,
    niezależnie od tego, czy jest to postać, przedmiot, czy element środowiska.
    """

    def __init__(self, name="Nieznany Byt", description=None,
                 max_health=1, weight=1):
        """
        Inicjalizuje nowy byt.

        Args:
            name (str): Nazwa bytu (np. "Goblin", "Miecz", "Kamień").
            description (str): Krótki opis bytu.
            max_health (int): Maksymalne punkty zdrowia bytu. Domyślnie 1.
                              Jeśli byt nie ma mieć HP (np. "czysty" przedmiot),
                              można to później zignorować lub ustawić na 0.
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.max_health = max_health
        self.health = max_health
        self.weight = weight
        self._is_alive = True

    @property
    def is_alive(self):
        """
        Zwraca True, jeśli byt ma więcej niż 0 punktów zdrowia, w przeciwnym razie False.
        Jest to property, więc nie wywołujesz go jak metody (np. entity.is_alive, a nie entity.is_alive()).
        """
        return self.health > 0

    def take_damage(self, amount: int):
        """
        Zmniejsza punkty zdrowia bytu.

        Args:
            amount (int): Ilość zadanych obrażeń.
        """
        if not self.is_alive:
            print(f"{self.name} jest już zniszczony/martwy i "
                  f"nie może otrzymać więcej obrażeń.")
            return

        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self._is_alive = False
            print(f"{self.name} otrzymuje {amount} obrażeń. "
                  f"{self.name} zostaje zniszczony/umiera!")
            self.on_death()

        else:
            print(f"{self.name} otrzymuje {amount} obrażeń. "
                  f"Zostało mu {self.health}/{self.max_health} HP.")

    def heal(self, amount: int):
        """
        Zwiększa punkty zdrowia bytu, nie przekraczając maksymalnego zdrowia.

        Args:
            amount (int): Ilość punktów zdrowia do uleczenia.
        """
        if not self.is_alive:
            print(
                f"{self.name} jest zniszczony/martwy i "
                f"nie może być uleczony/naprawiony.")
            return

        old_health = self.health
        self.health = min(self.health + amount, self.max_health)
        print(f"{self.name} leczy się o {self.health - old_health} HP. "
              f"Obecnie ma {self.health}/{self.max_health} HP.")

    def on_death(self):
        """
        Metoda wywoływana, gdy byt zostanie zniszczony lub umrze.
        Jest to metoda przeznaczona do nadpisania w klasach pochodnych
        (np. Monster, Item, Door), aby zaimplementować specyficzną logikę (np. upuszczenie łupu,
        zmiana stanu drzwi na "otwarte/zniszczone").
        """
        print(f"{self.name} ginie/przestaje istnieć.")

    def get_info(self):
        """
        Zwraca podstawowe informacje o bycie.
        """
        status = "Żyje" if self.is_alive else "Martwy/Zniszczony"
        return (f"--- {self.name} ({self.id[:8]}...) ---\n"
                f"Opis: {self.description}\n"
                f"Status: {status} ({self.health}/{self.max_health} HP)\n")

    def __str__(self):
        return (f"{self.name} (ID: {self.id[:8]}, "
                f"HP: {self.health}/{self.max_health})")
