from pico2d import *
import math
rad=math.pi/180
from sdl2 import SDLK_DOWN, SDLK_SPACE
import game_framework
import game_world
import play_mode
from ball import Ball
from bat import Bat
import random
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
def is_swing(player,e):
    print('swing')
    return e[0]=='INPUT'and e[1].type==SDL_KEYDOWN and e[1].key==SDLK_SPACE

def is_not_arrive(player,e):
    return e[0]=='CHECK' and player.destination!=player.location

def is_arrive_(player,e):
    return e[0]=='CHECK' and player.destination==player.location

def mouse_in(player,e):
    in_x=player.location[0]>=e[1].x-player.size[0]/2 and player.location[0]<=e[1].x+player.size[0]/2
    in_y=player.location[1]>=800-e[1].y-1-player.size[0]/2 and player.location[1]<=800-e[1].y-1+player.size[0]/2
    return in_x and in_y

def is_click(player,e):
    if e[0]=='INPUT' and e[1].type==SDL_MOUSEBUTTONDOWN and mouse_in(player,e):
        player.base_dir*=-1
        play_mode.control.base.player_run(player)
        print(player.base_dir)
        return True
    return False

PIXEL_PER_METER=8.16
RUN_SPEED_KMPH=24
RUN_SPEED_MPM=(RUN_SPEED_KMPH*1000/60)
RUN_SPEED_MPS=(RUN_SPEED_MPM/60)
RUN_SPEED_PPS=(RUN_SPEED_MPS*PIXEL_PER_METER)

TIME_PER_ACTION=1
ACTION_PER_TIME=1/TIME_PER_ACTION
FRAME_PER_ACTION=10
PI=math.pi

class Run:
    @staticmethod
    def enter(player,e):
        print('Run')
        get_bt(player)

    @staticmethod
    def exit(player,e):
        pass
    
    @staticmethod
    def do(player):
        player.frame=(player.frame+ACTION_PER_TIME*FRAME_PER_ACTION*game_framework.frame_time)%3
        pass

    @staticmethod
    def draw(player):
        player.image.clip_composite_draw(int(player.frame)*16+player.sprite_p[0]+18,player.sprite_p[1]+12-player.sprite_option[1]*12+48,16,19,0,player.sprite_option[0],player.location[0],player.location[1],player.size[0],player.size[1])

class Hit:
    @staticmethod
    def enter(player,e):
        get_bt(player)
        player.swing=False
        player.frame=0
    
    @staticmethod
    def exit(player,e):
        pass

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        player.image.clip_composite_draw(0,488-72,16,32,0,'',player.location[0],player.location[1],player.size[0],int(4/3*player.size[1]))
        pass

class Hitting: #416 488
    @staticmethod
    def enter(player,e):
        get_bt(player)
        player.swing=True
        player.frame=0
    
    @staticmethod
    def exit(player,e):
        if player.bat!=None:
            player.delete_bat()
        pass

    @staticmethod
    def do(player):
        pass
            
    @staticmethod
    def draw(player):
        hitter_frame_left=[0,2,5,8,12,15] #draw용 좌측 벽
        hitter_size=[16,24,24,24,24,24] #hitter 이미지 사이즈
        relocate_hitter_frame_left=[0,0,-24,-24,-24,0] #다시 맞추기 용
        player.image.clip_composite_draw(hitter_frame_left[int(player.frame)]*8,488-72,hitter_size[int(player.frame)],32,0,'',player.location[0]-relocate_hitter_frame_left[int(player.frame)],player.location[1],int(player.size[0]*(hitter_size[int(player.frame)])/16),int(4/3*player.size[1]))
        pass


class Idle:
    @staticmethod
    def enter(player,e):
        print('idle')
        get_bt(player)
        player.frame=0

    @staticmethod
    def exit(player,e):
        pass
    
    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        player.image.clip_composite_draw(player.sprite_p[0],player.sprite_p[1]+24,16,20,0,player.sprite_option[0],player.location[0],player.location[1],player.size[0],player.size[1])
        pass
    

