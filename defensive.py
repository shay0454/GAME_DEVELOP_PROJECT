from pico2d import *
import math,random
from sdl2 import SDLK_DOWN, SDLK_SPACE
import game_framework
import game_world
import play_mode
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from ball import Ball
def is_less_than_ball(player,b_location,gap):
    return ((b_location[0]-player.location[0])**2+(b_location[1]-player.location[1])**2<=(gap)**2)

def check_near_in_ball(player):
    if play_mode.control.ball!=None:
        if is_less_than_ball(player,play_mode.control.ball.location,9*PIXEL_PER_METER):
            player.goto(play_mode.control.ball.location)

def lower_than_player(player,height):
    return player.size[1]>height

def do_out_batter(control):
    control.out_list.append(control.batter[0])
    if control.batter[0] in control.runners:
        control.runners.remove(control.batter[0])
    control.player_stop(control.batter[0])

def set_field_control_Catch(control):
    if control.state_machine.cur_state==control.state_list['Hitted']:
        control.state_machine.change_state(control.state_list['Catch'])

def set_field_control_End(control):
    if control.state_machine.cur_state==control.state_list['Start']:
        control.state_machine.change_state(control.state_list['End'])   

def set_player_catch_the_ball(player):
    player.ball_picked=True
    if player.state_machine.cur_state!=The_Catcher:
        player.state_machine.change_state(Catch,('CHANGE',0))

PIXEL_PER_METER=8.16

PI=math.pi
is_check=False
class Catch:
    @staticmethod
    def enter(player,e):
        player.get_bt()
        player.catch_time=get_time()
        player.stop()
        if not play_mode.control.is_ground:
            play_mode.control.out_list+=[*play_mode.control.batter]
        player.frame=0
    
    @staticmethod
    def exit(player,e):
        pass

    @staticmethod
    def do(player):
        player.frame=(player.frame+player.ACTION_PER_TIME*player.FRAME_PER_ACTION*game_framework.frame_time*1/2)
        pass

    @staticmethod
    def draw(player):
        player.image.clip_composite_draw(player.sprite_p[0]+96,player.sprite_p[1]+72,16,24,0,'',player.location[0],player.location[1],player.size[0],player.size[1])

class The_Catcher:
    @staticmethod
    def enter(player,e):
        player.get_bt()
        player.frame=0
        pass

    @staticmethod
    def exit(player,e):
        pass

    @staticmethod
    def do(player):
        if not player.ball_picked:
            return
        if player.frame<2:
            player.frame=(player.frame+player.ACTION_PER_TIME*player.FRAME_PER_ACTION*game_framework.frame_time*1/2)
        else:
            player.time=get_time()
            print('strike')
            play_mode.control.is_strike=True
            player.ball_picked=False
            if get_time()-player.time>1:
                player.frame=0

    @staticmethod
    def draw(player):
        player.image.clip_composite_draw(int(player.frame)*16+player.sprite_p[0]+160,player.sprite_p[1]+72,16,24,0,'',player.location[0],player.location[1],player.size[0],player.size[1])

class Ready_to_Shoot:
    @staticmethod
    def enter(player,e):
        player.get_bt()
        player.frame=0

    @staticmethod
    def exit(player,e):
        pass

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        player_temp=[0,2,4,6,8,11,14,16]
        player_size=[16,16,16,16,24,24,16,16,16]
        dif=[0,0,0,0,0,0,4,8]
        player.image.clip_composite_draw(player.sprite_p[0]+player_temp[int(player.frame)]*8,player.sprite_p[1]-24-dif[int(player.frame)]+160,player_size[int(player.frame)],23,0,'',player.location[0],player.location[1]-dif[int(player.frame)],player.size[0]*(player_size[int(player.frame)])/16,player.size[1])

class Shoot:
    @staticmethod
    def enter(player,e):
        player.get_bt()
        player.frame=0
        player.already_shoot=True

    @staticmethod
    def exit(player,e):
        pass

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        player_temp=[0,2,4,6,8,11,14,16]
        player_size=[16,16,16,16,24,24,16,16,16]
        dif=[0,0,0,0,0,0,4,8]
        player.image.clip_composite_draw(player.sprite_p[0]+player_temp[int(player.frame)]*8,player.sprite_p[1]-24-dif[int(player.frame)]+160,player_size[int(player.frame)],23,0,'',player.location[0],player.location[1]-dif[int(player.frame)],player.size[0]*(player_size[int(player.frame)])/16,player.size[1])


