from pico2d import load_image
import math
rad=math.pi/180
from sdl2 import SDLK_DOWN, SDLK_SPACE


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
            player.frame=(player.frame+1)%6
            if player.frame==0:
                player.is_swing=False

    @staticmethod
    def draw(player):
        hitter_frame_left=[0,2,5,8,12,15] #draw용 좌측 벽
        hitter_size=[16,24,24,24,24,24] #hitter 이미지 사이즈
        relocate_hitter_frame_left=[24,24,0,0,0,24] #다시 맞추기 용
        player.clip_composite_draw(hitter_frame_left[player.frame]*8,488-72,hitter_size[player.frame],32,0,'',player.x-relocate_hitter_frame_left[player.frame],player.y,player.size[0]*(hitter_size[player.frame])/24,player.size[1])
        pass


class Run:
    @staticmethod
    def enter(player,e):
        player.start=[player.x,player.y]
        Run.set_run_angle(player)
        Run.set_sprite_showed(player)

    @staticmethod
    def exit(player,e):
        pass
    
    @staticmethod
    def do(player):
        player.frame=(player.frame+1)%3
        Run.set_next_position(player)
        pass

    @staticmethod
    def draw(player):
        player.image.clip_composite_draw((player.frame)*16+18,320+12-player.updown*12,16,20,0,player.face,player.x,player.y,player.size[0],player.size[1])
        pass
    
    @staticmethod
    def set_run_angle(player):
        if(player.destination[0]!=player.x):
            player.angle=math.atan2((player.destination[1]-player.y),(player.destination[0]-player.x))/rad
        else :
            if(player.destination[1]>player.y): 
                player.angle=90
            else:
                player.angle=-90
        player.angle%=360

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
        if((player.destination[0]-player.x)**2+(player.destination[1]-player.y)**2<=player.v**2):
            player.x,player.y=player.destination[0],player.destination[1]
        else:
            player.x+=player.v*math.cos(player.angle*rad)
            player.y+=player.v*math.sin(player.angle*rad)
            
class Defend:
    pass
class Back:
    pass
class Catch:
    pass
class Pass:
    pass
class Shoot:
    pass
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
        player.image.clip_composite_draw(0,320+24,16,20,0,player.face,player.x,player.y,player.size[0],player.size[1])
        pass
    
class StateMachine:
    def __init__(self,player,num):
        self.player=player
        self.cur_state=Idle if num==0 else Defend
        self.state_table={
            Idle : {be_hitter : Hit, is_not_arrive: Run},
            Hit : {is_hit: Run, is_hit:Hit},
            Run : {is_out:Back, is_arrive:Idle},
            Defend:{is_hit:Catch, is_not_hit:Defend},
            Catch:{is_catch:Pass, is_not_catch:Catch},
            Shoot:{is_hit:Defend, is_not_hit:Shoot}
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
    image=None
    def __init__(self,num):
        self.x,self.y=400,20                        # 기본 좌표
        self.frame=0                                # 프레임
        self.face=''                                #  'h': 왼쪽, '': 오른쪽
        self.updown=1                               #  -1 : 다운, 1 : 업
        self.team=num                               # 팀 지정
        self.state_machine=StateMachine(self,num)   # 상태머신 지정
        self.state_machine.start()                  # 상태머신 시작
        self.destination=[self.x,self.y]            # 도착지점
        self.start=self.destination                 # 시작지점
        self.angle=0                                # run 각도 (도 각도)
        self.size=40,30                             # player draw 사이즈
        self.v=1                                    # player 속도
        if Player.image==None:
            Player.image=load_image('Baseball_Players.png')

    def handle_event(self,event):
        self.state_machine.handle_event(('INPUT',event))

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def goto(self,destination):
        self.destination=destination    


