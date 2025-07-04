import random
from istoty import Postac, Przeciwnik

# === ZMIENNE GLOBALNE MAPY I GRY ===
mapa_lasu = {}  # Słownik przechowujący wygenerowane lokacje. Klucz: (x, y), Wartość: słownik z danymi lokacji
obecna_pozycja_gracza = (0, 0) # Początkowa pozycja gracza na mapie (startujemy od (0,0))
limit_potworow_w_lesie = 3 # Ile potworów może być maksymalnie w całym generowanym lesie
wygenerowane_potwory = 0 # Licznik aktualnie wygenerowanych potworów
gracz = None # Zmienna na obiekt gracza, zostanie ustawiona w rozpocznij_nowa_gre()

# Pule opisów i zdarzeń dla lasu
opisy_lesne = [
    "Jesteś w gęstwinie drzew, słońce ledwie tu dociera. Słychać szum wiatru.",
    "Stoisz na niewielkiej leśnej polanie. Wokół ciebie rosną wysokie paprocie.",
    "Otacza cię gęsty las. Gdzieniegdzie widać ślady zwierząt.",
    "Ścieżka prowadzi przez zarośla. Powietrze jest duszne i ciężkie.",
    "Drzewa oplatają się ze sobą, tworząc naturalne sklepienie. Panuje tu półmrok.",
    "To wyjątkowo gęsta część lasu, przez którą ciężko się przedrzeć. Poczucie izolacji jest przytłaczające."
]

przedmioty_lesne = [
    {"nazwa": "Grzyb Jadalny", "opis": "Prosty grzyb, może odnowić 5 HP.", "typ": "leczniczy", "wartosc": 5},
    {"nazwa": "Zardzewiały Nóż", "opis": "Stary, zardzewiały nóż. Lepszy niż pięści.", "typ": "bron", "obrazenia": 7},
    {"nazwa": "Pusta Butelka", "opis": "Nic specjalnego, ale może się przydać.", "typ": "zwykly"},
    # Można dodawać więcej
]

def generuj_lokacje_lesna(x, y):
    """Generuje nową, losową lokację w lesie."""
    global wygenerowane_potwory

    lokacja = {
        "opis": random.choice(opisy_lesne),
        "przedmioty": [],
        "przeciwnik": None,
        "wyjscia": {}  # N, S, E, W
    }

    # Losowa szansa na przedmiot
    if random.random() < 0.3:  # 30% szans na przedmiot
        przedmiot = random.choice(przedmioty_lesne)
        lokacja["przedmioty"].append(przedmiot)
        print(
            f"W oddali dostrzegasz coś, co mogłoby być: {przedmiot['nazwa']}.")

    # Losowa szansa na przeciwnika, jeśli limit nie został osiągnięty
    if random.random() < 0.2 and wygenerowane_potwory < limit_potworow_w_lesie:  # 20% szans na potwora
        potwor_hp = random.randint(40, 60)  # HP potwora w zakresie
        potwor_sila = random.randint(8, 12)
        potwor_zrecznosc = random.randint(6, 10)
        lokacja["przeciwnik"] = Przeciwnik("Skrzekliwy Leśny Drapieżnik",
                                           potwor_hp, potwor_sila,
                                           potwor_zrecznosc)
        wygenerowane_potwory += 1
        print(
            "Słyszysz dziwne szmery. Wygląda na to, że nie jesteś sam w tej części lasu...")

    # Zawsze dodajemy podstawowe wyjścia (N, S, E, W)
    # W przyszłości dodamy logikę dla jeziora, czy ścian lasu
    lokacja["wyjscia"]["N"] = True  # Północ
    lokacja["wyjscia"]["S"] = True  # Południe
    lokacja["wyjscia"]["E"] = True  # Wschód
    lokacja["wyjscia"]["W"] = True  # Zachód

    # Przykładowe blokady (tutaj możemy dodać jezioro lub krawędzie mapy)
    if y > 5:  # Przykładowo, jeśli za daleko na północ, blokujemy wyjście
        lokacja["wyjscia"]["N"] = False
        print("Dalej na północ ścieżka staje się nieprzejezdna.")
    if x < -3:  # Przykładowo, jeśli za daleko na zachód, blokujemy wyjście
        lokacja["wyjscia"]["W"] = False
        print("Na zachód rozciąga się jezioro, blokujące dalszą drogę.")

    mapa_lasu[(x, y)] = lokacja  # Zapisujemy wygenerowaną lokację do mapy
    return lokacja


