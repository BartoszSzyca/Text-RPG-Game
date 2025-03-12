# Tekstowa gra RPG

## Spis treści

1.  [Ogólny opis projektu](#ogólny-opis-projektu)
2.  [Struktura plików i folderów](#struktura-plików-i-folderów)
3.  [Opis klas i ich funkcjonalności](#opis-klas-i-ich-funkcjonalności)
4.  [Diagram klas](#diagram-klas)
5.  [Przykładowe atrybuty i metody](#przykładowe-atrybuty-i-metody)
6.  [Przykładowe scenariusze użycia](#przykładowe-scenariusze-użycia)
7.  [Konfiguracja i dane](#konfiguracja-i-dane)
8.  [Funkcje pomocnicze](#funkcje-pomocnicze)
9.  [Instrukcja uruchomienia](#instrukcja-uruchomienia)

1. Ogólny opis projektu

* Nazwa projektu: Tekstowa gra RPG
* Cel projektu: Stworzenie rozbudowanej, tekstowej gry RPG w języku Python, z
naciskiem na modułową i rozszerzalną architekturę.
* Główne założenia:
 - Architektura oparta na obiektach (OOP).
 - Modułowa struktura kodu, ułatwiająca rozbudowę i modyfikacje.
 - Elastyczny system ras, klas postaci i potworów.
 - Interaktywne lokacje i system walki.
2. Struktura plików i folderów

rpg_game/
├── core/
│   ├── game_manager.py
│   ├── combat.py
│   └── interaction.py
├── entities/
│   ├── entity.py
├── characters/
│   ├── character.py
│   ├── player.py
│   ├── npc.py
│   ├── warrior.py
│   ├── mage.py
│   └── archer.py
├── monsters/
│   ├── monster.py
│   ├── goblin.py
│   ├── wolf.py
│   └── troll.py
├── races/
│   ├── race.py
│   ├── human.py
│   ├── goblin_race.py
│   └── wolf_race.py
├── locations/
│   ├── location.py
│   ├── forest.py
│   ├── cave.py
│   └── dungeon.py
├── items/
│   ├── item.py
│   ├── weapon.py
│   ├── armor.py
│   └── potion.py
├── data/
│   ├── config.json
│   └── saves/
├── utils/
│   └── helpers.py
└── main.py
* core/: Podstawowe mechaniki gry (zarządzanie grą, walka, interakcje).
* entities/: Klasa bazowa dla wszystkich bytów.
* characters/: Klasy postaci gracza i NPC.
* monsters/: Klasy potworów.
* races/: Klasy ras.
* locations/: Klasy lokacji.
* items/: Klasy przedmiotów.
* data/: Dane gry (konfiguracja, zapisy).
* utils/: Funkcje pomocnicze.
* main.py: Główny plik uruchamiający grę.
3. Opis klas i ich funkcjonalności

* entities/entity.py:
 - Klasa bazowa dla wszystkich bytów.
 - Atrybuty: name, health, attack, defense.
 - Metody: take_damage(), attack(), defend().
* characters/character.py:
 - Klasa bazowa dla postaci gracza i NPC.
 - Dziedziczy po Entity.
 - Atrybuty: inventory, skills, level, experience, stats, attributes.
 - Metody: add_item(), remove_item(), use_skill(), calculate_attributes().
* characters/player.py:
 - Klasa postaci gracza.
 - Dziedziczy po Character.
 - Atrybuty: gold, quests.
 - Metody: gain_experience(), level_up().
* characters/npc.py:
 - Klasa postaci niezależnych.
 - Dziedziczy po Character.
 - Atrybuty: dialogue, quests_available.
 - Metody: talk(), offer_quest().
* monsters/monster.py:
 - Klasa bazowa dla potworów.
 - Dziedziczy po Entity.
 - Atrybuty: experience_reward, loot.
 - Metody: die().
* races/race.py:
 - Klasa bazowa dla ras.
 - Atrybuty: name, base_stats, racial_skills.
* locations/location.py:
 - Klasa bazowa dla lokacji.
 - Atrybuty: name, description, entities_present, items_present.
 - Metody: enter(), exit().
* items/item.py:
 - Klasa bazowa dla przedmiotów.
 - Atrybuty: name, description, value.
* core/game_manager.py:
 - Główna klasa zarządzająca grą.
 - Metody: start_game(), load_game(), save_game(), handle_input(), update(),
 render().
* core/combat.py:
 - Logika walki.
 - Funkcje: calculate_damage(), initiate_combat(), handle_turn().
* core/interaction.py:
 - Obsługa interakcji.
 - Funkcje: talk_to_npc(), examine_item(), enter_location().
4. Diagram klas

* Diagram UML przedstawiający relacje między klasami (dziedziczenie, asocjacje).
+-----------------+     ^
    |     Entity      |     | (Dziedziczenie)
    +-----------------+     |
    | - name: str     |     |
    | - health: int   |     |
    | - attack: int   |     |
    | - defense: int  |     |
    +-----------------+     |
    | + take_damage() |     |
    | + attack()      |     |
    | + defend()      |     |
    +-----------------+     |
                              |
    +-----------------+     |
    |    Character    |     |
    +-----------------+     |
    | - inventory: list|     |
    | - skills: list  |     |
    | - level: int    |     |
    | - experience: int|     |
    +-----------------+     |
    | + add_item()    |     |
    | + remove_item() |     |
    | + use_skill()   |     |
    +-----------------+     |
    ^             ^         |
    |             |         |
    |             |         |
+-----------------+ +-----------------+
|     Player      | |      NPC        |
+-----------------+ +-----------------+
| - gold: int     | | - dialogue: str |
| - quests: list  | | - quests_avail:list|
+-----------------+ +-----------------+
| + gain_exp()    | | + talk()        |
| + level_up()    | | + offer_quest() |
+-----------------+ +-----------------+
    ^       ^       ^
    |       |       |
+-------+ +-----+ +--------+
|Warrior| |Mage | | Archer |
+-------+ +-----+ +--------+
5. Przykładowe atrybuty i metody

* Stats:
 - strength: Siła
 - agility: Zwinność
 - endurance: Wytrzymałość
 - intelligence: Inteligencja
 - knowledge: Wiedza
 - luck: Szczęście
* Attributes:
 - health: Życie
 - stamina: Kondycja
 - mana: Mana
 - attack_power: Siła ataku
 - magic_power: Siła magii
 - dodge_chance: Szansa na unik
 - block_chance: Szansa na blok
 - health_regeneration: Regeneracja życia
 - stamina_regeneration: Regeneracja kondycji
 - mana_regeneration: Regeneracja many
* Metoda calculate_attributes() w klasie Character będzie obliczać atrybuty na
podstawie statystyk.
6. Przykładowe scenariusze użycia

* Opis przykładowych scenariuszy rozgrywki, np. walka z potworem, rozmowa z NPC,
eksploracja lokacji.
7. Konfiguracja i dane

* Opis formatu plików konfiguracyjnych i danych (np. config.json).
* Opis jak przechowywane są zapisy gry.
8. Funkcje pomocnicze

* Opis funkcji pomocniczych w utils/helpers.py.
9. Instrukcja uruchomienia

* Opis kroków potrzebnych do uruchomienia gry.