class StateMachine:
    def __init__(self,player):
        self.player=player
        self.cur_state=Idle
        self.state_table={
            Idle : {},
            Run : {is_click:Run},
            Hit:{is_swing:Hitting},
            Hitting:{}
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
                self.change_state(next_state,e)
                return True
        return False
    
    def change_state(self,next_state,e=None):
        self.cur_state.exit(self.player,e)
        self.cur_state=next_state
        self.cur_state.enter(self.player,e)       

class Batter:

    image=None                                      # sprite

    def __init__(self,x=400,y=0):
        self.image=load_image('Baseball_Players.png')

        self.location=[x,y]                         # 기본 좌표
        self.frame=0                                # 프레임
        self.sprite_option=['',1]                   # 'h': 왼쪽, '': 오른쪽, -1 : 다운, 1 : 업
        self.destination=[self.location[0],self.location[1]]            # 도착지점
        self.size=[24,32]                           # player draw 사이즈
        self.swing,self.is_click=False,False        # 스윙 유무
        self.hit_delay=0.7
        self.target_base=1
        self.bat=None
        self.check=False
        self.base_dir=1
        self.bt_list=[]
        self.build_behavior_tree()
        self.sprite_p=[0,320]
        self.state_machine=StateMachine(self)       # 상태머신 지정
        self.state_machine.start()                  # 상태머신 시작
        game_world.add_collision_pair('base:player',None,self)

    def handle_event(self,event):
        self.state_machine.handle_event(('INPUT',event))

    def update(self):
        self.state_machine.update()
        self.bt.run()

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def goto(self,destination): #지점 이동용 명령
        self.destination=[destination[0],destination[1]+self.size[1]//2]    

    def get_bb(self):
        return self.location[0]-self.size[0]//2,self.location[1]-self.size[1]//2,self.location[0]+self.size[0]//2,self.location[1]-self.size[1]//2+4

    def handle_collision(self,group,other):
        if group == 'base:player':
            pass

    def stop(self): # 익수들이 공을 잡은 후에 쓸 명령
        self.destination=[self.location[0],self.location[1]]

    # Action :
    def change_state_Idle(self):
        self.state_machine.change_state(Idle,('Change',0))
        return BehaviorTree.SUCCESS

    def change_state_Run(self):
        self.state_machine.change_state(Run,('Change',0))
        return BehaviorTree.SUCCESS

    def set_run_angle(self):
            self.rad=(math.atan2((self.destination[1]-self.location[1]),(self.destination[0]-self.location[0])))%(2*PI)
            return BehaviorTree.SUCCESS

    def is_less_than(self):
        return (self.destination[0]-self.location[0])**2+(self.destination[1]-self.location[1])**2<=(game_framework.frame_time*RUN_SPEED_PPS)**2
    
    def move_slightly_to(self):
        if not self.is_less_than():
            self.location[0]+=(game_framework.frame_time*RUN_SPEED_PPS)*math.cos(self.rad)
            self.location[1]+=(game_framework.frame_time*RUN_SPEED_PPS)*math.sin(self.rad)
            return BehaviorTree.SUCCESS
        else:
            self.location[0],self.location[1]=self.destination[0],self.destination[1]
            return BehaviorTree.SUCCESS

    def set_sprite_option(self):
        showed_list=[['',1],['h',1],['h',-1],['',-1]]
        i=int(self.rad//(PI/2))
        self.sprite_option=showed_list[i]
        return BehaviorTree.SUCCESS

    #Condition : 
    def is_arrive(self):
        if self.destination==self.location:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        
    def is_not_arrive(self):
        if self.destination!=self.location:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        
    def is_state_Idle(self):
        if self.state_machine.cur_state==Idle:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def is_state_Run(self):
        if self.state_machine.cur_state==Run:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def is_hitter_swing(self):
        print("is_hitter_swing")
        if self.swing:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
    
    def is_hitter_not_swing(self):
        if not self.swing:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def create_bat(self):
        self.t=get_time()
        self.bat=Bat(self.location[0]+(-6 if self.sprite_option[0]==''else 6),self.location[1])
        BehaviorTree.SUCCESS

    def do_hitting(self):
        self.frame=(self.frame+ACTION_PER_TIME*3*FRAME_PER_ACTION*game_framework.frame_time)
        if self.frame>=6:
            self.frame=5
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def set_waiting_time_and_time(self):
        self.time=get_time()
        return BehaviorTree.SUCCESS
    
    def check_time(self):
        if get_time()-self.time>=self.hit_delay:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
        
    def set_end_swing(self):
        self.swing=False
        return BehaviorTree.SUCCESS
    
    def delete_bat(self):
        if self.bat!=None:
            for Craw in self.bat.bat_list:
                game_world.remove_object(Craw)
            game_world.remove_object(self.bat)
            self.bat=None
        return BehaviorTree.SUCCESS
    
    def change_state_Hit(self):
        self.state_machine.change_state(Hit,('Change',0))
        return BehaviorTree.SUCCESS

    #define :
    def build_behavior_tree(self):
        a_s1=Action('상태를 Idle로 변경',self.change_state_Idle)
        a_s2=Action('상태를 Run으로 변경',self.change_state_Run)
        a_s4=Action('스윙 준비 자세로 변경',self.change_state_Hit)
        a_s2_1=Action('방향 설정',self.set_run_angle)
        a_s2_2=Action('방향에 따른 스프라이트 설정',self.set_sprite_option)
        a_s2_3=Action('조금씩 이동',self.move_slightly_to)
        a_s4_1=Action('스윙 시간 체크',self.set_waiting_time_and_time)
        a_s4_1_1=Action('충돌 박스 소환',self.create_bat)
        a_s4_2=Action('스윙 활동',self.do_hitting)
        a_s4_3=Action('스윙 쿨 체크',self.check_time)
        a_s4_4=Action('스윙 끝으로 셋팅',self.set_end_swing)
        a_s4_5=Action('충돌 박스 삭제',self.delete_bat)
        


        c1_1=Condition('도착하였는가',self.is_arrive)
        c1_2=Condition('도착하지 못하였는가',self.is_not_arrive)
        c_2_1=Condition('스윙 확인',self.is_hitter_swing)
        c_2_2=Condition('스윙 안하는지 확인',self.is_hitter_not_swing)
        c_s1=Condition('Idle인가',self.is_state_Idle)
        c_s2=Condition('Run인가',self.is_state_Run)
        c_s4=Condition('Hit인가',self.is_hitter_not_swing)

        self.SEQ_is_Idle=Sequence('Idle 상태인지 확인',c1_1,a_s1)
        self.SEQ_Idle=Sequence('기본상태작동',)

        self.SEQ_is_Run=Sequence('Run 상태인지 확인',c1_2,a_s2)
        self.SEQ_Run=Sequence('이동상태작동',a_s2_1,a_s2_2,a_s2_3)

        self.SEQ_is_Hit=Sequence('Hit 상태인지 확인',c_2_2,a_s4)
        self.SEQ_do_Hitting=Sequence('Hitting 활동',a_s4_1,a_s4_1_1,a_s4_2,a_s4_4,a_s4_3,a_s4_5,a_s4)

        self.SEL_set_Idle=Selector('Idle 상태 활동',self.SEQ_is_Run,self.SEQ_Idle)
        self.bt_list.append(BehaviorTree(self.SEL_set_Idle))
        self.SEL_set_Run=Selector('Run 상태 활동',self.SEQ_is_Idle,self.SEQ_Run)
        self.bt_list.append(BehaviorTree(self.SEL_set_Run))
        self.SEQ_set_Hit=Sequence('스윙 준비 상태 활동',self.SEQ_is_Run)
        self.bt_list.append(BehaviorTree(self.SEQ_set_Hit))
        self.SEL_set_Hitting=Sequence('스윙 중 상태 활동',self.SEQ_do_Hitting,self.SEQ_is_Hit)
        self.bt_list.append(BehaviorTree(self.SEL_set_Hitting))

        self.bt=BehaviorTree(self.SEL_set_Idle)    

def get_bt(player):
    if player.state_machine.cur_state==Idle:
        player.bt=player.bt_list[0]
    elif player.state_machine.cur_state==Run:
        player.bt=player.bt_list[1]
    elif player.state_machine.cur_state==Hit:
        player.bt=player.bt_list[2]
    elif player.state_machine.cur_state==Hitting:
        player.bt=player.bt_list[3]