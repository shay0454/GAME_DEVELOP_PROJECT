import pico2d
import game_world
from player import *
from offensive import *
from base import *
from field_control_function import *
from ball_location_test import *
# 모든 player가 도착했는지 확인용
def is_all_arrive(control):
    for object_list in control.players:
        for player in object_list:
            if not is_arrive(player,('CHECK',0)):
                return False
    return True

class Ready:
    @staticmethod
    def enter(control):
        players_destination_init(control)

    @staticmethod
    def exit(control):
        pass

    @staticmethod
    def do(control):
        if is_all_arrive(control):
            change_state_Start(control)

class Start:
    @staticmethod
    def enter(control):
        set_Start(control)

    @staticmethod
    def exit(control):
        pass

    @staticmethod
    def do(control):
        pass

class Hitted:
    @staticmethod
    def enter(control):
        print('control_hit')
        batter_run(control)
        game_world.add_collision_pair('ball:defender',None,control.picker[0])
        control.fielder_goto_ball_allow()
        pass

    @staticmethod
    def exit(control):
        pass

    @staticmethod
    def do(control):
        control.base.runners_run()
        control.draw_ball_on_ground()
        pass

class Catch:
    @staticmethod
    def enter(control):
        defender_stop(control)
        pass

    @staticmethod
    def exit(control):
        pass

    @staticmethod
    def do(control):
        pass

class End:
    @staticmethod
    def enter(control):
        print('game end')
        pass

    @staticmethod
    def exit(control):
        pass

    @staticmethod
    def do(control):
        pass


class Field_statement:

    def __init__(self,f_control):
        self.f_control=f_control
        self.cur_state=Ready
        self.state_table={
            Ready:{},
            Start:{},
            Hitted:{},
            Catch:{},
            End:{}
        }
        
    def handle_events(self):
        for ckeck_active, next_state in self.state_table[self.cur_state].items():
            if ckeck_active(self.f_control):
                self.change_state(next_state)
                return True
        return False
    
    def start(self):
        self.cur_state.enter(self.f_control,('NONE',0))

    def update(self):
        self.cur_state.do(self.f_control)

    def draw(self):
        self.cur_state.draw(self.f_control)

    def change_state(self,next_state):
        self.cur_state.exit(self.f_control)
        self.cur_state=next_state
        self.cur_state.enter(self.f_control)

class Field_control:
            
    def __init__(self):
        self.strike,self.out=0,0      
        self.state_machine=Field_statement(self)
        self.base=Base()
        self.base_locations=[base.location for base in self.base.bases]                    # base_locations
        self.fielder_locations=[[250,440],[400,530],[550,440]]                             
        self.catcher_location,self.picker_location,self.batter_location=[400,30],[400,230],[400-25,70]
        self.allow_catch_list=[]
        self.ball=None
        self.tf_hit=False
        self.batter,self.picker,self.runners,self.fielders,self.basemen=[],[],[],[],[]
        self.players=[self.batter,self.runners,self.picker,self.basemen,self.fielders]            # players
        self.out_list=[]
        self.state_list={'Ready':Ready,'Start':Start,'Hitted':Hitted,'Catch':Catch}
        self.player_state_list={'Idle':Idle,'Run':Run,'Shoot':Shoot,'Hit':Hit,'The_Catcher':The_Catcher}
        self.players_init()
        self.state_machine.cur_state.enter(self)  
                  
    def update(self):
        self.state_machine.update()
        self.base.update()
    
    def draw(self):
        self.base.draw()
        if self.state_machine.cur_state==Hitted:
            self.draw_ball_on_ground()

    def handle_events(self,event):
        if event.type==SDL_KEYDOWN and event.key==SDLK_SPACE:
            if self.state_machine.cur_state==Start:
                print('space')
                self.batter[0].state_machine.handle_event(('INPUT',event))
            elif self.state_machine.cur_state==Ready:
                self.Skip_Ready()
        elif event.type==SDL_KEYDOWN and event.key==SDLK_1:
            print(1)
        if event.type==SDL_MOUSEBUTTONDOWN:
            for player in self.runners:
                player.state_machine.handle_event(('INPUT',event))

    def Skip_Ready(self):
        players_location_init(self)

    def fielders_init(self):                                                                 # fielder 객체들 초기화용
        for i in range(4):
            player=Player()
            self.fielders.append(player)
            game_world.add_collision_pair('ball:defender',None,player)
        game_world.add_objects(self.fielders,2)
        

    def basemen_init(self):                                                                 # fielder 객체들 초기화용
        for i in range(4):
            player=Player()
            self.basemen.append(player)
            game_world.add_collision_pair('ball:baseman',None,player)
            game_world.add_collision_pair('base:baseman',None,player)
        game_world.add_objects(self.basemen,2)

    def picker_init(self):
        picker=Player()
        self.picker.append(picker)
        game_world.add_objects(self.picker,2)

    def batter_init(self):
        batter=Batter()
        self.batter.append(batter)
        game_world.add_objects(self.batter,2)

    def players_init(self):
        self.fielders_init()
        self.basemen_init()
        self.picker_init()
        self.batter_init()

    def draw_ball_on_ground(self):
        for location in self.ball.locations_when_ball_on_ground:
            game_world.add_object(Ball_ground_location(*location),1)

    def fielder_check_point(self,fielder):
        for i in range(len(self.ball.locations_when_ball_on_ground)-1):
            if distance_less_than(self.ball.locations_when_ball_on_ground[i][0]-fielder.location[0],self.ball.locations_when_ball_on_ground[i][1]-fielder.location[1],self.ball.times_when_ball_on_ground[i]*fielder.RUN_SPEED_PPS):
                fielder.goto(self.ball.locations_when_ball_on_ground[i])
                return
        fielder.goto(self.ball.locations_when_ball_on_ground[len(self.ball.locations_when_ball_on_ground)-1])

    def fielder_goto_ball_allow(self):
            for fielder in self.fielders:
                self.fielder_check_point(fielder)
        
    def find_base(self):
        for runner in self.runners:
            if not self.base.is_player_in_base(runner):
                return runner.target_base
        self.state_machine.change_state(End)
        return -1

def distance_less_than(x,y,r):
    return True if x*x+y*y<r*r else False
