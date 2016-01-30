import pygame, sys
from pygame.locals import *
FPS = 40
class PyMain:
    """
    The Main PyMan Class - This class handles the main
    initialization and creating of the Game.
    v.0.2 (edit:20.05.2014)
    """
    
    def __init__(self, width=640,height=480):
        """Initialize"""
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        self.width = width
        self.height = height
        """Create the Screen"""
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.render_list = []
        self.none_render_list = []

    def add_render_object(self, obj):
        self.render_list.append(obj)

    def add_none_render_object(self, obj):
        self.none_render_list.append(obj)

    def addEventListener(self, obj, event_type):
        pass

    def MainLoop(self, FPS = FPS):
        """This is the Main Loop of the Game"""
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                for obj in self.render_list:
                    obj.event(event)
                for obj in self.none_render_list:
                    obj.event(event)
                if event.type == pygame.QUIT:
                    sys.exit()
            dt = clock.tick(FPS)
            self.screen.fill((0,0,0))
            for render_obj in self.render_list:
                render_obj.render(self.screen)
                render_obj.update(dt)


            pygame.display.flip()


#if __name__ == "__main__":
#    mainWindow = PyManMain(RES_X,RES_Y)
#    mainWindow.MainLoop()