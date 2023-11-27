import pico2d
import game_world
from player import *
from batter import *

# 모든 player가 도착했는지 확인용
def is_all_arrive(control):
    for x in range(len(control.f_objects)):
        for i in range(len(control.f_objects[x])):
            if not is_arrive(control.f_objects[x][i],('CHECK',0)):
                control.tf_all_arrive=False
                return False
    control.tf_all_arrive=True
    return True

def is_end(players):
    pass

def is_catched(players):
    pass

def is_hit(control):
    pass

def is_not_hit(control):
    pass

def is_out(control):
    pass
class Ready:
    @staticmethod
    def enter(control):
        Ready.picker_location_init(control)
        #Ready.fielders_location_init(control)
        #Ready.basemen_location_init(control)
        Ready.batter_location_init(control) 

    @staticmethod
    def exit(control):
        pass

    @staticmethod
    def do(control):
        if is_all_arrive(control):
            control.state_machine.change_state(Start)
            control.fielders[0].state_machine.change_state(Shoot,('CHANGE',0))
            print(control.fielders[0].state_machine.cur_state)
            control.players[0].state_machine.change_state(Hit)
        pass
    
    def picker_location_init(control):
        control.fielders[0].goto(control.fielder_point[control.fielder_info[0]])

    def fielders_location_init(control):                                                        # fielders 위치 초기화용
            for i in range(1,len(control.fielders)):
                control.fielders[i].goto(control.fielder_point[control.fielder_info[i]])

    def basemen_location_init(control):                                                          # basemen 위치 초기화용
            for i in range(len(control.basemen)):
                control.basemen[i].goto(control.base_point[i])

    def batter_location_init(control):
        control.players[0].goto([400,130])

class Start:
    @staticmethod
    def enter(control):
        print('start')

    @staticmethod
    def exit(control):
        pass

    @staticmethod
    def do(control):
        pass

class Hitted:
    
    @staticmethod
    def enter():
        pass

    @staticmethod
    def exit():
        pass

    @staticmethod
    def do(control):
        control.base.players_run()
        
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
            Start:{is_hit:Hitted,is_not_hit:Start,is_end:End},
            Hitted:{},
            Catch:{is_out:Catch,is_out:Catch},
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
        self.field =[None,None,None,None,None]                                                      # 홈, 1루, 2루, 3루, 홈
        self.strike,self.out=0,0                                                                    # strike, out
        self.base_point=[[400,90],[560+4,240],[400,400+12],[240-4,240],[400,90]]                    # base_point
        self.fielder_point={'shoot':[400,230],'left':[250,240],'mid':[400,330],'right':[550,240]}   # fielders의 위치 dict
        self.fielder_info={0:'shoot',1:'left',2:'mid',3:'right'}                                    # 제거 예정
        self.p={'players':0,'fielders':1,'basemen':2}                                               # 매칭용
        self.tf_all_arrive=False
        self.tf_hit=False
        self.players=[]                                                                             # 변형 예정
        self.fielders=[]                                                                            # fielders
        self.basemen=[]                                                                             # basemen
        self.f_objects=[self.players,self.fielders,self.basemen]                                    # f_objects
        self.state_list={'Ready':Ready,'Start':Start,'Hitted':Hitted,'Catch':Catch}
        self.player_state_list={'Idle':Idle,'Run':Run}
        self.base=Base()
        game_world.add_objects(self.base.bases)
        self.f_object_init()
        self.state_machine.cur_state.enter(self)  
                  

    def update(self):
        self.state_machine.update()
        self.base.update()
        pass
    
    def draw(self):
        self.base.draw()

    def get_next_base(self,player):                                                         # 변형 예정
        if(player.destination==self.field_set_info[player.base]):
            player.base+=1
            if 1:
                return player.destination
            return self.field_set_info[player.base]
        return player.destination

    def handle_events(self,event):
        if event.type==SDL_KEYDOWN and event.key==SDLK_SPACE and self.players[0]!=None and self.players[0].state_machine.cur_state==Hit:
            print('space')
            self.players[0].state_machine.handle_event(('INPUT',event))

    def fielders_init(self):                                                                 # fielder 객체들 초기화용
        for i in range(1,4):
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
        self.fielders.append(picker)
        game_world.add_object(picker,2)

    def batter_init(self):
        batter=Batter()
        self.f_objects[self.p['players']].append(batter)
        game_world.add_object(batter,2)

    def f_object_init(self):
        self.fielders_init()
        self.basemen_init()
        self.picker_init()
        self.batter_init()