def pokaz_lokacje_gracza():
    """Wyświetla opis aktualnej lokacji gracza."""
    global obecna_pozycja_gracza
    x, y = obecna_pozycja_gracza

    if (x, y) not in mapa_lasu:
        generuj_lokacje_lesna(x, y)  # Jeśli lokacja nie istnieje, generujemy ją

    lokacja = mapa_lasu[(x, y)]

    print("\n" + "-" * 40)
    print(f"Jesteś w lesie na pozycji ({x},{y}).")  # Pomocnicze info o pozycji
    print(lokacja["opis"])

    if lokacja["przedmioty"]:
        print("Widzisz tu następujące przedmioty:")
        for i, item in enumerate(lokacja["przedmioty"]):
            print(f"{i + 1}. {item['nazwa']}")

    # Wyświetl dostępne kierunki
    print("Możesz iść w następujących kierunkach:")
    dostepne_kierunki = []
    if lokacja["wyjscia"].get("N"):
        dostepne_kierunki.append("Północ (N)")
    if lokacja["wyjscia"].get("S"):
        dostepne_kierunki.append("Południe (S)")
    if lokacja["wyjscia"].get("E"):
        dostepne_kierunki.append("Wschód (E)")
    if lokacja["wyjscia"].get("W"):
        dostepne_kierunki.append("Zachód (W)")

    if dostepne_kierunki:
        print(", ".join(dostepne_kierunki))
    else:
        print("Jesteś w ślepej uliczce! Nie ma dokąd iść.")
    print("-" * 40)

