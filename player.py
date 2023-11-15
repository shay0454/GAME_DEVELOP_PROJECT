from pico2d import *
import math
rad=math.pi/180
from sdl2 import SDLK_DOWN, SDLK_SPACE
import game_framework

def is_swing(player,e):
    return e[0]=='INPUT'and e[1].type==SDLK_DOWN and e[1].key==SDLK_SPACE

def is_arrive(player,e):
    return e[0]=='CHECK' and player.destination==[player.x,player.y]

def is_not_arrive(player,e):
    return e[0]=='CHECK' and player.destination!=[player.x,player.y]

def is_click(player,e):
    return e[0]=='INPUT' and e[1].type==SDL_MOUSEBUTTONDOWN and player.x>=e[1].x-player.size[0]/2 and player.x<=e[1].x+player.size[0]/2 and player.y>=600-e[1].y-1-player.size[0]/2 and player.y<=600-e[1].y-1+player.size[0]/2

PIXEL_PER_METER=5.9 #미터 당 픽셀 : 5.9 pixel
RUN_SPEED_KMPH=24  #24km/h
RUN_SPEED_MPM=(RUN_SPEED_KMPH*1000/60)
RUN_SPEED_MPS=(RUN_SPEED_MPM/60)
RUN_SPEED_PPS=(RUN_SPEED_MPS*PIXEL_PER_METER)

TIME_PER_ACTION=1
ACTION_PER_TIME=1/TIME_PER_ACTION
FRAME_PER_ACTION=100


# Run : 이동 상태
class Run:
    @staticmethod
    def enter(player,e):
        Run.set_run_angle(player)  #도착점에 따른 각도 초기화
        Run.set_sprite_showed(player)  #각도에 따른 스프라이트 변경

    @staticmethod
    def exit(player,e):
        if is_click(player,e):  # 클릭했는가
            pass
        pass
    
    @staticmethod
    def do(player,e=0):
        if is_arrive(player,e):
            player.state_machine.change_state(Idle,e)
        player.frame=(player.frame+ACTION_PER_TIME*FRAME_PER_ACTION*game_framework.frame_time)%3
        Run.set_next_position(player)
        pass

    @staticmethod
    def draw(player):
        player.image.clip_composite_draw(int(player.frame)*16+player.sprite_p[0]+18,player.sprite_p[1]+12-player.updown*12,16,20,0,player.face,player.x,player.y,player.size[0],player.size[1])
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

# Idle : 기본 상태      
class Idle:
    @staticmethod
    def enter(player,e):
        print('idle')  #
        player.frame=0  # 프레임 초기화

    @staticmethod
    def exit(player,e):
        pass
    
    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        player.image.clip_composite_draw(player.sprite_p[0],player.sprite_p[1]+24,16,20,0,player.face,player.x,player.y,player.size[0],player.size[1])
        pass
    
class StateMachine:
    def __init__(self,player):
        self.player=player
        self.cur_state=Idle
        self.state_table={
            Idle : {is_not_arrive:Run},
            Run : {is_click:Run, is_arrive:Idle}
        }

    def start(self):
        self.cur_state.enter(self.player,('START',0))

    def update(self):
        self.cur_state.do(self.player)

    def draw(self):
        self.cur_state.draw(self.player)

    def handle_event(self,e):
        for ckeck_event, next_state in self.state_table[self.cur_state].items():
            if ckeck_event(self.player,e):
                self.change_state(next_state,e)
                return True
        return False
    
    def change_state(self,next_state,e):
        self.cur_state.exit(self.player,e)
        self.cur_state=next_state
        self.cur_state.enter(self.player,e)       

class Player:

    image=None                                      # sprite

    def __init__(self,num=1):
        self.x,self.y=400,20                        # 기본 좌표
        self.frame=0                                # 프레임
        self.face=''                                #  'h': 왼쪽, '': 오른쪽
        self.updown=1                               #  -1 : 다운, 1 : 업
        self.team=num                               # 팀 지정
        self.state_machine=StateMachine(self,num)   # 상태머신 지정
        self.state_machine.start()                  # 상태머신 시작
        self.destination=[self.x,self.y]            # 도착지점
        self.size=[32,24]                           # player draw 사이즈
        self.base=0
        self.base_dir=0
        self.sprite_p=[208,160]
        if Player.image==None:
            Player.image=load_image('Baseball_Players.png')

    # 외부 이벤트 체크
    def handle_event(self,event):                           
        self.state_machine.handle_event(('INPUT',event))

    # 업데이트
    def update(self):                                       
        self.state_machine.update()                         # cur_state.do
        self.state_machine.handle_event(('CHECK',0))        # 내부 이벤트 (무입력) 체크

    # 현 상태에 따른 draw
    def draw(self):
        self.state_machine.draw()                           # cur_state.draw

    # 도착점 변경 함수
    def goto(self,destination):
        self.destination=destination    