# Run : 이동 상태
class Run:
    @staticmethod
    def enter(player,e):
        player.get_bt()
        pass

    @staticmethod
    def exit(player,e):
        pass
    
    @staticmethod
    def do(player):
        if player.role=='fielder'or player.role=='picker':
            check_near_in_ball(player)
        player.frame=(player.frame+player.ACTION_PER_TIME*player.FRAME_PER_ACTION*game_framework.frame_time)%3
        pass

    @staticmethod
    def draw(player):
        player.image.clip_composite_draw(int(player.frame)*16+player.sprite_p[0]+18,player.sprite_p[1]+12-player.sprite_option[1]*12+48,16,19,0,player.sprite_option[0],player.location[0],player.location[1],player.size[0],player.size[1])
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
        if player.role=='fielder':
            check_near_in_ball(player)
        pass

    @staticmethod
    def draw(player):
        player.image.clip_composite_draw(player.sprite_p[0],player.sprite_p[1]+72,16,20,0,player.sprite_option[0],player.location[0],player.location[1],player.size[0],player.size[1])
        pass
    
class StateMachine:
    def __init__(self,player):
        self.player=player
        self.cur_state=Idle
        self.state_table={
            Idle : {},
            Run : {},
            Shoot:{},
            Catch:{},
            The_Catcher:{}
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
    check_tf=False
    def __init__(self,role='defender',x=400,y=0):
        self.location=[x,y]                           # 기본 좌표
        self.frame=0                                # 프레임
        self.role=role
        self.sprite_option=['',1]                   # 'h': 왼쪽, '': 오른쪽,  -1 : 다운, 1 : 업
        self.destination=[self.location[0],self.location[1]]            # 도착지점
        self.size=[24,32]                           # player draw 사이즈
        self.base=0
        self.base_dir=1
        self.already_shoot=False
        self.ball_picked=False
        self.set_pps()
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
        draw_rectangle(*self.get_bb())

    def stop(self):
        self.destination=self.location
        
    def get_bb(self):
        return self.location[0]-self.size[0]//2,self.location[1]-self.size[1]//2,self.location[0]+self.size[0]//2,self.location[1]+self.size[1]//2
    
    def get_bool_is_batter_out(self,ball):
        return not ball.is_touch_ground and  self!=play_mode.control.basemen[0]
    
    def handle_collision(self,group,other):
        if group=='ball:the_catcher':
            self.ball_picked=True
            play_mode.control.is_strike=True
        elif group=='ball:defender'or group=='ball:baseman':
            if lower_than_player(self,other.h):
                set_player_catch_the_ball(self)

                

    # 도착점 변경 함수
    def goto(self,destination):
        self.destination=[destination[0],destination[1]+self.size[1]//2]    

    def fire_ball(self,cur_v,angle,h_angle=0):
        if play_mode.control.ball!=None:
            return
        ball=Ball(self.location[0],self.location[1],cur_v,angle,h_angle)
        game_world.add_object(ball,3)
        game_world.add_collision_pair('ball:bat',ball,None)

    def set_pps(self):
        self.RUN_SPEED_KMPH=24  #24km/h
        self.RUN_SPEED_MPM=(self.RUN_SPEED_KMPH*1000/60)
        self.RUN_SPEED_MPS=(self.RUN_SPEED_MPM/60)
        self.RUN_SPEED_PPS=(self.RUN_SPEED_MPS*PIXEL_PER_METER)

        self.TIME_PER_ACTION=1
        self.ACTION_PER_TIME=1/self.TIME_PER_ACTION
        self.FRAME_PER_ACTION=8

    def get_bt(self):
        if self.state_machine.cur_state==Idle:
            self.bt=self.bt_list[0]
        elif self.state_machine.cur_state==Run:
            self.bt=self.bt_list[1]
        elif self.state_machine.cur_state==Ready_to_Shoot:
            self.bt=self.bt_list[2]
        elif self.state_machine.cur_state==Shoot:
            self.bt=self.bt_list[3]
        elif self.state_machine.cur_state==The_Catcher:
            self.bt=self.bt_list[4]
        elif self.state_machine.cur_state==Catch:
            self.bt=self.bt_list[5]

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

    def is_less_than(self,gap):
        return (self.destination[0]-self.location[0])**2+(self.destination[1]-self.location[1])**2<=(gap)**2

#도착지로 조금씩 이동
    def move_slightly_to(self):
        if not self.is_less_than(game_framework.frame_time*self.RUN_SPEED_PPS):
            self.location[0]+=(game_framework.frame_time*self.RUN_SPEED_PPS)*math.cos(self.rad)
            self.location[1]+=(game_framework.frame_time*self.RUN_SPEED_PPS)*math.sin(self.rad)
            return BehaviorTree.SUCCESS
        else:
            self.location=[*self.destination]
            return BehaviorTree.SUCCESS


# 방향에 맞는 스프라이트 셋팅
    def set_sprite_option(self):
        showed_list=[['',1],['h',1],['h',-1],['',-1]]
        i=int(self.rad//(PI/2))
        self.sprite_option=showed_list[i]
        return BehaviorTree.SUCCESS

#베이스 찾기
    def find_base(self):
        self.base_for_shoot=play_mode.control.find_base()
        if self.base_for_shoot==-1:
            self.state_machine.change_state(Idle,('CHANGE',0))
            return BehaviorTree.FAIL
        self.destination=play_mode.control.base_locations[self.base_for_shoot]
        return BehaviorTree.SUCCESS
    
    def check_base(self):
        if self.is_less_than(PIXEL_PER_METER*12):
            self.state_machine.change_state(Idle,('CHANGE',0))
            return BehaviorTree.FAIL
        else:
            return BehaviorTree.SUCCESS

#베이스 각도 설정
    def set_angle_base_for_shoot(self):
        location=play_mode.control.base_locations[self.base_for_shoot]
        location[1]+=12
        self.rad=math.atan2(location[1]-self.location[1],location[0]-self.location[0])
        self.base_distance=math.sqrt((location[1]-self.location[1])**2+(location[0]-self.location[0])**2)
        return BehaviorTree.SUCCESS

    def set_v_to_base(self):
        self.h_v=240
        self.t_=abs(2*self.h_v/Ball.h_a)
        self.ball_v=self.base_distance/self.t_-1/2*Ball.a*self.t_
        return BehaviorTree.SUCCESS
#   
    def do_pass(self):
        self.fire_ball(self.ball_v,self.rad,0)
        self.ball_picked=False
        return BehaviorTree.SUCCESS

    def set_point(self):
        return BehaviorTree.SUCCESS 
    
    def reset_collsion(self):
        game_world.remove_collision_object(self)

        return BehaviorTree.SUCCESS
    
    def check_ball(self):
        if play_mode.control.ball==None:
            game_world.add_collision_pair('ball:defender',None,self)
            return BehaviorTree.SUCCESS
        if not is_less_than_ball(self,play_mode.control.ball.location,48):
            game_world.add_collision_pair('ball:defender',None,self)
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL
    
    #Condition : 
    def is_frame_over_catch(self):
        if self.frame>=4:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        
    def is_arrive(self):
        if self.destination==[self.location[0],self.location[1]]:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        
    def is_not_arrive(self):
        if self.destination!=[self.location[0],self.location[1]]:
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

    def is_not_already_shoot(self):
        if not self.already_shoot:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        
    def set_waiting_time_and_time(self):
        self.waiting_time=random.randint(10,20)/10
        self.set_time=get_time()
        return BehaviorTree.SUCCESS
    
    def waiting_shoot(self):
        if get_time()-self.set_time>self.waiting_time:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def do_shoot(self):
        self.frame=(self.frame+self.ACTION_PER_TIME*self.FRAME_PER_ACTION*game_framework.frame_time)
        if self.frame>=8:
            self.frame=7
            self.is_shoot=True        
            self.fire_ball(random.randint(120,170),PI*3/2)
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING
    
    def change_state_Ready_to_Shoot(self):
        self.state_machine.change_state(Ready_to_Shoot,('Change',0))
        return BehaviorTree.SUCCESS
    
    def change_state_Shoot(self):
        self.state_machine.change_state(Shoot,('Change',0))
        return BehaviorTree.SUCCESS

    #define :
    def build_behavior_tree(self):
        a_0=Action('체크 포인트',self.set_point)
        a_s1=Action('상태를 Idle로 변경',self.change_state_Idle)
        a_s2=Action('상태를 Run으로 변경',self.change_state_Run)
        a_s3=Action('상태를 R_Shoot으로 변경',self.change_state_Ready_to_Shoot)
        a_s4=Action('상태를 Shoot으로 변경',self.change_state_Shoot)
        a_s2_1=Action('도착지 방향 설정',self.set_run_angle)

        a_s2_2=Action('방향에 따른 스프라이트 설정',self.set_sprite_option)
        a_s2_3=Action('도착지 조금씩 이동',self.move_slightly_to)
        a_s3_1=Action('기다릴 시간 셋팅',self.set_waiting_time_and_time)
        a_s3_2=Action('기다림',self.waiting_shoot)
        a_s3_3=Action('슈팅',self.do_shoot)
        a_s5_1=Action('알맞은 베이스 찾기',self.find_base)
        a_s5_2=Action('베이스 각도 설정',self.set_angle_base_for_shoot)
        a_s5_3=Action('속도설정 (베이스)',self.set_v_to_base)
        a_s5_4=Action('베이스로 패스',self.do_pass)
        a_s5_5=Action('충돌 삭제',self.reset_collsion)
        a_s5_6=Action('충돌 리셋',self.check_ball)
        a_s5_1_1=Action('거리 확인',self.check_base)

        c1_1=Condition('도착하였는가',self.is_arrive)
        c1_2=Condition('도착하지 못하였는가',self.is_not_arrive)
        c_s1=Condition('Idle인가',self.is_state_Idle)
        c_s2=Condition('Run인가',self.is_state_Run)
        c3_1=Condition('이미 던졌는가',self.is_not_already_shoot)
        c5_1=Condition('프레임이 넘었는가 (catch)',self.is_frame_over_catch)
        self.SEQ_is_Idle=Sequence('Idle 상태인지 확인',c1_1,a_s1)
        self.SEQ_Idle=Sequence('기본상태작동',)

        self.SEQ_is_Run=Sequence('Run 상태인지 확인',c1_2,a_s2)
        self.SEQ_do_Run=Sequence('Run 상태 활동',a_s2_1,a_s2_2,a_s2_3)
        self.SEL_Run=Selector('Run 상태 체크 후 활동',self.SEQ_is_Idle,self.SEQ_do_Run)

        self.SEQ_set_already_Shoot=Sequence('R-Shoot 활동',c3_1,a_s4)

        self.SEQ_do_Shoot=Sequence('Shoot 상태 활동',a_s3_1,a_s3_2,a_s3_2,a_s3_3,a_s3)
        self.SEQ_is_Shoot=Sequence('Shoot 상태인지 확인',)
        self.SEL_Shoot=Sequence('Shoot 상태 체크 후 활동',self.SEQ_do_Shoot)
        self.SEL_set_Idle=Selector('Idle 상태 활동',self.SEQ_is_Run,self.SEQ_Idle)

        self.bt_list.append(BehaviorTree(self.SEL_set_Idle))
        self.SEL_set_Run=Selector('Run 상태 활동',self.SEQ_is_Idle,self.SEL_Run)
        self.bt_list.append(BehaviorTree(self.SEL_set_Run))
        self.SEQ_is_already_Shoot=Sequence('shooter, 던졌는지 체크 후, 변경',self.SEQ_set_already_Shoot)
        self.bt_list.append(BehaviorTree(self.SEQ_is_already_Shoot))
        self.SEQ_set_Shoot=Sequence('Shoot 상태 활동',self.SEL_Shoot)
        self.bt_list.append(BehaviorTree(self.SEQ_set_Shoot))
        self.SEQ_set_The_Catcher=Sequence('포수 상태 활동',self.SEQ_is_Run)
        self.bt_list.append(BehaviorTree(self.SEQ_set_The_Catcher))
        self.SEQ_set_Catch=Sequence('공을 잡은 후 상태 활동',a_s5_1,a_s5_1_1,a_s5_2,a_s5_3,c5_1,a_s5_4,a_s5_5,a_0,a_s5_6,a_s1)
        self.bt_list.append(BehaviorTree(self.SEQ_set_Catch))

        self.bt=BehaviorTree(self.SEL_set_Idle)