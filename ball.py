from pico2d import load_image
class Ball:
    def __init__(self):
        self.image=load_image('ball.png')

    def update(self):
        pass
    
    def draw(self):
        self.image.clip_draw(0,0,68,68,400,100,34,34)
    