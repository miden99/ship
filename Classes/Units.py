import pygame, os
from pygame.locals import *
from Utilities.loads import load_image


class BlueMan:
    def __init__(self, x, y,
                 time=200):  # time-частота смены кадров(в милисекундах). 200-Кадр меняется каждые 0,2 секунды

        self.x = x
        self.y = y
        self.speed = 5  # скорость (пикс/сек)
        self.action = 'stop'
        self.direction = 0  # Направление движения: 0-нет направления,1-вверх, 2-право, 3-вниз, 4-лево
        self.directions = ((0, 0), (0, -1), (1, 0), (0, 1), (-1, 0))

        self.sprites = [load_image('b_m_r01.png', path='../Images', alpha_cannel=True),
                        load_image('b_m_r02.png', path='../Images', alpha_cannel=True),
                        load_image('b_m_r03.png', path='../Images', alpha_cannel=True)]  # кадры анимации

        # набор свойств для анимации
        self.time = time
        self.work_time = 0
        self.skip_frame = 0
        self.frame = 0

    def handle_event(self, event):
        """
        Обработка всех событий
        """
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == K_UP:
                self.action = 'move'
                self.direction = 1
            if key == K_RIGHT:
                self.action = 'move'
                self.direction = 2
            if key == K_DOWN:
                self.action = 'move'
                self.direction = 3
            if key == K_LEFT:
                self.action = 'move'
                self.direction = 4
            elif event.type == pygame.KEYUP:
                self.action = 'stop'

    def move(self, dt):
        """
        Перемещение юнита
        """
        self.x += self.directions[self.direction][0] * self.speed * (dt / 100)
        self.y += self.directions[self.direction][1] * self.speed * (dt / 100)

    def update(self, dt):
        """
        Обновление состояния объекта. dt - сколько милисекунд прошло с прошлого вызова данного метода
        """
        # Перемещение
        if self.action == 'move':
            self.move(dt)

        # Анимация
        self.work_time += dt
        # Считаем сколько кадров надо перелистнуть
        skip_frame = self.work_time / self.time
        if skip_frame < 1:
            skip_frame = 0
        else:
            skip_frame = round(skip_frame)
        if skip_frame > 0:
            # Не забываем, что у нас, при смене кадров с частотой в
            # 100 мс, вполне могло уже пройти 133 мс, и важно не
            # забыть про эти 33 мс.
            self.work_time %= self.time
            self.frame += skip_frame
            if self.frame >= len(self.sprites):
                self.frame = 0

    def render(self, screen):
        screen.blit(self.sprites[self.frame], (self.x, self.y))