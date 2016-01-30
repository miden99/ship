import pygame,os, sys
from Utilities.loads import load_image
from Classes.PyMain import PyMain

CLICK = pygame.USEREVENT + 1
DBLCLICK = pygame.USEREVENT + 2
DBLC_TIME = 500 #максимальный промежуток между кликами - двойной клик
class Bar:
    def __init__(self, pos = (0,0), size = (20,20), color = (100,100,100)):
        self.image = None
        self.color = color
        self.rect = pygame.Rect(pos, size)
        self.draw()
        self.rect.move_ip(pos)
        self.drag = False # True - Объект захвачен мышью и будет перемещаться, False - не захвачен
        self.resizable = False # True - при перемещении мыши, объект будет менять свой размер
        self.last_mouse_event = None # Последее событие от мыши полученное объектом
        self.prev_click_time = None

    def draw(self):
        """
        Создаем поверхность, в зависимости от размера rect'а
        Рисуем элементы нашего объекта
        """
        self.image = pygame.Surface(self.rect.size)
        pygame.draw.rect(self.image, self.color, ((0,0), self.rect.size))
        w,h = 10,10 # resize_rect ширина и высота
        self.resize_rect = pygame.Rect(self.rect.w-w,self.rect.h -h,w,h)
        pygame.draw.rect(self.image, (0,0,200), self.resize_rect)

    def resize(self, rel):
        """
        Изменяем размеры нашего объекта
        """
        self.rect.width += rel[0]
        self.rect.height += rel[1]
        #Не даем уменьшить размер меньше области "ресайза"
        if self.rect.w < self.resize_rect.w:
            self.rect.w = self.resize_rect.w
            self.resizable = False
        if self.rect.h < self.resize_rect.h:
            self.rect.h = self.resize_rect.h
            self.resizable = False
        self.draw()

    def resize_ip(self, size):
        self.rect.size = size
        self.draw()

    def transfer_to_local(self, coords):
        """
        Переводит в локальные координаты объекта
        """
        return coords[0] - self.rect.x, coords[1] - self.rect.y

    def event(self, event):
        """
        Обрабатываем события
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.resize_rect.collidepoint(self.transfer_to_local(event.pos)):
                self.resizable = True
            elif self.rect.collidepoint(event.pos):
                self.drag = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.drag = self.resizable = False
        elif event.type == pygame.MOUSEMOTION:
            if self.drag:
                self.rect = self.rect.move(event.rel)
            elif self.resizable:
                self.resize(event.rel)
        elif event.type == CLICK:
            if event.target == self:
                pass
                print("CLICK on", self)
        elif event.type == DBLCLICK:
            if event.target == self:
                # print("DBL CLICK")
                self.resize_ip((40,40))

        self.custom_events(event)

    def custom_events(self, event):
        """
        Создаем собственные события, если они произошли
        """
        # Отлавливаем событие "Двойной Клик"
        if event.type == CLICK:
            if event.target == self:
                if not self.prev_click_time:
                    self.prev_click_time = pygame.time.get_ticks()
                elif pygame.time.get_ticks() - self.prev_click_time < DBLC_TIME:
                    dbclickevent = pygame.event.Event(DBLCLICK, pos=event.pos, target = self)
                    pygame.event.post(dbclickevent)
                    self.prev_click_time = None
                else:
                    self.prev_click_time = pygame.time.get_ticks()

        # Отлавливаем сбытие "Клик" на нашем объекте
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                if self.last_mouse_event == pygame.MOUSEBUTTONDOWN and event.type == pygame.MOUSEBUTTONUP:
                    clickevent = pygame.event.Event(CLICK, pos=event.pos, target = self)
                    pygame.event.post(clickevent)
            self.last_mouse_event = event.type
        elif event.type == pygame.MOUSEMOTION:
            self.last_mouse_event = event.type

    def update(self, dt):
        """
        Обновляем состояние(местоположение, угол поворота и т.п.) объекта
        Этот метод должен вызываться перед отрисовкой каждого кадра
        Как правило, из данного метода вызываются другие методы, которые изменяют нужное состояние объекта
        """
        pass

    def render(self, screen):
        """
        Отрисовываем объект на поверхность screen
        """
        screen.blit(self.image, self.rect)

if __name__ == "__main__":
    main = PyMain(width=800, height=600)
    main.add_render_object(Bar(pos=(50,50), size=(50,50)))
    main.add_render_object(Bar(pos=(120,150), size=(60,60)))
    main.MainLoop(FPS=120)