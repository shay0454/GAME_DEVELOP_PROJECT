from pico2d import *
import math
rad=math.pi/180
from sdl2 import SDLK_DOWN, SDLK_SPACE
import game_framework
import random
def is_swing(picker,e):
    return e[0]=='INPUT'and e[1].type==SDLK_DOWN and e[1].key==SDLK_SPACE

def be_hitter(picker,e):
    return e[0]=='INPUT' and picker.x==500 and picker.y==60

def is_hit(picker,e):
    return False

def is_not_arrive(picker,e):
    return picker.destination!=[picker.x,picker.y]

def is_not_hit(picker,e):
    return not is_hit(picker,e)

def is_catch(picker,e):
    pass

def is_not_catch(picker,e):
    return not is_catch(picker,e)


def is_arrive(picker,e):
    return picker.destination==[picker.x,picker.y]

def is_click(picker,e):
    if e[1]!=None and e[1].type==SDL_MOUSEBUTTONDOWN and picker.x>=e[1].x-picker.size[0]/2 and picker.x<=e[1].x+picker.size[0]/2 and picker.y>=600-e[1].y-1-picker.size[0]/2 and picker.y<=600-e[1].y-1+picker.size[0]/2:
        picker.destination,picker.pre_base=picker.pre_base,picker.destination
        if picker.base_dir==1:
            picker.base-=1
            picker.base_dir=-1
        else:
            picker.base+=1
            picker.base_dir=1
        print('click')
        return True
    return False

def is_ready_to_catch(picker,e):
    pass

PIXEL_PER_METER=5.9
RUN_SPEED_KMPH=24
RUN_SPEED_MPM=(RUN_SPEED_KMPH*1000/60)
RUN_SPEED_MPS=(RUN_SPEED_MPM/60)
RUN_SPEED_PPS=(RUN_SPEED_MPS*PIXEL_PER_METER)

TIME_PER_ACTION=1
ACTION_PER_TIME=1/TIME_PER_ACTION
FRAME_PER_ACTION=10

class Run:
    @staticmethod
    def enter(player,e):
        Run.set_run_angle(player)
        Run.set_sprite_showed(player)

    @staticmethod
    def exit(player,e):
        pass
    
    @staticmethod
    def do(player):
        player.frame=(player.frame+ACTION_PER_TIME*FRAME_PER_ACTION*game_framework.frame_time)%3
        Run.set_next_position(player)
        pass

    @staticmethod
    def draw(player):
        player.image.clip_composite_draw(int(player.frame)*16+player.sprite_p[0]+18,player.sprite_p[1]+12-player.updown*12+48,16,20,0,player.face,player.x,player.y,player.size[0],player.size[1])
        pass
    
    @staticmethod
    def set_run_angle(player):
        player.angle=(math.atan2((player.destination[1]-player.y),(player.destination[0]-player.x))/rad)%360

    @staticmethod
    def set_sprite_showed(player):
        if player.angle>=90 and player.angle<=270:
            player.face='h'
        else:
            player.face=''
        if player.angle>0 and player.angle<180:
            player.updown=1
        else:
            player.updown=-1

    @staticmethod
    def set_next_position(player):
        if((player.destination[0]-player.x)**2+(player.destination[1]-player.y)**2<=(game_framework.frame_time*RUN_SPEED_PPS)**2):
            player.x,player.y=player.destination[0],player.destination[1]
        else:
            player.x+=(game_framework.frame_time*RUN_SPEED_PPS)*math.cos(player.angle*rad)
            player.y+=(game_framework.frame_time*RUN_SPEED_PPS)*math.sin(player.angle*rad)
            
class Catch:
    @staticmethod
    def enter(picker,e):
        pass

    @staticmethod
    def exit(picker,e):
        pass

    def do(picker):
        pass

    def draw(picker):
        pass

class Shoot:
    @staticmethod
    def enter(picker,e):
        picker.frame=0
        picker.waiting_time=random.randint(5,50)/10
        picker.set_time=get_time()
        picker.shooted=False
        print('shoot')
        pass

    @staticmethod
    def exit(picker,e):
        pass

    @staticmethod
    def do(picker):
        if(get_time()-picker.set_time<picker.waiting_time):
            return
        if not picker.shooted:
            picker.frame=(picker.frame+ACTION_PER_TIME*FRAME_PER_ACTION*game_framework.frame_time)
            if picker.frame>=8:
                picker.shooted=True
                picker.frame=7

    def draw(picker):
        picker_temp=[0,2,4,6,8,11,14,16]
        picker_size=[16,16,16,16,24,24,16,16,16]
        dif=[0,0,0,0,0,0,4,8]
        picker.image.clip_composite_draw(picker.sprite_p[0]+picker_temp[int(picker.frame)]*8,picker.sprite_p[1]-24-dif[int(picker.frame)]+160,picker_size[int(picker.frame)],24,0,'',picker.x,picker.y-dif[int(picker.frame)],picker.size[0]*(picker_size[int(picker.frame)])/24,picker.size[1])


class Idle:
    @staticmethod
    def enter(picker,e):
        print('idle')
        picker.frame=0

    @staticmethod
    def exit(picker,e):
        pass
    
    @staticmethod
    def do(picker):
        pass

    @staticmethod
    def draw(picker):
        picker.image.clip_composite_draw(picker.sprite_p[0],picker.sprite_p[1]+72,16,20,0,picker.face,picker.x,picker.y,picker.size[0],picker.size[1])
        pass
    

class StateMachine:
    def __init__(self,picker):
        self.picker=picker
        self.cur_state=Idle
        self.state_table={
            Idle : {is_not_arrive: Run},
            Run : {is_click:Run, is_arrive:Idle,is_ready_to_catch:Catch},
            Catch:{is_catch:Idle, is_not_catch:Catch},
            Shoot:{}
        }

    def start(self):
        self.cur_state.enter(self.picker,('NONE',0))

    def update(self):
        self.cur_state.do(self.picker)

    def draw(self):
        self.cur_state.draw(self.picker)

    def handle_event(self,e):
        for ckeck_event, next_state in self.state_table[self.cur_state].items():
            if ckeck_event(self.picker,e):
                self.cur_state.exit(self.picker,e)
                self.cur_state=next_state
                self.cur_state.enter(self.picker,e)
                return True
        return False
    
    def change_state(self,next_state):
        self.cur_state.exit(self.picker,None)
        self.cur_state=next_state
        self.cur_state.enter(self.picker,None)

class Picker:

    image=None                                      # sprite

    def __init__(self):
        self.x,self.y=400,20                        # 기본 좌표
        self.frame=0                                # 프레임
        self.face=''                                #  'h': 왼쪽, '': 오른쪽
        self.updown=1                               #  -1 : 다운, 1 : 업
        self.state_machine=StateMachine(self)       # 상태머신 지정
        self.state_machine.start()                  # 상태머신 시작
        self.destination=[self.x,self.y]            # 도착지점
        self.size=[32,24]                           # picker draw 사이즈
        self.v=1                                    # picker 속도
        self.base=0
        self.base_dir=0
        self.sprite_p=[208,160]
        self.image=load_image('Baseball_Players.png')

    def handle_event(self,event):
        self.state_machine.handle_event(('INPUT',event))

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def goto(self,destination): #지점 이동용 명령
        self.destination=destination    

    def stop(self): # 익수들이 공을 잡은 후에 쓸 명령
        self.destination=[self.x,self.y]

