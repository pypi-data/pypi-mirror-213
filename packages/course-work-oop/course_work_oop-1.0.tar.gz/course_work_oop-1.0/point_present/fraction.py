from point_present.point import Point


class Fraction(Point):

    def __init__(self, x, y):
        super().__init__(x, y)

    def __str__(self):
        return f"{self.x}/{self.y}"

    def custom_add(self, other):
        new_x = self.x * other.y + self.y * other.x
        new_y = self.y * other.y
        return Fraction(new_x, new_y)

    def change_sign(self):
        if self.x > 0 and self.y > 0:
            return f"{-1 *self.x}/{self.y}"
        else:
            return f"{-1 *self.x}/{-1*self.y}"

    def compare(self, other):
        return self.x * other.y == other.x * self.y



