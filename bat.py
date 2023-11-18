from pico2d import draw_rectangle
class Bat:
    def __init__(self):
        self.x,self.y=400,70
    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def handle_collision(self,group,other):
        if group == 'ball:bat':
            print(1)
            pass

    def get_bb(self):
        return self.x-10,self.y-10,self.x+10,self.y+10