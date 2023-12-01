import game_world
from pico2d import draw_rectangle
class Ball_ground_location:
    def __init__(self,x,y):
        self.x,self.y=x,y

    def update(self):
        pass

    def draw(self):
        draw_rectangle(self.x-5,self.y-5,self.x+5,self.y+5)