def poruszaj_gracza():
    """Obsługuje ruch gracza po mapie."""
    global obecna_pozycja_gracza
    x, y = obecna_pozycja_gracza
    lokacja = mapa_lasu[(x, y)]

    while True:
        kierunek = input(
            "Dokąd idziesz? (N/S/E/W, P - Podnieś, A - Atakuj, I - Ekwipunek): ").upper()

        nowe_x, nowe_y = x, y
        if kierunek == 'N' and lokacja["wyjscia"].get("N"):
            nowe_y += 1
        elif kierunek == 'S' and lokacja["wyjscia"].get("S"):
            nowe_y -= 1
        elif kierunek == 'E' and lokacja["wyjscia"].get("E"):
            nowe_x += 1
        elif kierunek == 'W' and lokacja["wyjscia"].get("W"):
            nowe_x -= 1
        elif kierunek == 'P':  # Akcja Podnieś
            if lokacja["przedmioty"]:
                for i, item in enumerate(lokacja["przedmioty"]):
                    print(f"{i + 1}. {item['nazwa']} - {item['opis']}")
                try:
                    wybor_przedmiotu_idx = int(input(
                        "Który przedmiot chcesz podnieść? (wpisz numer): ")) - 1
                    if 0 <= wybor_przedmiotu_idx < len(lokacja["przedmioty"]):
                        przedmiot_do_podniesienia = lokacja["przedmioty"].pop(
                            wybor_przedmiotu_idx)
                        gracz.ekwipunek.append(
                            przedmiot_do_podniesienia["nazwa"])
                        print(
                            f"Podniosłeś: {przedmiot_do_podniesienia['nazwa']}.")
                        # Jeśli to broń, możemy automatycznie ją wyposażyć (lub dać wybór)
                        if przedmiot_do_podniesienia["typ"] == "bron":
                            if gracz.obecna_bron["obrazenia"] < \
                                    przedmiot_do_podniesienia["obrazenia"]:
                                print(
                                    f"Nowa broń ({przedmiot_do_podniesienia['nazwa']}) jest lepsza niż Twoja obecna.")
                                gracz.zmien_bron(przedmiot_do_podniesienia)
                        elif przedmiot_do_podniesienia["typ"] == "leczniczy":
                            # Tymczasowo używamy od razu
                            gracz.hp = min(gracz.max_hp,
                                           gracz.hp + przedmiot_do_podniesienia[
                                               "wartosc"])
                            print(
                                f"Używasz {przedmiot_do_podniesienia['nazwa']} i odzyskujesz {przedmiot_do_podniesienia['wartosc']} HP. Twoje HP: {gracz.hp}/{gracz.max_hp}")
                            gracz.ekwipunek.remove(przedmiot_do_podniesienia[
                                                       "nazwa"])  # Usuwamy z ekwipunku po użyciu
                    else:
                        print("Nieprawidłowy numer przedmiotu.")
                except ValueError:
                    print("Wpisz numer.")
            else:
                print("W tej lokacji nie ma przedmiotów do podniesienia.")
            # Po akcji podniesienia, pozwalamy graczowi na kolejną akcję w tej samej turze
            pokaz_lokacje_gracza()
            continue

        elif kierunek == 'A':  # Akcja Atakuj (jeśli jest potwór)
            if lokacja["przeciwnik"]:
                print(
                    f"Przygotowujesz się do ataku na {lokacja['przeciwnik'].nazwa}!")
                # Tutaj wywołamy funkcję walki
                walcz_z_przeciwnikiem(lokacja["przeciwnik"],
                                      obecna_pozycja_gracza)  # Przekazujemy potwora i pozycję
                # Po walce, jeśli potwór został pokonany, usuwamy go z lokacji
                if lokacja["przeciwnik"].hp <= 0:
                    lokacja["przeciwnik"] = None
                return  # Po walce gracz wybiera akcje od nowa (czyli wyświetlamy lokacje)
            else:
                print("Nie ma tu żadnych przeciwników do zaatakowania.")
            pokaz_lokacje_gracza()
            continue

        elif kierunek == 'I':  # Akcja Ekwipunek
            print("\n--- TWÓJ EKWIPUNEK ---")
            if not gracz.ekwipunek:
                print("Twój ekwipunek jest pusty.")
            else:
                for item in gracz.ekwipunek:
                    print(f"- {item}")
            print(
                f"Obecnie wyposażona broń: {gracz.obecna_bron['nazwa']} (Obrażenia: {gracz.obecna_bron['obrazenia']})")
            input("Naciśnij ENTER, aby wrócić do eksploracji...\n")
            pokaz_lokacje_gracza()  # Ponownie wyświetl lokację
            continue

        elif kierunek == 'Q':  # Opcja wyjścia z eksploracji (do menu głównego)
            print("Opuszczasz las i wracasz do menu głównego gry.")
            return

        elif (nowe_x, nowe_y) == (
        x, y):  # Jeśli kierunek jest nieprawidłowy lub zablokowany
            print(
                "Nie możesz iść w tym kierunku. Wybierz inną drogę (N/S/E/W) lub akcję (P/A/I).")
            continue

        else:  # Poprawny ruch
            obecna_pozycja_gracza = (nowe_x, nowe_y)
            break  # Wyjście z pętli ruchu, aby odświeżyć lokację

def rozpocznij_nowa_gre():
    """Funkcja uruchamiająca nową grę."""

    print("\n--- ROZPOCZYNAMY NOWĄ GRĘ ---")
    imie_gracza = input("Podaj imię swojego bohatera: ")

    # Wybór rasy
    rasa_wybor = wybor_rasy()

    # Wybór klasy (na razie tylko wojownik)
    klasa_wybor = wybor_klasy()

    # Tworzymy obiekt gracza na podstawie dokonanych wyborów
    global gracz # Deklarujemy 'gracz' jako zmienną globalną
    gracz = Postac(imie_gracza, rasa_wybor, klasa_wybor)

    print(f"\nJesteś {gracz.imie}, {gracz.rasa} {gracz.klasa}. "
          f"Przygotuj się na przygodę!")
    print(f"Twoje początkowe statystyki: "
          f"HP: {gracz.hp}/{gracz.max_hp}, "
          f"Siła: {gracz.sila}, "
          f"Zręczność: {gracz.zrecznosc}, "
          f"Wytrzymałość: {gracz.wytrzymalosc}")

    print("Budzisz się w gęstym, nieznanym lesie. Powietrze jest gęste od wilgoci i dziwnych zapachów.")
    print("Twoje futurystyczne ubranie wydaje się tutaj zupełnie nie na miejscu.")
    print("Coś szepcze w oddali...")
    input("Naciśnij ENTER, aby kontynuować...\n")

    print("Słońce przebija się przez gęste liście, a ty czujesz, że nie jesteś "
          "sam...")
    input("\nNaciśnij ENTER, aby wyruszyć w głąb nieznanego...\n")

    # TUTAJ WYWOŁUJEMY PIERWSZĄ SCENĘ GRY

    # Tutaj w przyszłości będzie rozpoczynał się faktyczny świat gry, np. pierwsza scena z przeciwnikiem.

    print("\nCzujesz, że musisz zacząć odkrywać ten dziwny, nowy świat.")
    input("Naciśnij ENTER, aby wyruszyć...\n")

    # Nowa główna pętla eksploracji
    eksploracja_lasu()  # Wywołujemy nową funkcję, która będzie pętlą gry
    # scena_lesna_z_drapieznikiem()

    # Tutaj w przyszłości będzie rozpoczynał się faktyczny świat gry, np. pierwsza scena z przeciwnikiem.

