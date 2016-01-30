import pygame
from Utilities.loads import load_image
from Classes.PyMain import PyMain

#Простой класс, для вывода работы с текстом
class Text:
    def __init__(self, text, color = (0,0,0), font = None, font_size = 24):
        self.text = text
        self.font = pygame.font.Font(font, font_size)
        self.color = color

    def render(self):
        """
        Возвращает картинку с текстом
        """
        return self.font.render(self.text, True, self.color)

# Базовый класс кнопки
class Button:  #основная кнопка
    def __init__(self, image_names, path='../Images/Buttons', pos=(0,0), function=None, text = 'Simple Button', w=0, h=0):
        self.images = {"normal": load_image(image_names[0], path=path, alpha_cannel=True),
                       "over": load_image(image_names[1], path=path, alpha_cannel=True),
                       "click": load_image(image_names[2], path=path, alpha_cannel=True)}
        self.status = "normal"                          #текущее состояние
        self.rect = self.images[self.status].get_rect()
        self.rect.topleft = pos
        self.text = Text(text).render()                 #Surf текста кнопки
        self.function = function                        #функция кнопки


    def event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.function:
                    self.function()
                self.status = 'click'

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                self.status ='over'

        elif event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.status = 'over'
            elif not self.rect.collidepoint(event.pos):
                self.status = 'normal'

    def update(self, dt):
        pass

    def render(self,screen):
        screen.blit(self.images[self.status], self.rect)
        #смещение текста на центр картинки кнопки
        rect_text_x = self.rect.x+self.rect.w/2-self.text.get_rect().w/2
        rect_text_y = self.rect.y+self.rect.h/2-self.text.get_rect().h/2
        screen.blit(self.text, (rect_text_x, rect_text_y))

#Расширенный класс кнопки, с "потухшим" состоянием после клика п ней.
class OffButton(Button):
    def __init__(self, image_names, path='../Images/Buttons', pos=(0,0), function=None, text = 'Simple Button', w=0, h=0):
        super().__init__(image_names, path, pos, function, text, w, h)
        self.images["clicked"] = load_image(image_names[-1], path=path, alpha_cannel=True)
        self.clicked = False

    def event(self,event):
        super().event(event)
        if self.status == 'click':
            self.clicked = True
        if self.status == 'normal' and self.clicked:
            self.status = 'clicked'




if __name__ == "__main__":
    main = PyMain(width=800, height=600)
    main.add_render_object(OffButton(image_names=('button_on.png', 'button_hover.png', 'button_click.png', 'button_off.png'), pos=(50,50)))
    main.add_render_object(Button(image_names=('button_on.png', 'button_hover.png', 'button_click.png'), pos=(350,50)))
    main.MainLoop(FPS=120)
