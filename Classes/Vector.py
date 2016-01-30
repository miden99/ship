import pygame, math
from pygame.locals import *
import math


class Vector:
    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]

    def __add__(self, other):
        return Vector((self.x + other.x, self.y + other.y))

    def __repr__(self):
        return "v(%s,%s)" % (math.floor(self.x), math.floor(self.y))

    def __mul__(self, other):
        return Vector((self.x * other, self.y * other))

    def __floordiv__(self, other):
        return Vector((self.x / other, self.y / other))

    def __sub__(self, other):
        return Vector((self.x - other.x, self.y - other.y))

    def len(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        try:
            return Vector((self.x / self.len(), self.y / self.len()))
        except ZeroDivisionError:
            return Vector((0, 0))

    def update(self):
        pass

    def as_point(self):
        return self.x, self.y

    def rotate(self, angle):

        angle = math.radians(angle)
        x = self.x * math.cos(angle) - self.y * math.sin(angle)
        y = self.x * math.sin(angle) + self.y * math.cos(angle)
        self.x, self.y = x, y

    def render(self, screen):
        pygame.draw.line(screen, (250, 0, 0), (0, 0), (self.x, self.y))

    @property
    def angle(self):
        """
        возвращающий угол поворота вектора
        """
        try:
            return 360 - math.degrees(math.acos(self.x / self.len())) if self.y > 0 \
                else math.degrees(math.acos(self.x / self.len()))
        except ZeroDivisionError:
            return 0


if __name__ == "__main__":
    v1 = Vector((10, 10))
    v2 = Vector((20, 20))
    print(v1.normalize())
