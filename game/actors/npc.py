from .character import Character
from .character import Attributes

class NPC(Character):
    def __init__(self, name, dialogue):
        super().__init__(name, None, None)
        self.dialogue = dialogue
        self.attributes = Attributes(100, 10, 0.1)

    def talk(self):
        print(self.dialogue)

    def __str__(self):
        return f"{self.name} (NPC)"