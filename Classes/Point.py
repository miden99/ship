import math
class Point:
    """
    Вспомогательный Класс для удобной работы с точками
    """
    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]

    def len(self, point_B):
        return math.sqrt((point_B.x - self.x)**2+(point_B.y - self.y)**2)

    def as_tuple(self):
        return self.x, self.y