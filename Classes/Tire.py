# -*- coding: utf-8 -*-
"""
Класс объекта покрышки (tire). Покрышка используется для создания гоночной трассы, как препятсвие.
"""
import pygame, os
from pygame.locals import *
from Utilities.loads import load_image
from  Classes.PyMain import PyMain

class Tire:
    def __init__(self, pos):
        self.image = load_image('584529.png', path='Images', alpha_cannel=True)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self, dt):
        pass

    def event(self, event):
        pass

    def render(self, screen):
        screen.blit(self.image,self.rect)


#if __name__ == "__main__":
#    mainWindow = PyMain(800,600)
#    tire01 = Tire((20,40))
#    tire02 = Tire((100,40))
#    mainWindow.add_render_object(tire01)
#    mainWindow.add_render_object(tire02)
#    mainWindow.MainLoop()