from .character import Character

class NPC(Character):
    def __init__(self, name, dialogue):
        super().__init__(name, None, None)
        self.dialogue = dialogue

    def talk(self):
        print(self.dialogue)

    def __str__(self):
        return f"{self.name} (NPC)"