def wczytaj_gre():
    """Funkcja do wczytywania zapisanego stanu gry (na razie atrapa)."""
    print("\n--- WCZYTAJ GRĘ ---")
    print("Brak zapisanych gier lub funkcja wczytywania nie jest jeszcze zaimplementowana.")
    input("Naciśnij ENTER, aby wrócić do menu...\n")

def opcje_gry():
    """Funkcja do ustawień gry (na razie atrapa)."""
    print("\n--- OPCJE GRY ---")
    print("Tutaj w przyszłości znajdą się ustawienia dźwięku, grafiki (jeśli będzie) itp.")
    input("Naciśnij ENTER, aby wrócić do menu...\n")

def wyjdz_z_gry():
    """Funkcja do wyjścia zgry."""
    print("\nŻegnaj! Dziękujemy za grę.")

def wyswietl_menu():
    """Główna funkcja wyświetlająca menu i obsługująca wybór gracza."""
    while True:
        print("\n" + "="*30)
        print("    TEKSTOWE RPG: NIEZNANY WYMIAR")
        print("="*30)
        print("1. Nowa Gra")
        print("2. Wczytaj Grę")
        print("3. Opcje")
        print("4. Wyjdź")
        print("="*30)

        wybor = input("Wybierz opcję (1-4): ")

        if wybor == '1':
            rozpocznij_nowa_gre()
        elif wybor == '2':
            wczytaj_gre()
        elif wybor == '3':
            opcje_gry()
        elif wybor == '4':
            wyjdz_z_gry()
            break
        else:
            print("\nNieprawidłowy wybór. Spróbuj ponownie.")


def wybor_rasy():
    """Wybór rasy (na razie tylko człowiek)"""
    while True:
        print("\n--- WYBÓR RASY ---")
        print("1. Człowiek")
        # print("2. Elf (jeszcze niedostępne)") # Przykład na przyszłe opcje
        wybor_rasy = input("Wybierz swoją rasę: ")
        if wybor_rasy == '1':
            rasa = "Człowiek"
            print(f"Wybrałeś rasę: {rasa}.")
            return rasa
        else:
            print("Nieprawidłowy wybór rasy. Wybierz '1'.")

def wybor_klasy():
    # Wybór klasy (na razie tylko wojownik)
    while True:
        print("\n--- WYBÓR KLASY ---")
        print("1. Wojownik")
        # print("2. Mag (jeszcze niedostępne)") # Przykład na przyszłe opcje
        # print("3. Łucznik (jeszcze niedostępne)")
        wybor_klasy = input("Wybierz swoją klasę: ")
        if wybor_klasy == '1':
            klasa = "Wojownik"
            print(f"Wybrałeś klasę: {klasa}.")
            return klasa
        else:
            print("Nieprawidłowy wybór klasy. Wybierz '1'.")


