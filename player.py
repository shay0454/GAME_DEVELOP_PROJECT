from pico2d import *
import math,random
from sdl2 import SDLK_DOWN, SDLK_SPACE
import game_framework
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from ball import Ball
def is_swing(player,e):
    return e[0]=='INPUT'and e[1].type==SDLK_DOWN and e[1].key==SDLK_SPACE

def is_click(player,e):
    return e[0]=='INPUT' and e[1].type==SDL_MOUSEBUTTONDOWN and player.x>=e[1].x-player.size[0]/2 and player.x<=e[1].x+player.size[0]/2 and player.y>=600-e[1].y-1-player.size[0]/2 and player.y<=600-e[1].y-1+player.size[0]/2

PIXEL_PER_METER=5.9 #미터 당 픽셀 : 5.9 pixel
RUN_SPEED_KMPH=24  #24km/h
RUN_SPEED_MPM=(RUN_SPEED_KMPH*1000/60)
RUN_SPEED_MPS=(RUN_SPEED_MPM/60)
RUN_SPEED_PPS=(RUN_SPEED_MPS*PIXEL_PER_METER)

TIME_PER_ACTION=1
ACTION_PER_TIME=1/TIME_PER_ACTION
FRAME_PER_ACTION=8

PI=math.pi
class Shoot:
    @staticmethod
    def enter(player,e):
        print('shoot')
        player.get_bt()
        player.frame=0
        player.is_setted=False
        player.is_shoot=False

    @staticmethod
    def exit(player,e):
        pass

    @staticmethod
    def do(player):
        pass

    def draw(player):
        player_temp=[0,2,4,6,8,11,14,16]
        player_size=[16,16,16,16,24,24,16,16,16]
        dif=[0,0,0,0,0,0,4,8]
        player.image.clip_composite_draw(player.sprite_p[0]+player_temp[int(player.frame)]*8,player.sprite_p[1]-24-dif[int(player.frame)]+160,player_size[int(player.frame)],24,0,'',player.x,player.y-dif[int(player.frame)],player.size[0]*(player_size[int(player.frame)])/24,player.size[1])


# Run : 이동 상태
class Run:
    @staticmethod
    def enter(player,e):
        player.get_bt()
        pass

    @staticmethod
    def exit(player,e):
        if is_click(player,e):  # 클릭했는가
            pass
        pass
    
    @staticmethod
    def do(player):
        player.frame=(player.frame+ACTION_PER_TIME*FRAME_PER_ACTION*game_framework.frame_time)%3
        pass

    @staticmethod
    def draw(player):
        player.image.clip_composite_draw(int(player.frame)*16+player.sprite_p[0]+18,player.sprite_p[1]+12-player.sprite_option[1]*12+48,16,20,0,player.sprite_option[0],player.x,player.y,player.size[0],player.size[1])
        pass


# Idle : 기본 상태      
class Idle:
    @staticmethod
    def enter(player,e):
        print('idle')  #
        player.get_bt()
        player.frame=0  # 프레임 초기화

    @staticmethod
    def exit(player,e):
        pass
    
    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        player.image.clip_composite_draw(player.sprite_p[0],player.sprite_p[1]+72,16,20,0,player.sprite_option[0],player.x,player.y,player.size[0],player.size[1])
        pass
    
