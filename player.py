from pico2d import *
import math
def is_swing(e):
    return e[0]=='INPUT'and e[1].type==SDLK_DOWN and e[1].key==SDLK_SPACE

def be_hitter(e):
    return e[0]=='INPUT' and player.x==500 and player.y==60

def is_hit(e):
    return e.key==SDLK_SPACE

def is_not_hit(e):
    return not is_hit(e)

def is_catch(e):
    pass

def is_not_catch(e):
    return not is_catch(e)

def is_out(e):
    pass

def is_arrive(e):
    pass

def goto(player,destination):
    start=[player.x,player.y]
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
        player.clip_composite_draw(hitter_frame_left[player.frame]*8,488-72,hitter_size[player.frame],32,0,'',player.x-relocate_hitter_frame_left[player.frame],player.y,80*(hitter_size[player.frame])/24,60)
        pass


class Run:
    @staticmethod
    def enter(player,e):
        print('runner')


    @staticmethod
    def exit(player,e):
        pass
    
    @staticmethod
    def do(player):
        player.frame=(player.frame+1)%3
        pass

    @staticmethod
    def draw(player):
        pass
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
        player.frame=(player.frame+1)%3
        pass

    @staticmethod
    def draw(player):
        pass
    
class StateMachine:
    def __init__(self,player,num):
        self.player=player
        self.cur_state=Idle if num==0 else Defend
        self.state_table={
            Idle : {be_hitter : Hit,is_hit: Run},
            Hit : {is_hit: Run,is_hit:Hit},
            Run : {is_out:Back,is_arrive:Idle},
            Defend:{is_hit:Catch,is_not_hit:Defend},
            Catch:{is_catch:Pass,is_not_catch:Catch},
            Shoot:{is_hit:Defend,is_not_hit:Shoot}
        }
    def start(self):
            self.cur_state.enter(self.player,('NONE',0))
    def update(self):
        self.cur_state.do(self.player)
    def draw(self):
        self.cur_state.draw(self.player)
    def handle_event(self,e):
        for ckeck_event,next_state in self.state_table[self.cur_state].items() :
            if check_event(e):
                self.cur_state.exit(self.player,e)
                self.cur_state=next_state
                self.cur_state.enter(self.player,e)
                return True
        return False
class Player:
    image=None
    def __init__(self,num):
        self.x,self.y=400,20    # 기본 좌표
        self.frame=0            # 프레임
        self.face=1             #  -1 : 왼쪽, 1 : 오른쪽 
        self.updown=1           #  -1 : 다운, 1 : 업
        self.team=num
        self.state_machine=StateMachine(self,num)
        self.state_machine.start()
        if not self.image:
            self.image=load_image('Baseball_Players.png')

    def handle_event(self,event):
        self.state_machine.handle_event('INPUT',event)

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

                   


