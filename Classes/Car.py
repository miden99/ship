import pygame, math
from pygame.locals import *
from Classes.Vector import Vector
from Classes.OutPutWindow import OutPutWindow
from Utilities import load_image
#statuses
STOP = 0
MOVE = 1
TURN_LEFT = 2
TURN_RIGHT = 3

class Game_Object:
    def __init__(self, coords=(0,0), speed=(0,0)):
        self.coords = Vector(coords)
        self.speed = Vector(speed)  #пикселей/сек
        self.max_speed = 100
        self.len_speed = self.speed.len()
        self.color = (250,0,0)
        self.acsel = Vector((0,0))
        self.len_acsel = self.acsel.len()
        self.d_acsel = 0            #Изменение ускорения, x пикс/сек
        self.friction = 0         #Сила трения
        self.status = STOP
        self.angle_speed = 40      #Угловая скорость, градусов/сек

    def event(self, event):
        """
        Обработка событий объектом
        """
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.status = TURN_RIGHT
            elif event.key == K_RIGHT:
                self.status = TURN_LEFT
            elif event.key == K_UP:
                self.d_acsel = +12
            elif event.key == K_DOWN:
                self.d_acsel = -6
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                self.status = MOVE
            elif event.key == K_RIGHT:
                self.status = MOVE
            elif event.key == K_UP or event.key == K_DOWN:
                self.d_acsel = 0

    def change_acselerate(self):
        self.acsel = self.speed.normalize()* (self.d_acsel + self.friction) #?
        self.len_acsel = self.acsel.len()

    def change_speed(self, dt):
        self.speed+= self.acsel*(dt/1000)
        self.len_speed = self.speed.len()
        #fixme: добавить ограничение на max_speed

    def move(self, dt):
        self.coords += (self.speed*(dt/1000))

    def update(self, dt):
        """
        Обновление состояния объкта (вызывается каждый кадр)
        """
        if self.status == TURN_LEFT:
            self.speed.rotate(self.angle_speed/1000*dt)
        elif self.status == TURN_RIGHT:
            self.speed.rotate(-self.angle_speed/1000*dt)
        self.change_acselerate()
        self.change_speed(dt)
        self.move(dt)

    def render(self, screen):
        center = self.coords.as_point()
        dx = 4
        dy = 4
        #cross
        pygame.draw.line(screen, (0,250,0), (self.coords.x, self.coords.y-dy),(self.coords.x, self.coords.y+dy))
        pygame.draw.line(screen, (0,250,0), (self.coords.x-dx, self.coords.y),(self.coords.x+dx, self.coords.y))

        pygame.draw.line(screen, self.color, (self.coords.as_point()),(self.coords+self.speed).as_point())
        pygame.draw.line(screen, (0,0,250), (self.coords.as_point()),(self.coords+self.acsel*2).as_point(),4)

