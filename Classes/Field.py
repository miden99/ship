class Field: #Поле, на котором все происходит
    def __init__(self,width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height

    def event(self, event):
        pass

    def update(self, screen):
        pass

if __name__ == '__main__':
    pass