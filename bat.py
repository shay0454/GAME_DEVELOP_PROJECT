from pico2d import draw_rectangle
import game_framework
import game_world
import math

PI=math.pi

PIXEL_PER_METER=5.9 #미터 당 픽셀 : 5.9 pixel

TIME_PER_ACTION=1
ACTION_PER_TIME=1/TIME_PER_ACTION
FRAME_PER_ACTION=8


class Craw_Bat:
    def __init__(self,x,y,size,radius):
        self.ix,self.iy=x,y
        self.x,self.y=self.ix+radius,self.iy
        self.size=size
        self.radius=radius
        game_world.add_collision_pair('ball:bat',None,self)

    def update(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())


    def handle_collision(self,group,other):
        if group == 'ball:bat':
            print('bat_hit')
            del self
            pass

    def get_bb(self):
        return self.x-self.size/2,self.y-self.size/2,self.x+self.size/2,self.y+self.size/2
    
class Bat:
    def __init__(self,x,y):
        self.x,self.y=x,y
        self.angle=PI/2
        self.list=[5,5,5,5,7,10]
        self.radius=[5,8,11,14,20,25]
        self.bat_list=[Craw_Bat(self.x,self.y,self.list[i],self.radius[i]) for i in range(6)]
        self.angle_v=[PI/2,PI,PI*11/6,2*PI,2*PI+PI/4,2*PI+PI*5/4]

    def check_angle_v(self):
        for i in range(5):
            if self.angle>=self.angle_v[i] and self.angle<=self.angle_v[i+1]:
                return self.angle_v[i]

    def update(self):
        self.angle+=TIME_PER_ACTION*FRAME_PER_ACTION*game_framework.frame_time*3*PI/2#self.check_angle_v()
        for Craw in self.bat_list:
            Craw.x,Craw.y=self.x+Craw.radius*math.cos(self.angle),self.y+Craw.radius*math.sin(self.angle)

    def draw(self):
        for Craw in self.bat_list:
            Craw.draw()
