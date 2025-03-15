class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.npcs = []

    def enter(self):
        print(f"Wchodzisz do {self.name}.")
        print(self.description)

    def exit(self):
        print(f"Opuszczasz {self.name}.")

    def add_npc(self, npc):
        self.npcs.append(npc)

    def get_npcs(self):
        return self.npcs