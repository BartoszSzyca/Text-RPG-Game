class Postac:
    def __init__(self, imie, rasa, klasa):
        self.imie = imie
        self.rasa = rasa
        self.klasa = klasa
        self.hp = 0
        self.max_hp = 0
        self.sila = 0
        self.zrecznosc = 0
        self.wytrzymalosc = 0
        self.inteligencja = 0
        self.charyzma = 0
        self.ekwipunek = []
        self.doswiadczenie = 0
        self.poziom = 1
        self.exp_do_nastepnego_poziomu = 100

        self.obecna_bron = {"nazwa": "Pięści", "obrazenia": 5}  # Domyślna broń

        self.ustaw_poczatkowe_statystyki()

    def ustaw_poczatkowe_statystyki(self):
        """Ustawia początkowe statystyki w zależności od rasy i klasy."""
        # Tymczasowo, dla naszej pierwszej postaci: Człowiek Wojownik
        if self.rasa == "Człowiek" and self.klasa == "Wojownik":
            self.max_hp = 100
            self.hp = self.max_hp
            self.sila = 15
            self.zrecznosc = 10
            self.wytrzymalosc = 12
            self.inteligencja = 8
            self.charyzma = 7
            print(f"Statystyki startowe dla {self.rasa} {self.klasa} zostały ustawione.")
        else:
            # W przyszłości dodamy tu logikę dla innych kombinacji ras i klas
            print("Brak zdefiniowanych statystyk dla tej kombinacji rasy/klasy. Ustawiono domyślne.")
            self.max_hp = 50
            self.hp = self.max_hp
            self.sila = 5
            self.zrecznosc = 5
            self.wytrzymalosc = 5
            self.inteligencja = 5
            self.charyzma = 5

    # Dodawanie doświadczenia i poziomowanie
    def dodaj_doswiadczenie(self, ilosc_exp):
        self.doswiadczenie += ilosc_exp
        print(f"Zdobywasz {ilosc_exp} punktów doświadczenia.")
        while self.doswiadczenie >= self.exp_do_nastepnego_poziomu:
            self.poziom_w_gore()

    def poziom_w_gore(self):
        self.poziom += 1
        self.doswiadczenie -= self.exp_do_nastepnego_poziomu
        self.exp_do_nastepnego_poziomu = int(self.exp_do_nastepnego_poziomu * 1.5) # Zwiększ wymagane PD

        print(f"\n--- GRATULACJE! OSIĄGNĄŁEŚ POZIOM {self.poziom}! ---")
        # Przykładowe zwiększenie statystyk po awansie:
        self.max_hp += 10
        self.hp = self.max_hp # Ulecz się do pełna po awansie
        self.sila += 2
        self.zrecznosc += 1
        self.wytrzymalosc += 2
        print("Twoje statystyki wzrosły!")
        print(f"Nowe statystyki: HP: {self.hp}/{self.max_hp}, Siła: {self.sila}, Zręczność: {self.zrecznosc}, Wytrzymałość: {self.wytrzymalosc}")

    # Zmiana broni
    def zmien_bron(self, nowa_bron):
        self.obecna_bron = nowa_bron
        print(f"Wyposażyłeś: {self.obecna_bron['nazwa']}.")

    # Obliczanie obrażeń ataku (uwzględnia broń)
    def oblicz_obrazenia_ataku(self):
        # Obrażenia = siła postaci + obrażenia z broni
        return self.sila + self.obecna_bron["obrazenia"]

class Przeciwnik:
    def __init__(self, nazwa, hp, sila, zrecznosc):
        self.nazwa = nazwa
        self.hp = hp
        self.max_hp = hp # Maksymalne HP przeciwnika
        self.sila = sila
        self.zrecznosc = zrecznosc

    def otrzymuje_obrazenia(self, obrazenia):
        self.hp -= obrazenia
        if self.hp < 0:
            self.hp = 0
        print(f"{self.nazwa} otrzymuje {obrazenia} obrażeń. Pozostało mu {self.hp}/{self.max_hp} HP.")
        if self.hp <= 0:
            print(f"{self.nazwa} został pokonany!")
            return True # Przeciwnik pokonany
        return False # Przeciwnik żyje