class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def custom_add(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def change_sign(self):
        return Point(-1 * self.x, -1 * self.y)

    def compare(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def action(self, func, value):
        function_maps = {
            "add": self.custom_add,
            "compare": self.compare,
            "change sign": self.change_sign
        }

        return function_maps[func](value)