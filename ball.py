from pico2d import load_image,draw_rectangle,get_time
import game_framework
import math
import play_mode
import game_world
import random
def is_catch(ball):
    pass
def is_stopped(ball):
    return ball.v==0
def is_hitted(ball):
    return ball.is_hit

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

class Ball_hit:
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
        }

    def start(self):
        self.cur_state.enter(self.ball)

    def update(self):
        self.cur_state.do(self.ball)

    def draw(self):
        self.cur_state.draw(self.ball)

    def change_state(self,next_state):
        self.cur_state.exit(self.ball)
        self.cur_state=next_state
        self.cur_state.enter(self.ball)

class Ball:
    a,h_a=-5*8,-100
    def __init__(self,x,y,shoot_v,angle,h_angle=0):
        self.image=load_image('ball.png')
        self.shadow_image=load_image('ball_shadow.png')
        self.state_machine=StateMachine(self)
        self.v,self.static_v,self.h_v=shoot_v*math.cos(h_angle),shoot_v,shoot_v*math.sin(h_angle)
        self.a,self.h_a=Ball.a,Ball.h_a
        self.shoot_angle,self.h_angle=angle,h_angle
        self.location,self.h=[x,y],12
        self.is_hit,self.is_touch_ground,self.check,self.is_stop=False,False,False,False
        self.cur_state=0
        self.moving_state=['sky','allow','on_ground','stop']
        self.state_point,self.times_when_ball_on_ground,self.distances_when_ball_on_ground,self.locations_when_ball_on_ground=[],[],[],[]
        self.state_machine.start()
        game_world.add_collision_pair('ball:defender',self,None)
        game_world.add_collision_pair('ball:bat',self,None)
        play_mode.control.ball=self
        if play_mode.control.state_machine.cur_state==play_mode.control.state_list['Catch']:
            self.is_hit=True

    def is_less_than(self):
        return (self.destination[0]-self.location[0])**2+(self.destination[1]-self.location[1])**2<=(game_framework.frame_time*ONE_PPS)**2

    def update(self):
        self.state_machine.update()
        self.update_z()
        self.update_xy()
    
    def draw(self):
        self.shadow_image.clip_draw(0,0,68,68,self.location[0],self.location[1],4,2)
        self.image.clip_draw(0,0,68,68,self.location[0],self.location[1]+self.h,4,4)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.location[0]-2,self.location[1]+self.h-2,self.location[0]+2,self.location[1]+self.h+2
    
    def handle_collision(self,group,other):
        if group=='ball:bat':
            if not self.check:
                self.is_hit=True
                play_mode.control.is_hit=True
                self.shoot_angle=other.rad+PI/2+PI*1/12*random.random()
                self.v=random.randint(140,170)        # 3차원 속도 설정
                self.h_angle=PI/180*random.randint(25,35)  # 높이 각도 설정
                self.h_v,self.v=self.v*math.sin(self.h_angle),self.v*math.cos(self.h_angle) # 높이 각도에 따른 xy평면과 y영역의 속도 설정
                self.check,self.stop=True,False
                self.calculate_times()
                self.calculate_distances()

        if group=='ball:defender':
            if self.h<=32:
                game_world.remove_object(self)
                play_mode.control.ball=None
                del self


    def update_xy(self):
        self.set_xy_velocity()
        self.location[0]+=game_framework.frame_time*ONE_PPS*self.v*math.cos(self.shoot_angle)
        self.location[1]+=game_framework.frame_time*ONE_PPS*self.v*math.sin(self.shoot_angle)

    def update_z(self):
        if self.is_hit:
            self.set_z_velocity()
            self.h+=game_framework.frame_time*ONE_PPS*self.h_v

    def set_z_velocity(self):
        if self.h<0:
            if not play_mode.control.is_ground:
                print('ground')
            play_mode.control.is_ground=True
            self.h=0
            self.h_v*=-0.5 if (abs(self.h_v/self.h_a)<abs(self.v/self.a))else 0
        else:
            self.h_v+=self.h_a*game_framework.frame_time
    
    def set_xy_velocity(self):
        self.v=self.v+self.a*game_framework.frame_time if self.v>0 else 0

    def calculate_times(self):
        self.time=get_time() # 실제 체크용 
        heighest_time=abs(self.h_v/self.h_a)  #처음때의 높이 최고점일 때 시간
        height_h=self.h_a/2*heighest_time**2+self.h_v*heighest_time+12 #최고점에서의 z 높이
        frist_on_ground_h_time=math.sqrt(abs(height_h/self.h_a*2))+heighest_time-0.07 #다시 내려올 때의 시간 + 최고점 시간
        self.times_when_ball_on_ground.append(frist_on_ground_h_time)
        v_on_ground=abs(self.h_a*(frist_on_ground_h_time-heighest_time))
        while v_on_ground*0.5>40: #0.5=탄성계수
            v_on_ground/=2
            self.times_when_ball_on_ground.append(abs(2*v_on_ground/self.h_a)+self.times_when_ball_on_ground[-1])
        self.times_when_ball_on_ground.append(abs(self.v/self.a))

    def calculate_distances(self):
        for t in self.times_when_ball_on_ground:
            distance=ONE_PPS*abs(self.a/2*t**2+self.v*t)
            location=[self.location[0]+distance*math.cos(self.shoot_angle),self.location[1]+distance*math.sin(self.shoot_angle)]
            self.distances_when_ball_on_ground.append(distance)
            self.locations_when_ball_on_ground.append(location)
    