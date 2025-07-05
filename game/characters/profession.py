class Profession:
    def __init__(self, name, stat_bonuses=None, abilities=None):
        self.name = name
        self.stat_bonuses = {"hp_modifier": 0}
        if stat_bonuses is not None:
            self.stat_bonuses.update(stat_bonuses)
        self.abilities = abilities if abilities is not None else []

class Warrior(Profession):
    def __init__(self):
        super().__init__(
            name="Wojownik",
            stat_bonuses={"hp_modifier": 20,"strength": 5,"agility": 2,"endurance": 4,},
            # abilities=["Potężne Uderzenie"]
        )