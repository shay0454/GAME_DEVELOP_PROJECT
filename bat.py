from pico2d import draw_rectangle
import game_framework
import game_world
import math
import random
PI=math.pi

PIXEL_PER_METER=8.16 #미터 당 픽셀 : 5.9 pixel

TIME_PER_ACTION=1
ACTION_PER_TIME=1/TIME_PER_ACTION
FRAME_PER_ACTION=8


class Craw_Bat:
    def __init__(self,The_bat,x,y,rad,size,radius):
        self.The_bat=The_bat
        self.x,self.y=self.The_bat.x+radius,self.The_bat.y
        self.rad=rad
        self.size=size
        self.radius=radius
        game_world.add_collision_pair('ball:bat',None,self)

    def update(self):
        self.rad=self.The_bat.rad
        self.x,self.y=self.The_bat.x+self.radius*math.cos(self.rad),self.The_bat.y+self.radius*math.sin(self.rad)
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())


    def handle_collision(self,group,other):
        if group == 'ball:bat':
            pass

    def get_bb(self):
        return self.x-self.size/2,self.y-self.size/2,self.x+self.size/2,self.y+self.size/2
    
class Bat:
    def __init__(self,x,y):
        self.x,self.y=x,y
        self.rad=PI/2
        self.list,self.radius=[4,4,4,4,8,8],[4,8,12,16,24,32]
        self.bat_list=[Craw_Bat(self,self.x,self.y,self.rad,self.list[i],self.radius[i]) for i in range(6)]
        game_world.add_object(self,3)

    def check_rad_v(self):
        for i in range(5):
            if self.rad>=self.rad_v[i] and self.rad<=self.rad_v[i+1]:
                return self.rad_v[i]

    def update(self):
        if self.rad<=8/3*PI:
            self.rad+=TIME_PER_ACTION*FRAME_PER_ACTION*game_framework.frame_time*3*PI/2#self.check_rad_v()
        else:
            return
        for Craw_bat in self.bat_list:
            Craw_bat.update()

    def draw(self):
        for Craw in self.bat_list:
            Craw.draw()