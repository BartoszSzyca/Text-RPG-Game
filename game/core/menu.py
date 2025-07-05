from races import Human
from characters import Warrior

def new_game():
    print("Funkcja rozpocznij_nowa_gre.")

def save_game():
    """Zapisuje bieżący stan gry do pliku."""
    print("\n--- ZAPISZ GRĘ ---")
    print("Funkcja wczytywania nie jest jeszcze zaimplementowana.")
    input("Naciśnij ENTER, aby wrócić do menu...\n")

def load_game():
    """Funkcja do wczytywania zapisanego stanu gry (na razie atrapa)."""
    print("\n--- WCZYTAJ GRĘ ---")
    print("Brak zapisanych gier lub funkcja wczytywania nie jest jeszcze zaimplementowana.")
    input("Naciśnij ENTER, aby wrócić do menu...\n")

def game_options():
    """Funkcja do ustawień gry (na razie atrapa)."""
    print("\n--- OPCJE GRY ---")
    print("Tutaj w przyszłości znajdą się ustawienia dźwięku, grafiki (jeśli będzie) itp.")
    input("Naciśnij ENTER, aby wrócić do menu...\n")

def exit_game():
    """Funkcja do wyjścia zgry."""
    print("\nŻegnaj! Dziękujemy za grę.")

def show_menu():
    """Główna funkcja wyświetlająca menu i obsługująca wybór gracza."""
    while True:
        print("\n" + "="*30)
        print("    TEKSTOWE RPG: NIEZNANY WYMIAR")
        print("="*30)
        print("1. Nowa Gra")
        print("2. Zapisz Grę")
        print("3. Wczytaj Grę")
        print("4. Opcje")
        print("5. Wyjdź")
        print("="*30)

        wybor = input("Wybierz opcję (1-5): ")

        if wybor == '1':
            new_game()
        elif wybor == '2':
            save_game()
        elif wybor == '3':
            load_game()
        elif wybor == '4':
            game_options()
        elif wybor == '5':
            exit_game()
            break
        else:
            print("\nNieprawidłowy wybór. Spróbuj ponownie.")

def choose_race():
    while True:
        print("\n--- WYBÓR RASY ---")
        print("1. Człowiek")
        wybor_input = input("Wybierz swoją rasę: ")
        if wybor_input == '1':
            rasa_wybor = "Człowiek"
            race = Human()
            print(f"Wybrałeś rasę: {rasa_wybor}.")
            return race
        else:
            print("Nieprawidłowy wybór rasy. Wybierz '1'.")

def choose_class():
    while True:
        print("\n--- WYBÓR KLASY ---")
        print("1. Wojownik")
        wybor_input = input("Wybierz swoją klasę: ")
        if wybor_input == '1':
            klasa_wybor = "Wojownik"
            print(f"Wybrałeś klasę: {klasa_wybor}.")
            profession = Warrior()
            return profession
        else:
            print("Nieprawidłowy wybór klasy. Wybierz '1'.")

if __name__ == "__main__":
    show_menu()