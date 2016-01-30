import sys
import pygame
import math
from Classes.Vector import Vector

NORMAL = 0
TURN_LEFT = 1
TURN_RIGHT = 2
SLOW = 4
FAST = 5
STOP = 3
FPS = 40
# dv = Vector((20, 20))
# RES_X = 800
# RES_Y = 800
Display = (800, 800)


class Ship:
    def __init__(self, pos):
        self.pos = Vector(pos)
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        # self.copyimage = self.image.copy()
        self.speed = Vector((0, 0))
        self.angle_speed = 5
        self.state = NORMAL
        self.direction = Vector((1, 0))

        self.draw()

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.state = TURN_LEFT
            if event.key == pygame.K_RIGHT:
                self.state = TURN_RIGHT
            if event.key == pygame.K_DOWN:
                self.state = SLOW
            if event.key == pygame.K_UP:
                self.state = FAST
            if event.key == pygame.K_ESCAPE:
                sys.exit()
        if event.type == pygame.KEYUP:
            self.state = NORMAL

    def update(self):
        if self.pos.x > Display[0]:
            self.pos = Vector((-50, self.pos.y))
        if self.pos.y > 850:
            self.pos = Vector((self.pos.x, -50))
        if self.pos.y < -50:
            self.pos = Vector((self.pos.x, 850))
        if self.pos.x < -50:
            self.pos = Vector((850, self.pos.y))

        if self.state == TURN_LEFT:
            self.speed.rotate(-self.angle_speed)
            # (Так не надо)self.image = pygame.transform.rotate(self.copyimage, self.angle + Angle)

        if self.state == TURN_RIGHT:
            self.speed.rotate(self.angle_speed)

        if self.state == FAST:
            if self.speed.len() == 0:
                self.speed = self.direction
            self.speed = self.speed + self.speed.normalize()
        if self.speed.len() == 0:
            return

        if self.state == SLOW:
            if self.speed.len() < 1:
                self.direction = self.speed
                self.speed = Vector((0, 0))

            else:
                self.speed = self.speed - self.speed.normalize()

        self.pos += self.speed

    def draw(self):
        pygame.draw.lines(self.image, (0, 0, 200), False, [(35, 20), (20, 15), (0, 0), (0, 40), (20, 25), (35, 20)])

    def render(self, screen):
        r = Vector(self.image.get_rect().center)  # r - центр фигуры для вектора направления
        rotate_image = pygame.transform.rotate(self.image, self.speed.angle)
        origin_rect = self.image.get_rect()
        rotate_rect = rotate_image.get_rect()
        rotate_rect.center = origin_rect.center
        rotate_rect.move_ip(self.pos.as_point())
        screen.blit(rotate_image, rotate_rect)
        pygame.draw.line(screen, (200, 255, 200), (self.pos + r).as_point(),
                         (self.pos + self.speed * 20 + r).as_point())
        pygame.draw.lines(self.image, (0, 0, 200), False, [(35, 20), (20, 15), (0, 0), (0, 40), (20, 25), (35, 20)])


pygame.init()
pygame.display.set_mode(Display)
screen = pygame.display.get_surface()

ship = Ship((400, 400))
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        ship.events(event)
        if event.type == pygame.QUIT:
            sys.exit()
    clock.tick(FPS)
    ship.update()
    screen.fill((100, 100, 100))
    ship.render(screen)
    pygame.display.flip()
