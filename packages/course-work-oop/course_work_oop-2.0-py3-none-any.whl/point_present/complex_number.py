from src.point_present.point import Point


class ComplexNumber(Point):

    def __init__(self, x, y=0):
        super().__init__(x, y)

    def __str__(self):
        if self.x < 0:
            return f"{self.x}{self.y}j"
        else:
            return f"{self.x}+{self.y}j"

    def custom_add(self, other):
        return ComplexNumber(self.x + other.x, self.y + other.y)

    def change_sign(self):
        return ComplexNumber(-1 * self.x, -1 * self.y)

    def compare(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

