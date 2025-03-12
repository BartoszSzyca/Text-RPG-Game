class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def enter(self):
        print(f"Wchodzisz do {self.name}.")
        print(self.description)

    def exit(self):
        print(f"Opuszczasz {self.name}.")