class Game_Object_control(Game_Object):
    #def __init__(self):
    #    pass
    def event(self, event):
        '''
        обработка событий
        '''

        if event.type == pygame.KEYUP:    # или поднята
            if event.key in self.keys:
                if event.key == self.key_left or event.key == self.key_right: # то направление отсутствует
                    self.dir = None
                if event.key == self.key_up or event.key == self.key_down: # то ускорение отсутствует
                    self.dir_of_accel = None
                if event.key == self.key_fire: # то статус огня = False
                    self.press_button_fire = False
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            self.set_state(event)
            self.bin_mask()

    def set_state(self, event_key):
        """
        Функцию вызывать когда нажата/отпущена кнопка, event_key - событие нажатия кнопки
        Изменяет переменную keys_state в зависимости от нажатых кнопок
        Пример: Если нажаты функциональные кнопки вверх и влево, то keys_state = 0b10100
        """

        keys = [self.key_left, self.key_right, self.key_up, self.key_down, self.key_fire] #Список функциональных клавиш
        if event_key.key in keys: #Обрабатываем только нужные клавиши
            if event_key.type == pygame.KEYDOWN:
             self.keys_state = self.keys_state | (0b10000 >> keys.index(event_key.key))
            if event_key.type == pygame.KEYUP:
             self.keys_state = self.keys_state ^ (0b10000 >> keys.index(event_key.key))

    def bin_mask(self):
        """
        Проверка зажатых комбинаций кнопок, с использованием битовой маски
        На данный момент функция ничего не принимает и ничего не возвращает, реализуйте как вам удобнее
        """
        #global keys_state #используем глобальную переменную, в которой хранится состояние нажатых клавишь
        #Список используемых масок
        mask_left_right = 0b11000 #Если одновременно зажаты клавиши "лево" "право", состояние остальных не интересно
        mask_up_down = 0b00110
        mask_left = 0b10000
        mask_right = 0b01000
        mask_up = 0b00100
        mask_down = 0b00010
        mask_fire = 0b00001
        mask_left_up = 0b10100
        mask_left_down = 0b10010
        mask_right_up = 0b01100
        mask_right_down = 0b01010


        if self.keys_state & mask_left_right == mask_left_right:
            self.dir = None

        elif self.keys_state & mask_up_down == mask_up_down:
            self.dir_of_accel = None

        elif self.keys_state & mask_left == mask_left:
            self.dir = "left"

        elif self.keys_state & mask_right == mask_right:
            self.dir = "right"

        elif self.keys_state & mask_up == mask_up:
            self.dir_of_accel = "up"

        elif self.keys_state & mask_down == mask_down:
            self.dir_of_accel = "down"

        if self.keys_state & mask_left_up == mask_left_up:
            self.dir_of_accel = "up"
        elif self.keys_state & mask_right_up == mask_right_up:
            self.dir_of_accel = "up"

        if self.keys_state & mask_left_down == mask_left_down:
            self.dir_of_accel = "down"
        elif self.keys_state & mask_right_down == mask_right_down:
            self.dir_of_accel = "down"

        if self.keys_state & mask_fire == mask_fire:
            self.press_button_fire = True

    def event(self, event):
        '''
        обработка событий
        '''

        if event.type == pygame.KEYUP:    # или поднята
            if event.key in self.keys:
                if event.key == self.key_left or event.key == self.key_right: # то направление отсутствует
                    self.dir = None
                if event.key == self.key_up or event.key == self.key_down: # то ускорение отсутствует
                    self.dir_of_accel = None
                if event.key == self.key_fire: # то статус огня = False
                    self.press_button_fire = False
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            self.set_state(event)
            self.bin_mask()

class Car(Game_Object):
    def __init__(self, coords=(0,0), speed=(0,0)):
        Game_Object.__init__(self, coords=coords, speed=speed)
        self.image = load_image('yellow_car.png', path='Images', alpha_cannel=True)
        self.image = pygame.transform.rotate(self.image, -90)
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.track = None

    def move(self, dt):
        if self.track:
            temp_coords = self.coords
            Game_Object.move(self, dt)
            self.rect.center = self.coords.as_point()
            if self.rect.collidelist(self.track) != -1:
                #self.acsel = self.acsel*-1
                self.speed = Vector((0,0))
        else:
            Game_Object.move(self, dt)


    def add_track(self, track):
        self.track = track

    def render(self, screen):
        angle_of_rotate = math.degrees(math.acos(self.speed.normalize().x))
        #print(angle_of_rotate)

        if self.speed.y>0:
            angle_of_rotate = 360-angle_of_rotate

        rotated_img = pygame.transform.rotate(self.image, angle_of_rotate)
        rect_img = rotated_img.get_rect()
        rect_img.center = self.coords.as_point()  # центр картинки приравниваем вектору позиции
        screen.blit(rotated_img, rect_img) # блитуем все на скрин
        Game_Object.render(self, screen)


if __name__ == "__main__":
    from Classes.PyMain import PyMain
    mainWindow = PyMain(800,600)
    #vector = Game_Object((200,120),(30,0))
    car = Car((300,150),(30,0))
    trace = OutPutWindow((10,10))

    #mainWindow.add_render_object(vector)
    mainWindow.add_render_object(trace)
    mainWindow.add_render_object(car)

    #trace.add_attr(vector, "speed")
    #trace.add_attr(vector, "len_speed")
    #trace.add_attr(vector, "acsel",)
    #trace.add_attr(vector, "len_acsel")
    mainWindow.MainLoop()
