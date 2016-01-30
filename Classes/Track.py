import math, pygame
from Classes.Point import Point
class Create_Track:
    """
    Класс позволяющий создавать трассу
    """
    def __init__(self):
        self.click_coords = []
        self.points = []

    def event(self, event):
        #print("event")
        if event.type == pygame.MOUSEBUTTONUP:
            #print("mouse B D")
            self.get_track(event)

    def points_on_line(self, point_A, point_B, step):
        """
        Делим отрезок AB на равные отрезки длиной step.
        Возвращает список промежуточных точек(их координат), между point_A и point_B.
        Включая первую точку, последняя точка в списке отсутствует.
        Если нужна и последняя точка, раскомментируйте строку.
        """
        point_A = Point(point_A)
        point_B = Point(point_B)
        if point_B.len(Point((0,0)))<point_A.len(Point((0,0))):
            point_A, point_B = point_B, point_A
        try:
            alpha = math.atan((point_B.y-point_A.y)/(point_B.x - point_A.x))
        except ZeroDivisionError:
            alpha = math.radians(90)
        l_AB = point_A.len(point_B)
        print(alpha)
        steps = 0
        points = [point_A.as_tuple()]
        k=1
        while steps<l_AB-step:
            steps += step
            x = k*steps*math.cos(alpha)+point_A.x
            y = k*steps*math.sin(alpha)+point_A.y
            if point_B.len(Point((x,y)))>l_AB: #fixme: костыль!
                k = -1
                x = k*steps*math.cos(alpha)+point_A.x
                y = k*steps*math.sin(alpha)+point_A.y
            points.append((x,y))
        #points.append(point_B.as_tuple())
        #print("points = ", self.points)
        return points

    def get_track(self, event):
        """
        Добавляет в список render_list объекты "шины".
        Объекты располагаются между координатами двух кликов мыши, на расстоянии len_step друг от друга
        """
        #print("get_track")
        len_step = 40
        if self.click_coords:
            self.click_coords.append(event.pos)
            self.points = self.points_on_line(self.click_coords[0], self.click_coords[1], len_step)
            #for point in points:
            #    render_list.append(Tire(point))
            self.click_coords = []
        else:
            self.click_coords.append(event.pos)
