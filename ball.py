from pico2d import load_image,draw_rectangle
import game_framework
import math
import play_mode
import random
def is_catch(ball):
    pass
def is_stopped(ball):
    return ball.v==0

def is_move(ball):
    return ball.v!=0
def is_passed(ball):
    return False
PIXEL_PER_METER=8.16
PI=math.pi
TIME_PER_ACTION=1
ACTION_PER_TIME=1/TIME_PER_ACTION
FRAME_PER_ACTION=200

ONE_KMPH=1
ONE_MPM=(ONE_KMPH*1000/60)
ONE_MPS=(ONE_MPM/60)
ONE_PPS=(ONE_MPS*PIXEL_PER_METER)
class Stopped:
    @staticmethod
    def enter(ball):
        print('stop')
        pass

    @staticmethod
    def exit(ball):
        pass

    @staticmethod
    def do(ball):
        pass

    @staticmethod
    def draw(ball):
        pass

class Moving:
    @staticmethod
    def enter(ball):
        print('ball:move',ball.v)
        pass

    @staticmethod
    def exit(ball):
        pass

    @staticmethod
    def do(ball):
        pass

    @staticmethod
    def draw(ball):
        pass

class Catched:
    @staticmethod
    def enter(ball):
        pass

    @staticmethod
    def exit(ball):
        pass

    @staticmethod
    def do(ball):
        pass

    @staticmethod
    def draw(ball):
        pass
class StateMachine:
    def __init__(self,ball):
        self.ball=ball
        self.cur_state=Moving
        self.state_table={
            Stopped : {is_catch:Catched,is_move:Moving},
            Moving:{is_stopped:Stopped},
            Catched:{is_passed:Moving}
        }

    def start(self):
        self.cur_state.enter(self.ball)

    def update(self):
        self.cur_state.do(self.ball)
        self.handle_event()

    def draw(self):
        self.cur_state.draw(self.ball)

    def handle_event(self):
        for ckeck_event, next_state in self.state_table[self.cur_state].items():
            if ckeck_event(self.ball):
                self.cur_state.exit(self.ball)
                self.cur_state=next_state
                self.cur_state.enter(self.ball)
                return True
        return False


class Ball:
    def __init__(self,x,y,shoot_v,angle):
        self.image=load_image('ball.png')
        self.shadow_image=load_image('ball_shadow.png')
        self.state_machine=StateMachine(self)
        self.v,self.static_v,self.h_v=shoot_v,shoot_v,shoot_v*3/4
        self.a,self.h_a=-5*8,-80
        self.distance=self.v*(self.v/(-self.a))/2
        self.shoot_angle,self.h_angle=angle,0
        self.x,self.y,self.h=x,y,12
        self.is_hit=False
        self.cur_state=0
        self.moving_state=['sky','allow','on_ground','stop']
        self.state_point=[]
        self.state_machine.start()

    def is_less_than(self):
        return (self.destination[0]-self.x)**2+(self.destination[1]-self.y)**2<=(game_framework.frame_time*ONE_PPS)**2

    def update(self):
        if self.is_hit:
            self.set_velocity_h()
            self.h+=game_framework.frame_time*ONE_PPS*self.h_v*math.sin(self.h_angle)
        self.set_velocity_xy()
        self.x+=game_framework.frame_time*ONE_PPS*self.v*math.cos(self.shoot_angle)*math.cos(self.h_angle)
        self.y+=game_framework.frame_time*ONE_PPS*self.v*math.sin(self.shoot_angle)*math.cos(self.h_angle)

    
    def draw(self):
        self.shadow_image.clip_draw(0,0,68,68,self.x,self.y,4,2)
        self.image.clip_draw(0,0,68,68,self.x,self.y+self.h,4,4)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x-2,self.y+self.h-2,self.x+2,self.y+self.h+2
    
    def handle_collision(self,group,other):
        if group=='ball:bat':
            if not self.is_hit:
                play_mode.control.state_machine.change_state(play_mode.control.state_list['Hitted'])
                self.shoot_angle=play_mode.control.runner[-1].bat.rad+PI/2+PI*1/12*random.random()
                play_mode.control.runner[-1].state_machine.change_state(play_mode.control.player_state_list['Idle'])
            self.v=random.randint(140,170)
            self.h_v=self.v*math.sin(random.randint(25,35))
            self.h_angle=PI/180*random.randint(25,35)
            self.is_hit=True

    def set_velocity_h(self):
        if self.h<0:
            self.h=0
            self.h_v*=-0.5 if (abs(self.h_v)>20)else 0
        else:
            self.h_v+=self.h_a*game_framework.frame_time
    
    def set_velocity_xy(self):
        if self.v<=0:
            self.v=0
        else:
            self.v+=self.a*game_framework.frame_time
    


    