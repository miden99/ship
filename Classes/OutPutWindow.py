# -*- coding: utf-8 -*-
"""
Класс для создания вспомогательного окна.
Окно служит для вывода текущего значения любого свойства объектов в реальном времени
Пользоваться Классом довольно просто:
    1.Создайте экземпляр Класса (новый объект)
    2.Вызовите метод add_attr. Метод первым аргументом принимает ссылку на объект,
    а вторым - имя свойства (в виде строки), значение которого вы хотите отслеживать
    3.Незабудте вызвать метод render() для отрисовки окна

Демонстрация использования в demoOutPutWindow
"""
import pygame
class OutPutWindow:
    def __init__(self, coords=(0,0), font_size = 20, font_color = (255,0,0)):
        self.image = pygame.Surface((200,400), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = coords
        self.font = pygame.font.Font(None, font_size)
        self.font_color = font_color
        self.variables = {}

    def add_attr(self, obj_link, var_name):
        self.variables[var_name] = obj_link

    def update(self, dt):
        pass

    def event(self, event):
        pass

    def render(self, screen):
        temp_img = self.font.render(" ", 1, (0,0,0))
        step_y = temp_img.get_rect().height*1.2
        self.image.fill(pygame.SRCALPHA)
        for n, var in enumerate(self.variables.keys()):
            text = str(var)+" = "+str(getattr(self.variables[var], var))
            image = self.font.render(text, 1, self.font_color)
            self.image.blit(image, (0, step_y*n))

        screen.blit(self.image, self.rect)