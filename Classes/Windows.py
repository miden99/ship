import pygame
from pygame.locals import *

class Output_window(pygame.sprite.Sprite):
    title_height = 20
    border_thick = 3
    def __init__(self,x=0,y=0,widht=100,height=100,caption ="undefined"):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = widht
        self.height = height
        self.caption = caption
        self.text_list = []

        self.image = pygame.Surface((self.width, self.height+self.title_height), SRCALPHA) #Поверхность для отрисовки самого окна
        self.workspace = pygame.Surface((self.width, self.height),SRCALPHA) #Поверхность для отрисовки рабочей области окна

        pygame.draw.lines(self.image, (0,200,0),True,
            [(0,0),(self.width,0),(self.width,self.title_height),
                (0,self.title_height)],self.border_thick)
        pygame.draw.lines(self.image, (0,0,255),True,
            [(0,0),(self.width,0),(self.width,self.height),
                (0,self.height)],self.border_thick)

        # Заголовок окна
        font = pygame.font.SysFont("Courier New",12)
        text = font.render(self.caption, 2, (0, 0, 180))
        #textpos = text.get_rect()
        #textpos.centerx = background.get_rect().centerx
        self.image.blit(text, (5,5))

        self.title_rect = Rect(self.x,self.y,self.width,self.title_height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.drag = 0 # 0-drop 1-drag

    def event(self,event):
        mouseXY = pygame.mouse.get_pos()#[0]
        if event.type == 5 or event.type == 6:
            self.clear()
            self.render_text_list()
            pygame.draw.lines(self.image, (0,200,0),True,
                [(0,0),(self.width,0),(self.width,self.title_height),
                    (0,self.title_height)],self.border_thick)
            pygame.draw.lines(self.image, (0,0,255),True,
            [(0,0),(self.width,0),(self.width,self.height),
                (0,self.height)],self.border_thick)
            if self.title_rect.collidepoint(mouseXY):
                #print("on Window Title")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #print("Drag!")
                    self.drag = 1 #grag
                if event.type == pygame.MOUSEBUTTONUP:
                    #print("Drop")
                    self.drag = 0
        elif event.type == 4 and self.drag:
            self.move(event.dict["rel"])

    def move(self, rel):
        #print("rel = ",rel)
        self.x += rel[0]
        self.y += rel[1]
        self.rect.x = self.x
        self.rect.y = self.y

        self.title_rect.x = self.x
        self.title_rect.y = self.y

    def get_ws(self):
        """
        Возвращает Rect пабочей области
        """
        return Rect(0,0+self.title_height,self.width,self.title_height+self.height)

    def clear(self):
        """
        Очищает рабочую область окна
        """
        #Surface.fill(color, rect=None, special_flags=0)
        self.image.fill((255,255,255,0),self.get_ws())


    def render_text_list(self):
        font = pygame.font.SysFont("Courier New",14)
        y = 0
        for text in self.text_list:
            text = font.render(text, 2, (0, 0, 0))
            self.image.blit(text, (0+4,0+self.title_height+y))
            y += 14+2

    def add_text(self, new_text):
        self.text_list.append(new_text)