class Race:
    def __init__(self, name, base_stats):
        self.name = name
        self.base_stats = base_stats

    def __str__(self):
        return self.name
