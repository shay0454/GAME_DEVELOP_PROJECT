from pico2d import load_image
class Field: #1024 1024
    def __init__(self):
        self.image=load_image('SNES-Human_Baseball_JPN-Saitama.png')

    def update(self):
        pass
    
    def draw(self):
        self.image.draw(400,450)