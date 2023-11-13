from pico2d import *
class Field: #1024 1024
    
    def __init__(self):
        self.size=[1024,1024]
        self.image=load_image('SNES-Human_Baseball_JPN-Saitama.png')

    def update(self):
        pass
    
    def draw(self):
        self.image.clip_draw(0,0,self.size[0],self.size[1],400,450+50*10*(1.79-1)-30,int(self.size[0]*1.8),int(self.size[1]*1.8))