def walcz_z_przeciwnikiem(przeciwnik, pozycja_walki):
    """Obsługuje ogólną walkę z dowolnym przeciwnikiem."""
    global gracz, obecna_pozycja_gracza  # Potrzebujemy dostępu do obiektu gracza i jego pozycji

    print(f"\n--- WALKA Z: {przeciwnik.nazwa.upper()} ---")
    print(f"Jesteś zaskoczony! {przeciwnik.nazwa} szykuje się do ataku!")
    input("Naciśnij ENTER, aby przygotować się do walki...\n")

    # Pętla walki
    while gracz.hp > 0 and przeciwnik.hp > 0:  # Zamiast drapiezniki.hp, używamy przeciwnik.hp
        print("\n--- TURA WALKI ---")
        print(
            f"Twoje HP: {gracz.hp}/{gracz.max_hp} | HP {przeciwnik.nazwa}: {przeciwnik.hp}/{przeciwnik.max_hp}")
        print(
            f"Wyposażona broń: {gracz.obecna_bron['nazwa']} (Obrażenia: {gracz.obecna_bron['obrazenia']})")
        print("Co robisz?")
        print("1. Atakuj")
        print("2. Uciekaj (niebezpieczne!)")
        print("3. Sprawdź ekwipunek")

        wybor_walka = input("Wybierz akcję (1-3): ")

        if wybor_walka == '1':
            obrazenia_gracza = gracz.oblicz_obrazenia_ataku() - przeciwnik.zrecznosc // 2
            if obrazenia_gracza < 1:
                obrazenia_gracza = 1
            print(
                f"\nAtakujesz {przeciwnik.nazwa} za pomocą {gracz.obecna_bron['nazwa']} i zadajesz {obrazenia_gracza} obrażeń!")
            przeciwnik_pokonany = przeciwnik.otrzymuje_obrazenia(
                obrazenia_gracza)

            if przeciwnik_pokonany:
                print(f"** {przeciwnik.nazwa} został pokonany! **")
                print(
                    "Czujesz ulgę, ale las wciąż jest pełen nieznanych zagrożeń.")
                gracz.dodaj_doswiadczenie(50)
                print(
                    "Przeszukujesz szczątki i znajdujesz dziwny, połyskujący **szpon**.")
                gracz.ekwipunek.append("Szpon Drapieżnika")
                print(f"Twój ekwipunek: {gracz.ekwipunek}")
                obecna_pozycja_gracza = pozycja_walki  # Gracz wraca do miejsca walki
                return  # Koniec funkcji walki

        elif wybor_walka == '2':
            print("\nPróbujesz uciec! To bardzo niebezpieczne...")
            szansa_ucieczki = gracz.zrecznosc - przeciwnik.zrecznosc + 5
            if szansa_ucieczki > 10:
                print(
                    "Udało Ci się uciec od przeciwnika! Odzyskujesz oddech, ale nie masz pojęcia, gdzie jesteś.")
                obecna_pozycja_gracza = pozycja_walki  # Gracz wraca do miejsca walki
                return
            else:
                print(
                    "Przeciwnik jest zbyt szybki! Nie udało Ci się uciec i zostajesz trafiony!")
                obrazenia_przeciwnika = przeciwnik.sila - gracz.wytrzymalosc // 2
                if obrazenia_przeciwnika < 1:
                    obrazenia_przeciwnika = 1
                gracz.hp -= obrazenia_przeciwnika
                print(
                    f"Otrzymujesz {obrazenia_przeciwnika} obrażeń. Twoje HP: {gracz.hp}/{gracz.max_hp}.")
                if gracz.hp <= 0:
                    print(
                        "\nTwoje siły Cię opuszczają... Ciemność Cię ogarnia. Koniec gry.")
                    return

        elif wybor_walka == '3':
            print("\n--- TWÓJ EKWIPUNEK ---")
            if not gracz.ekwipunek:
                print("Twój ekwipunek jest pusty.")
            else:
                for item in gracz.ekwipunek:
                    print(f"- {item}")
            print(
                f"Obecnie wyposażona broń: {gracz.obecna_bron['nazwa']} (Obrażenia: {gracz.obecna_bron['obrazenia']})")
            input("Naciśnij ENTER, aby wrócić do walki...\n")
            continue

        else:
            print("Nieprawidłowy wybór. Wybierz '1', '2' lub '3'.")
            continue

            # Tura przeciwnika (jeśli żyje)
        if przeciwnik.hp > 0:
            print(f"\n{przeciwnik.nazwa} atakuje!")
            obrazenia_przeciwnika = przeciwnik.sila - gracz.wytrzymalosc // 2
            if obrazenia_przeciwnika < 1:
                obrazenia_przeciwnika = 1
            gracz.hp -= obrazenia_przeciwnika
            print(
                f"Otrzymujesz {obrazenia_przeciwnika} obrażeń! Twoje HP: {gracz.hp}/{gracz.max_hp}.")

            if gracz.hp <= 0:
                print(
                    "\nTwoje siły Cię opuszczają... Ciemność Cię ogarnia. Koniec gry.")
                return

    if gracz.hp <= 0:
        print("\n--- PRZEGRAŁEŚ! ---")
        print("Możesz spróbować ponownie, wybierając 'Nowa Gra'.")
    # Po zakończeniu walki (porażce) nie wracamy do mapy, bo gra się kończy

