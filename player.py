from pico2d import *
import math
rad=math.pi/180
from sdl2 import SDLK_DOWN, SDLK_SPACE
import game_framework

def is_swing(player,e):
    return e[0]=='INPUT'and e[1].type==SDLK_DOWN and e[1].key==SDLK_SPACE

def be_hitter(player,e):
    return e[0]=='INPUT' and player.x==500 and player.y==60

def is_hit(player,e):
    return e[0]=='INPUT' and e.key==SDLK_SPACE

def is_not_arrive(player,e):
    return player.destination!=[player.x,player.y]

def is_not_hit(player,e):
    return not is_hit(player,e)

def is_catch(player,e):
    pass

def is_not_catch(player,e):
    return not is_catch(player,e)

def is_out(player,e):
    pass

def is_arrive(player,e):
    return player.destination==[player.x,player.y]

def is_click(player,e):
    if e[1]!=None and e[1].type==SDL_MOUSEBUTTONDOWN and player.x>=e[1].x-player.size[0]/2 and player.x<=e[1].x+player.size[0]/2 and player.y>=600-e[1].y-1-player.size[0]/2 and player.y<=600-e[1].y-1+player.size[0]/2:
        player.destination,player.pre_base=player.pre_base,player.destination
        if player.base_dir==1:
            player.base-=1
            player.base_dir=-1
        else:
            player.base+=1
            player.base_dir=1
        print('click')
        return True
    return False

PIXEL_PER_METER=5.9
RUN_SPEED_KMPH=24
RUN_SPEED_MPM=(RUN_SPEED_KMPH*1000/60)
RUN_SPEED_MPS=(RUN_SPEED_MPM/60)
RUN_SPEED_PPS=(RUN_SPEED_MPS*PIXEL_PER_METER)

TIME_PER_ACTION=1
ACTION_PER_TIME=1/TIME_PER_ACTION
FRAME_PER_ACTION=100
class Hit: #416 488
    @staticmethod
    def enter(player,e):
        print('hitter')
        player.is_swing=False
        player.frame=0
    
    @staticmethod
    def exit(player,e):
        pass

    @staticmethod
    def do(player):
        if(is_swing[1]):
            player.is_swing=True
        if(player.is_swing):
            player.frame=(player.frame+ACTION_PER_TIME*FRAME_PER_ACTION*game_framework.frame_time)%6
            if player.frame==0:
                player.is_swing=False

    @staticmethod
    def draw(player):
        hitter_frame_left=[0,2,5,8,12,15] #draw용 좌측 벽
        hitter_size=[16,24,24,24,24,24] #hitter 이미지 사이즈
        relocate_hitter_frame_left=[24,24,0,0,0,24] #다시 맞추기 용
        player.clip_composite_draw(hitter_frame_left[int(player.frame)]*8,488-72,hitter_size[int(player.frame)],32,0,'',player.x-relocate_hitter_frame_left[player.frame],player.y,player.size[0]*(hitter_size[player.frame])/24,player.size[1])
        pass

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
            
class Idle:
    @staticmethod
    def enter(player,e):
        print('idle')
        player.frame=0

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
    def __init__(self,player,num):
        self.player=player
        self.cur_state=Idle
        self.state_table={
            Idle : {is_not_arrive: Run},
            Run : {is_click:Run, is_arrive:Idle}
        }

    def start(self):
        self.cur_state.enter(self.player,('NONE',0))

    def update(self):
        self.cur_state.do(self.player)

    def draw(self):
        self.cur_state.draw(self.player)

    def handle_event(self,e):
        for ckeck_event, next_state in self.state_table[self.cur_state].items():
            if ckeck_event(self.player,e):
                self.cur_state.exit(self.player,e)
                self.cur_state=next_state
                self.cur_state.enter(self.player,e)
                return True
        return False

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
        if num==1:
            self.sprite_p=[0,320]
        else:
            self.sprite_p=[208,160]
        if Player.image==None:
            Player.image=load_image('Baseball_Players.png')

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

