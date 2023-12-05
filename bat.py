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

    def draw(self):
        draw_rectangle(*self.get_bb())

    def handle_collision(self,group,other):
        if group == 'ball:bat':
            for Craw in self.The_bat.bat_list:
                game_world.remove_object(Craw)

    def get_bb(self):
        return self.x-self.size/2,self.y-self.size/2,self.x+self.size/2,self.y+self.size/2
    
class Bat:
    def __init__(self,x,y):
        self.rad=PI/2
        self.x,self.y=x,y
        self.list,self.radius=[6,6,6,6,8],[4,8,12,16,24]
        self.bat_list=[Craw_Bat(self,self.x,self.y,self.rad,self.list[i],self.radius[i]) for i in range(5)]
        game_world.add_object(self)

    def update(self):
        print(self.rad/PI)
        if self.rad<=8/3*PI:
            self.rad+=TIME_PER_ACTION*FRAME_PER_ACTION*game_framework.frame_time*3*PI/2#self.check_rad_v()
        else:
            return
        for Craw in self.bat_list:
            Craw.update()

    def draw(self):
        for Craw in self.bat_list:
            Craw.draw()