def eksploracja_lasu():
    """Główna pętla eksploracji lasu."""
    global obecna_pozycja_gracza, mapa_lasu, wygenerowane_potwory, limit_potworow_w_lesie

    # Resetowanie stanu mapy i potworów przy nowej grze
    mapa_lasu = {}
    obecna_pozycja_gracza = (0, 0)
    wygenerowane_potwory = 0

    while True:
        pokaz_lokacje_gracza()
        print(mapa_lasu)
        current_x, current_y = obecna_pozycja_gracza
        current_location = mapa_lasu[(current_x, current_y)]

        # Sprawdzenie, czy jest przeciwnik w lokacji po odświeżeniu
        if current_location["przeciwnik"]:
            print(
                f"\nUWAGA! {current_location['przeciwnik'].nazwa} blokuje Ci drogę!")
            # Tutaj automatycznie wchodzimy w walkę, jeśli gracz wszedł w lokację z potworem
            walcz_z_przeciwnikiem(current_location["przeciwnik"],
                                  obecna_pozycja_gracza)
            # Po walce, jeśli potwór został pokonany, usuwamy go z lokacji
            if current_location["przeciwnik"] and current_location[
                "przeciwnik"].hp <= 0:
                current_location["przeciwnik"] = None

            # Jeśli gracz przegrał walkę lub uciekł, funkcja walki już obsłuży wyjście z gry/sceny
            if gracz.hp <= 0:  # Jeśli gracz przegrał, kończymy eksplorację
                return
            else:  # Jeśli uciekł lub wygrał, pokazujemy lokację ponownie, aby mógł podjąć decyzje
                pokaz_lokacje_gracza()

        # Jeśli nie ma potwora lub został pokonany, pozwalamy na ruch
        poruszaj_gracza()

        # Jeśli funkcja poruszaj_gracza zwróci (bo Q, walka, śmierć), kończymy pętlę eksploracji
        if gracz.hp <= 0 or (poruszaj_gracza.__code__.co_consts and
                             poruszaj_gracza.__code__.co_consts[
                                 -1] == "Opuszczasz las i wracasz do menu głównego gry."):
            break

