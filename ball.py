from pico2d import load_image,draw_rectangle
import game_framework
import math
import play_mode
import random
def is_catch(ball):
    pass
def is_stopped(ball):
    return ball.pixel_v==0

def is_move(ball):
    return ball.pixel_v!=0
def is_passed(ball):
    return False
PIXEL_PER_METER=8.16
PI=math.pi
TIME_PER_ACTION=1
ACTION_PER_TIME=1/TIME_PER_ACTION
FRAME_PER_ACTION=200
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
        print('ball:move',ball.pixel_v)
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
        self.state_machine=StateMachine(self)
        self.pixel_v=shoot_v*self.set_v_1kmph()
        self.shoot_angle=angle
        self.x,self.y=x,y
        self.a=-4*8  # 1m/s^2*PIXEL_PER_METER=4.08 pixel
        self.height_a=-80
        self.height_v=30
        self.height=1.5*8.16 #meter   1.5*PIXEL_PER_METER
        self.state_machine.start()

    def update(self):
        self.state_machine.update()
        if self.height>0:
            self.height+=self.height_a*game_framework.frame_time
        else:
            self.heihgt=0
            self.a=-4*32
        self.height+=game_framework.frame_time*self.height_v
        if self.pixel_v>0:
            self.pixel_v+=self.a*game_framework.frame_time
        else:
            self.pixel_v=0
        self.x+=game_framework.frame_time*self.pixel_v*math.cos(self.shoot_angle)
        self.y+=game_framework.frame_time*self.pixel_v*math.sin(self.shoot_angle)
        

    
    def draw(self):
        self.image.clip_draw(0,0,68,68,self.x,self.y,4,4)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x-2,self.y-2,self.x+2,self.y+2
    
    def handle_collision(self,group,other):
        if group=='ball:bat':
            self.pixel_v=160*self.set_v_1kmph()
            self.shoot_angle=play_mode.control.players[-1].bat.angle+PI/2+PI*1/12*random.random()


    def set_v_1kmph(self):
        run_speed_KMPH=1
        run_speed_MPM=(run_speed_KMPH*1000/60)
        run_speed_MPS=(run_speed_MPM/60)
        run_speed_PPS=(run_speed_MPS*PIXEL_PER_METER)
        return run_speed_PPS

    