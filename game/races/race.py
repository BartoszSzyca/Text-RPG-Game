class Race:
    def __init__(self, name, stat_bonuses=None, racial_abilities=None):
        self.name = name
        self.stat_bonuses = {"hp_modifier": 0}
        if stat_bonuses is not None:
            self.stat_bonuses.update(stat_bonuses)
        self.racial_abilities = racial_abilities if racial_abilities is not None else []

    def __str__(self):
        return self.name

class Human(Race):
    """
    Klasa reprezentująca rasę Człowieka.
    Charakteryzuje się zbalansowanymi statystykami i brakiem specjalnych słabości.
    """
    def __init__(self):
        super().__init__(
            name="Człowiek",
            stat_bonuses={
                "strength": 2,
                "agility": 2,
                "endurance": 2,
                "intelligence": 2,
                "wisdom": 2
            },
            racial_abilities=[]
        )

class Goblin(Race):
    def __init__(self):
        super().__init__(
            name="Goblin",
            stat_bonuses={
                "hp_modifier": -20,
                "strength": 2,
                "agility": 3,
                "endurance": 3,
                "intelligence": 1,
                "wisdom": 1
            },
            racial_abilities=["Widzenie w ciemności (częściowe)", "Zwinny Uciekinier"]
        )

class Drapieznik(Race):
    def __init__(self):
        super().__init__(
            name="Młody Skrzekliwy Leśny Drapieżnik",
            stat_bonuses={
                "hp_modifier": 10,
                "strength": 2,
                "agility": 4,
                "endurance": 4,
                "intelligence": 0,
                "wisdom": 0
            },
            racial_abilities=["Widzenie w ciemności", "Zwinny Uciekinier"]
        )


class ElfRace(Race):
    def __init__(self):
        super().__init__(
            name="Elf",
            stat_bonuses={
                "strength": 1,
                "agility": 3,
                "endurance": 1,
                "intelligence": 2,
                "wisdom": 3
            },
            racial_abilities=["Widzenie w ciemności (pełne)", "Odporność na urok", "Mistrzostwo w łucznictwie"]
        )