class StateMachine:
    def __init__(self,player):
        self.player=player
        self.cur_state=Idle
        self.state_table={
            Idle : {},
            Run : {},
            Shoot:{}
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
                self.cur_state.exit(self.player,e)
                self.cur_state=next_state
                self.cur_state.enter(self.player,e)  
                return True
        return False
    
    def change_state(self,next_state,e):
        self.cur_state.exit(self.player,e)
        self.cur_state=next_state
        self.cur_state.enter(self.player,e)       

class Player:

    image=None                                      # sprite

    def __init__(self,x=400,y=0):
        self.x,self.y=x,y                           # 기본 좌표
        self.frame=0                                # 프레임
        self.sprite_option=['',1]                   # 'h': 왼쪽, '': 오른쪽,  -1 : 다운, 1 : 업
        self.destination=[self.x,self.y]            # 도착지점
        self.size=[32,24]                           # player draw 사이즈
        self.base=0
        self.base_dir=1
        self.bt_list=[]
        self.build_behavior_tree()
        self.sprite_p=[208,160]
        self.state_machine=StateMachine(self)       # 상태머신 지정
        self.state_machine.start()                  # 상태머신 시작

        if Player.image==None:
            Player.image=load_image('Baseball_Players.png')

    # 외부 이벤트 체크
    def handle_event(self,event):                           
        self.state_machine.handle_event(('INPUT',event))

    # 업데이트
    def update(self):                                       
        self.state_machine.update()                         # cur_state.do
        self.bt.run()

    # 현 상태에 따른 draw
    def draw(self):
        self.state_machine.draw()                           # cur_state.draw

    # 도착점 변경 함수
    def goto(self,destination):
        self.destination=destination    

    def fire_ball(self,cur_v,angle):
        ball=Ball(self.x,self.y,cur_v,angle)
        game_world.add_object(ball,3)
        game_world.add_collision_pair('ball:bat',ball,None)

    def get_bt(self):
        if self.state_machine.cur_state==Idle:
            self.bt=self.bt_list[0]
        elif self.state_machine.cur_state==Run:
            self.bt=self.bt_list[1]
        elif self.state_machine.cur_state==Shoot:
            self.bt=self.bt_list[2]

    # Action :
    def change_state_Idle(self):
        self.state_machine.change_state(Idle,('Change',0))
        return BehaviorTree.SUCCESS

    def change_state_Run(self):
        self.state_machine.change_state(Run,('Change',0))
        return BehaviorTree.SUCCESS

    def set_run_angle(self):
            self.rad=(math.atan2((self.destination[1]-self.y),(self.destination[0]-self.x)))%(2*PI)
            return BehaviorTree.SUCCESS

    def is_less_than(self):
        return (self.destination[0]-self.x)**2+(self.destination[1]-self.y)**2<=(game_framework.frame_time*RUN_SPEED_PPS)**2
    
    def move_slightly_to(self):
        if not self.is_less_than():
            self.x+=(game_framework.frame_time*RUN_SPEED_PPS)*math.cos(self.rad)
            self.y+=(game_framework.frame_time*RUN_SPEED_PPS)*math.sin(self.rad)
            return BehaviorTree.RUNNING
        else:
            self.x,self.y=self.destination[0],self.destination[1]
            return BehaviorTree.SUCCESS

    def set_sprite_option(self):
        showed_list=[['',1],['h',1],['h',-1],['',-1]]
        i=int(self.rad//(PI/2))
        self.sprite_option=showed_list[i]
        return BehaviorTree.SUCCESS


    #Condition : 
    def is_arrive(self):
        if self.destination==[self.x,self.y]:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        
    def is_not_arrive(self):
        if self.destination!=[self.x,self.y]:
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

    def is_not_shoot_setted(self):
        if not self.is_setted:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
    
    def set_waiting_time_and_time(self):
        self.is_setted=True
        self.waiting_time=random.randint(10,50)/10
        self.set_time=get_time()
        return BehaviorTree.SUCCESS
    
    def waiting_shoot(self):
        if get_time()-self.set_time>self.waiting_time:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def do_shoot(self):
        if not self.is_shoot:
            self.frame=(self.frame+ACTION_PER_TIME*FRAME_PER_ACTION*game_framework.frame_time)
            if self.frame>=8:
                self.frame=7
                self.is_shoot=True
                self.fire_ball(random.randint(90,140),270)
                return BehaviorTree.SUCCESS
            return BehaviorTree.RUNNING
        return BehaviorTree.SUCCESS
    #define :
    def build_behavior_tree(self):
        a_s1=Action('상태를 Idle로 변경',self.change_state_Idle)
        a_s2=Action('상태를 Run으로 변경',self.change_state_Run)
        a_s2_1=Action('방향 설정',self.set_run_angle)
        a_s2_2=Action('방향에 따른 스프라이트 설정',self.set_sprite_option)
        a_s2_3=Action('조금씩 이동',self.move_slightly_to)
        a_s3_1=Action('기다릴 시간 셋팅',self.set_waiting_time_and_time)
        a_s3_2=Action('기다림',self.waiting_shoot)
        a_s3_3=Action('슈팅',self.do_shoot)
        
        c1_1=Condition('도착하였는가',self.is_arrive)
        c1_2=Condition('도착하지 못하였는가',self.is_not_arrive)
        c_s1=Condition('Idle인가',self.is_state_Idle)
        c_s2=Condition('Run인가',self.is_state_Run)
        c_s3_1=Condition('Shoot 이미 활동하지 않았는가',self.is_not_shoot_setted)

        self.SEQ_is_Idle=Sequence('Idle 상태인지 확인',c1_1,a_s1)
        self.SEQ_Idle=Sequence('정지상태작동',)

        self.SEQ_is_Run=Sequence('Run 상태인지 확인',c1_2,a_s2)
        self.SEQ_Run=Sequence('Run 상태작동',a_s2_1,a_s2_2,a_s2_3)

        self.SEQ_is_Shoot=Sequence('Shoot 상태인지 확인',)
        self.SEQ_Shoot=Sequence('Shoot 상태작동',c_s3_1,a_s3_1,a_s3_2,a_s3_3)

        self.SEQ_set_Idle=Selector('Idle 상태 활동',self.SEQ_Idle,self.SEQ_is_Run)
        self.bt_list.append(self.SEQ_set_Idle)
        self.SEQ_set_Run=Selector('Run 상태 활동',self.SEQ_Run,self.SEQ_is_Idle)
        self.bt_list.append(self.SEQ_set_Run)
        self.SEQ_set_Shoot=Selector('Shoot 상태 활동',self.SEQ_Shoot)
        self.bt_list.append(self.SEQ_set_Shoot)
        self.SEL_check_state=Selector('상태확인',self.SEQ_set_Idle,self.SEQ_set_Run)

        self.bt=BehaviorTree(self.SEQ_set_Idle)