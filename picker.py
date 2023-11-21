from pico2d import *
import math
rad=math.pi/180
from sdl2 import SDLK_DOWN, SDLK_SPACE
import game_framework
import game_world
from ball import Ball
import random
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

def is_not_arrive(player,e):
    return e[0]=='CHECK' and player.destination!=[player.x,player.y]

def is_catch(picker,e):
    pass

def is_not_catch(picker,e):
    pass

def is_arrive(player,e):
    return e[0]=='CHECK' and player.destination==[player.x,player.y]

def is_click(player,e):
    return e[0]=='INPUT' and e[1].type==SDL_MOUSEBUTTONDOWN and player.x>=e[1].x-player.size[0]/2 and player.x<=e[1].x+player.size[0]/2 and player.y>=600-e[1].y-1-player.size[0]/2 and player.y<=600-e[1].y-1+player.size[0]/2

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
        print('run')
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
        picker.get_bt()
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
                picker.fire_ball(random.randint(90,140),270)

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
        if not is_arrive(picker,('CHECK',0)):
            picker.state_machine.change_state(Run,('CHANGE',0))

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
                self.change_state(next_state,e)
                return True
        return False
    
    def change_state(self,next_state,e):
        self.cur_state.exit(self.picker,e)
        self.cur_state=next_state
        self.cur_state.enter(self.picker,e)       

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

    def fire_ball(self,cur_v,angle):
        ball=Ball(self.x,self.y,cur_v,angle)
        game_world.add_object(ball,3)
        game_world.add_collision_pair('ball:bat',ball,None)

    # Action :
    def change_state_Idle(self):
        self.state_machine.change_state(Idle,('Change',0))
        return BehaviorTree.SUCCESS

    def change_state_Run(self):
        self.state_machine.change_state(Run,('Change',0))
        return BehaviorTree.SUCCESS

    def set_run_angle(self):
            self.rad=(math.atan2((self.destination[1]-self.y),(self.destination[0]-self.x)))%(2*PI)

    def is_less_than(self):
        return (self.destination[0]-self.x)**2+(self.destination[1]-self.y)**2<=(game_framework.frame_time*RUN_SPEED_PPS)**2
    
    def move_slightly_to(self):
        if not self.is_less_than():
            self.x+=(game_framework.frame_time*RUN_SPEED_PPS)*math.cos(self.rad)
            self.y+=(game_framework.frame_time*RUN_SPEED_PPS)*math.sin(self.rad)
            BehaviorTree.RUNNING
        else:
            self.x,self.y=self.destination[0],self.destination[1]
            BehaviorTree.SUCCESS

    def set_sprite_showed(self):
        showed_list=[['',1],['h',1],['h',-1],['',-1]]
        i=int(self.rad//(PI/2))
        self.sprite_option=showed_list[i]
        BehaviorTree.SUCCESS


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

    #define :
    def build_behavior_tree(self):
        a_s1=Action('상태를 Idle로 변경',self.change_state_Idle)
        a_s2=Action('상태를 Run으로 변경',self.change_state_Run)
        a_s2_1=Action('방향 설정',self.set_run_angle)
        a_s2_2=Action('방향에 따른 스프라이트 설정',self.set_sprite_showed)
        a_s2_3=Action('조금씩 이동',self.move_slightly_to)

        c1_1=Condition('도착하였는가',self.is_arrive)
        c1_2=Condition('도착하지 못하였는가',self.is_not_arrive)
        c_s1=Condition('Idle인가',self.is_state_Idle)
        c_s2=Condition('Run인가',self.is_state_Run)




        self.SEQ_Run=Sequence('이동상태',a_s2_1,a_s2_2,a_s2_3)
        self.SEQ_Idle=Sequence('정지상태',)

        self.SEQ_set_Idle=Sequence('Idle 상태 확인',c1_1,a_s1,self.SEQ_Idle)
        self.SEQ_set_Run=Sequence('Run 상태 확인',c1_2,a_s2,self.SEQ_Run)

        self.SEL_check_state=Selector('상태확인',self.SEQ_set_Idle,self.SEQ_set_Run)

        root=self.test=Selector('상태',self.SEQ_set_Idle,self.SEQ_set_Run)
        self.bt=BehaviorTree(root)