def scena_lesna_z_drapieznikiem():
    """Obsługuje pierwszą scenę w lesie i walkę z drapieżnikiem."""
    global gracz  # Potrzebujemy dostępu do obiektu gracza
    print("\n--- GĘSTY LAS ---")

    print(
        "Rozglądasz się nerwowo. Coś tu nie gra. Nagle dostrzegasz coś na ziemi.")

    # Szansa na znalezienie broni
    print(
        "\nNa ziemi, niedaleko Ciebie, leży **gruby patyk** i kilka **kamieni**.")
    print("Mogłyby posłużyć jako prowizoryczna broń.")

    while True:
        wybor_broni = input("Czy chcesz podnieść patyk (T/N)? ").lower()
        if wybor_broni == 't':
            patyk = {"nazwa": "Gruby Patyk",
                     "obrazenia": 10}  # Patyk zadaje 10 dodatkowych obrażeń
            gracz.zmien_bron(patyk)
            gracz.ekwipunek.append("Gruby Patyk")
            break
        elif wybor_broni == 'n':
            print(
                "Postanawiasz polegać na swoich pięściach. Oby to wystarczyło...")
            break
        else:
            print("Nieprawidłowy wybór. Wpisz 'T' dla Tak lub 'N' dla Nie.")

    input("\nNaciśnij ENTER, aby kontynuować zagłębianie się w las...\n")

    print(
        "Słońce ledwie przebija się przez gęste korony drzew. Słyszysz niepokojące szmery...")
    print(
        "Nagle, z cienia, wyłania się stworzenie, jakiego nigdy wcześniej nie widziałeś.")
    print(
        "Jego ciało pokryte jest pnączami i ostrymi kolcami, a z paszczy wydobywa się przeraźliwy skrzek.")
    print("To **Skrzekliwy Leśny Drapieżnik**!")

    # Tworzymy naszego pierwszego przeciwnika (młodsza, nieco osłabiona wersja)
    drapiezniki_hp = 50
    drapiezniki_sila = 10
    drapiezniki_zrecznosc = 8
    drapiezniki = Przeciwnik("Skrzekliwy Leśny Drapieżnik", drapiezniki_hp,
                             drapiezniki_sila, drapiezniki_zrecznosc)

    input("\nNaciśnij ENTER, aby przygotować się do walki...\n")

    # Pętla walki
    while gracz.hp > 0 and drapiezniki.hp > 0:
        print("\n--- TURA WALKI ---")
        print(
            f"Twoje HP: {gracz.hp}/{gracz.max_hp} | HP {drapiezniki.nazwa}: {drapiezniki.hp}/{drapiezniki.max_hp}")
        print(
            f"Wyposażona broń: {gracz.obecna_bron['nazwa']} (Obrażenia: {gracz.obecna_bron['obrazenia']})")  # Pokaż broń
        print("Co robisz?")
        print("1. Atakuj")
        print("2. Uciekaj (niebezpieczne!)")
        print("3. Sprawdź ekwipunek")

        wybor_walka = input("Wybierz akcję (1-3): ")

        if wybor_walka == '1':
            # Atak gracza
            obrazenia_gracza = gracz.oblicz_obrazenia_ataku() - drapiezniki.zrecznosc // 2
            if obrazenia_gracza < 1:  # Upewniamy się, że obrażenia są zawsze co najmniej 1
                obrazenia_gracza = 1
            print(
                f"\nAtakujesz {drapiezniki.nazwa} za pomocą {gracz.obecna_bron['nazwa']} i zadajesz {obrazenia_gracza} obrażeń!")
            drapiezniki_pokonany = drapiezniki.otrzymuje_obrazenia(
                obrazenia_gracza)

            if drapiezniki_pokonany:
                print(f"** {drapiezniki.nazwa} został pokonany! **")
                print(
                    "Czujesz ulgę, ale las wciąż jest pełen nieznanych zagrożeń.")

                # NOWY KOD PO ZWYCIĘSTWIE:
                gracz.dodaj_doswiadczenie(
                    50)  # Dajemy 50 PD za pokonanie drapieżnika
                print(
                    "Przeszukujesz szczątki drapieżnika i znajdujesz dziwny, połyskujący **szpon**.")
                gracz.ekwipunek.append("Szpon Drapieżnika")
                print(f"Twój ekwipunek: {gracz.ekwipunek}")

                input("\nNaciśnij ENTER, aby kontynuować...\n")

                # Zamiast return, przechodzimy do wyborów dalszej drogi
                wybory_po_walce()
                return  # Koniec sceny z drapieżnikiem

        elif wybor_walka == '2':
            # Próba ucieczki
            print("\nPróbujesz uciec! To bardzo niebezpieczne...")
            szansa_ucieczki = gracz.zrecznosc - drapiezniki.zrecznosc + 5  # Im większa różnica, tym łatwiej
            if szansa_ucieczki > 10:  # Ucieczka powodzi się
                print(
                    "Udało Ci się uciec od drapieżnika! Odzyskujesz oddech, ale nie masz pojęcia, gdzie jesteś.")
                # KOD PO UCIECZCE:
                # Brak PD i przedmiotów, ale gracz żyje
                input("\nNaciśnij ENTER, aby zastanowić się, co dalej...\n")
                wybory_po_walce()
                return  # Koniec sceny z drapieżnikiem
            else:
                    print(
                        "Drapieżnik jest zbyt szybki! Nie udało Ci się uciec i zostajesz trafiony!")
                    obrazenia_drapieznika = drapiezniki.sila - gracz.wytrzymalosc // 2
                    if obrazenia_drapieznika < 1:
                        obrazenia_drapieznika = 1
                    gracz.hp -= obrazenia_drapieznika
                    print(
                        f"Otrzymujesz {obrazenia_drapieznika} obrażeń. Twoje HP: {gracz.hp}/{gracz.max_hp}.")
                    if gracz.hp <= 0:
                        print(
                            "\nTwoje siły Cię opuszczają... Ciemność Cię ogarnia. Koniec gry.")
                        return  # Koniec gry, gracz przegrał

        elif wybor_walka == '3':  # Sprawdź ekwipunek
            print("\n--- TWÓJ EKWIPUNEK ---")
            if not gracz.ekwipunek:
                print("Twój ekwipunek jest pusty.")
            else:
                for item in gracz.ekwipunek:
                    print(f"- {item}")
            print(
                f"Obecnie wyposażona broń: {gracz.obecna_bron['nazwa']} (Obrażenia: {gracz.obecna_bron['obrazenia']})")
            input("Naciśnij ENTER, aby wrócić do walki...\n")
            continue  # Pozwala graczowi wrócić do wyboru akcji w tej samej turze

        else:
            print("Nieprawidłowy wybór. Wybierz '1' lub '2'.")
            continue  # Ponów turę, aby gracz wybrał poprawnie

        # Tura przeciwnika (jeśli żyje)
        if drapiezniki.hp > 0:
            print(f"\n{drapiezniki.nazwa} atakuje!")
            obrazenia_drapieznika = drapiezniki.sila - gracz.wytrzymalosc // 2  # Prosty wzór
            if obrazenia_drapieznika < 1:
                obrazenia_drapieznika = 1
            gracz.hp -= obrazenia_drapieznika
            print(
                f"Otrzymujesz {obrazenia_drapieznika} obrażeń! Twoje HP: {gracz.hp}/{gracz.max_hp}.")

            if gracz.hp <= 0:
                print(
                    "\nTwoje siły Cię opuszczają... Ciemność Cię ogarnia. Koniec gry.")
                return  # Koniec gry, gracz przegrał

    if gracz.hp <= 0:
        print("\n--- PRZEGRAŁEŚ! ---")
        print("Możesz spróbować ponownie, wybierając 'Nowa Gra'.")


