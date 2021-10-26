class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False

    def __lt__(self, other):
        if self.x == other.x:
            return self.y <= other.y
        return self.x < other.x

    def __hash__(self):
        return self.y * 10000 + self.x

    def __str__(self):
        return f'{self.x}-{self.y}'
