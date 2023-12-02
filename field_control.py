import pico2d
import game_world
from player import *
from offensive import *
from base import *
from field_control_function import *
# 모든 player가 도착했는지 확인용
def is_all_arrive(control):
    for object_list in control.players:
        for player in object_list:
            if len(object_list)!=0 and not is_arrive(player,('CHECK',0)):
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
            set_Start(control)
class Start:
    @staticmethod
    def enter(control):
        print('start')
        control.basemen[0].state_machine.change_state(The_Catcher,('CHANGE',0))

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
        control.batter.goto([560+4,240])
        control.runner.append(control.batter)
        control.batter=None
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
    pass

class End:
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
                self.cur_state.exit(self.f_control)
                self.cur_state=next_state
                self.cur_state.enter(self.f_control)
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
        self.state_machine=Field_statement(self)
        self.base=Base()
        self.base_locations=[base.location for base in self.base.bases]                    # base_locations
        self.strike,self.out=0,0      
        self.base_point=[[400,90],[560+4,240],[400,400+12],[240-4,240]]                    # base_point
        self.fielder_locations=[[250,240],[400,330],[550,240]]                                                                 # strike, out
        self.catcher_location=[400,30]
        self.picker_location=[400,230]
        self.batter_location=[400-25,70]
        self.fielder_info={0:'left',1:'mid',2:'right'}                                    # 제거 예정
        self.tf_hit=False
        self.batter=[]
        self.picker=[]
        self.runner=[]                                                                             # 변형 예정
        self.fielders=[]                                                                            # fielders
        self.basemen=[]                                                                             # basemen
        self.players=[self.batter,self.runner,self.picker,self.basemen,self.fielders]            # players
        self.state_list={'Ready':Ready,'Start':Start,'Hitted':Hitted,'Catch':Catch}
        self.player_state_list={'Idle':Idle,'Run':Run,'Shoot':Shoot,'Hit':Hit}
        self.players_init()
        self.state_machine.cur_state.enter(self)  
                  
    def update(self):
        self.state_machine.update()
        self.base.update()
    
    def draw(self):
        self.base.draw()

    def Skip_Ready(self):
        
        pass

    def tp_picker_destination_init(control):
        control.fielders[0].goto(control.fielder_locations[control.fielder_info[0]])

    def handle_events(self,event):
        if event.type==SDL_KEYDOWN and event.key==SDLK_SPACE:
            if self.state_machine.cur_state==Start:
                print('space')
                self.batter[0].state_machine.handle_event(('INPUT',event))
            elif self.state_machine.cur_state==Ready:
                self.Skip_Ready()
        if event.type==SDL_MOUSEBUTTONDOWN:
            for player in self.runner:
                player.state_machine.handle_event(('INPUT',event))


    def fielders_init(self):                                                                 # fielder 객체들 초기화용
        for i in range(4):
            player=Player()
            self.fielders.append(player)
            game_world.add_object(player,2)

    def basemen_init(self):                                                                 # fielder 객체들 초기화용
        for i in range(4):
            player=Player()
            self.basemen.append(player)
            game_world.add_object(player,2)

    def picker_init(self):
        picker=Player()
        self.picker.append(picker)
        game_world.add_object(self.picker[0],2)

    def batter_init(self):
        batter=Batter()
        self.batter.append(batter)
        game_world.add_object(self.batter[0],2)

    def players_init(self):
        self.fielders_init()
        self.basemen_init()
        self.picker_init()
        self.batter_init()