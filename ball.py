from pico2d import load_image,draw_rectangle
import game_framework
import math
import play_mode
import random
def is_catch(ball):
    pass

PIXEL_PER_METER=5.9
PI=math.pi
TIME_PER_ACTION=1
ACTION_PER_TIME=1/TIME_PER_ACTION
FRAME_PER_ACTION=200
class Stopped:
    @staticmethod
    def enter(ball,e):
        pass

    @staticmethod
    def exit(ball,e):
        pass

    @staticmethod
    def do(ball):
        pass

    @staticmethod
    def draw(ball):
        pass

class Moving:
    @staticmethod
    def enter(ball,e):
        print('ball:move',run_speed_KMPH)
        pass

    @staticmethod
    def exit(ball,e):
        pass

    @staticmethod
    def do(ball):
        pass

    @staticmethod
    def draw(ball):
        pass

class Catched:
    @staticmethod
    def enter(ball,e):
        pass

    @staticmethod
    def exit(ball,e):
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
        self.cur_state=Stopped
        self.state_table={
            Stopped : {is_catch:Catched},
            Moving:{is_stopped:Stopped},
            Catched:{is_passed:Moving}
        }

    def start(self):
        self.cur_state.enter(self.ball)

    def update(self):
        self.cur_state.do(self.ball)

    def draw(self):
        self.cur_state.draw(self.ball)

    def handle_event(self):
        for ckeck_event, next_state in self.state_table[self.cur_state]:
            if ckeck_event(self.ball):
                self.cur_state.exit(self.ball)
                self.cur_state=next_state
                self.cur_state.enter(self.ball)
                return True
        return False


class Ball:
    def __init__(self,x,y,shoot_v,angle):
        global RUN_SPEED_KMPH
        self.image=load_image('ball.png')
        self.cur_state=Moving
        self.set_v(shoot_v)
        self.shoot_angle=angle
        self.x,self.y=x,y
        self.heigt=1.5 #meter
        self.cur_state.enter(self,None)

    def update(self):
        self.x+=game_framework.frame_time*run_speed_PPS*math.cos(self.shoot_angle)
        self.y+=game_framework.frame_time*run_speed_PPS*math.sin(self.shoot_angle)

    
    def draw(self):
        self.image.clip_draw(0,0,68,68,self.x,self.y,4,4)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x-2,self.y-2,self.x+2,self.y+2
    
    def handle_collision(self,group,other):
        if group=='ball:bat':
            self.shoot_angle=play_mode.control.players[-1].bat.angle+PI/2+PI*1/12*random.random()

    def set_v(self,v):
        global run_speed_KMPH,run_speed_PPS
        run_speed_KMPH=v
        run_speed_MPM=(run_speed_KMPH*1000/60)
        run_speed_MPS=(run_speed_MPM/60)
        run_speed_PPS=(run_speed_MPS*PIXEL_PER_METER)
    