class DC:
    def __init__(self, cap, id=1):
        self.id = id
        self.cap = cap
        self.load = 0

    def __str__(self):
        return str(self.id)