def wybory_po_walce():
    """Pozwala graczowi na podjęcie decyzji po walce/ucieczce z drapieżnikiem."""
    print("\n--- CO DALEJ? ---")
    print("Stoisz na leśnej polanie. Coś ci podpowiada, że powinieneś iść dalej.")
    print("Widzisz dwie wyraźne ścieżki:")
    print("1. Podążaj **Wąską Ścieżką** prowadzącą w głąb gęstego lasu. Wydaje się cicha i bezpieczna, ale co się za nią kryje?")
    print("2. Idź **Szerokim Traktem** w kierunku ledwie widocznej mgły. Może to droga do cywilizacji... albo czegoś gorszego.")

    while True:
        wybor_drogi = input("Którą ścieżkę wybierasz (1-2)?: ")
        if wybor_drogi == '1':
            print("\nWkraczasz na Wąską Ścieżkę. Z każdą chwilą las staje się ciemniejszy i bardziej tajemniczy.")
            # Tutaj wywołamy kolejną funkcję sceny dla Wąskiej Ścieżki
            input("Naciśnij ENTER, aby kontynuować podróż...\n")
            # np. scena_ciemnego_lasu()
            print("To koniec demo tej ścieżki na dziś!") # Tymczasowo
            break
        elif wybor_drogi == '2':
            print("\nRuszasz Szerokim Traktem. Powietrze staje się cięższe, a mgła gęstnieje, zasłaniając widoczność.")
            # Tutaj wywołamy kolejną funkcję sceny dla Szerokiego Traktu
            input("Naciśnij ENTER, aby kontynuować podróż...\n")
            # np. scena_mglistego_bagna()
            print("To koniec demo tej ścieżki na dziś!") # Tymczasowo
            break
        else:
            print("Nieprawidłowy wybór. Wybierz '1' lub '2'.")

# Główny punkt startowy programu
if __name__ == "__main__":
    wyswietl_menu()
