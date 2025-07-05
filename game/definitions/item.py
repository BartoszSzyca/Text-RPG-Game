from actors.entity import Entity

class Item(Entity):
    def __init__(self, name, description="_", item_type="misc", weight=0.1,
                 value=1, slot=None, stat_modifiers=None):
        super().__init__(name, description, weight)
        self.item_type = item_type
        self.value = value
        self.slot = slot
        self.stat_modifiers = stat_modifiers if stat_modifiers is not None else {}

    # def __str__(self):
    #     return f"{self.name} - {self.description} (Wartość: {self.value})"

class Weapon(Item):
    def __init__(self, name, description, damage, slot="main_hand",
                 stat_modifiers=None):
        super().__init__(name, description, item_type="weapon", slot=slot,
                         stat_modifiers=stat_modifiers)
        self.damage = damage

class Armor(Item):
    def __init__(self, name, description, armor_value, slot="chest",
                 stat_modifiers=None):
        super().__init__(name, description, item_type="armor", slot=slot,
                         stat_modifiers=stat_modifiers)
        self.armor_value = armor_value

class AmuletOfVigor(Item):
    def __init__(self, name, description, armor_value, slot="chest",
                 stat_modifiers=None):
        super().__init__(name, description, item_type="amulet", slot="amulet",
                         stat_modifiers=stat_modifiers)

class Potion(Item):
    def __init__(self, name, description, potion_type="healing",
                 effect_amount=0):
        super().__init__(name, description, item_type="potion")
        self.potion_type = potion_type
        self.effect_amount = effect_amount