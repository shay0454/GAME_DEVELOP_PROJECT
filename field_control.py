import pico2d
import game_world
from player import *
from picker import *
def is_all_arrive(control):                                             # 모든 player가 도착했는지 확인용
    for i in range(len(control.f_objects[control.p['fielders']])):
        if not is_arrive(control.f_objects[control.p['fielders']][i], None): return False
    return True

def is_end(players):
    pass

def is_catched(players):
    pass

def is_hit(control):
    pass

def is_not_hit(control):
    pass

class Ready:
    @staticmethod
    def enter(control):
        Ready.fielders_location_init(control)
        Ready.basemen_location_init(control)

    @staticmethod
    def exit(control):
        pass

    @staticmethod
    def do(control):
        print(1)
        pass
    
    def picker_location_init(control):
        control.fielders[0].goto(control.fielder_point[control.fielder_info[0]])
    def fielders_location_init(control):                                                        # fielders 위치 초기화용
            for i in range(1,len(control.fielders)):
                control.fielders[i].goto(control.fielder_point[control.fielder_info[i]])

    def basemen_location_init(control):                                                          # basemen 위치 초기화용
            for i in range(len(control.basemen)):
                control.basemen[i].goto(control.base_point[i])

class Start:
    @staticmethod
    def enter(control):
        print('start')
        control.fielders[0].state_machine.change_state(Shoot)

    @staticmethod
    def exit(control):
        pass

    @staticmethod
    def do(control):
        pass

class Hit:
    
    @staticmethod
    def enter():
        pass

    @staticmethod
    def exit():
        pass

    @staticmethod
    def do():
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
            Ready:{is_all_arrive:Start},
            Start:{is_hit:Hit,is_not_hit:Start,is_end:End},
            Catch:{is_out:Catch,is_catch:Catch},
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

class Field_control:
            
    def __init__(self):
        self.state_machine=Field_statement(self)
        self.field =[None,None,None,None,None]                                                      # 홈, 1루, 2루, 3루, 홈
        self.strike,self.out=0,0                                                                    # strike, out
        self.catched=False                                                                          # ball_catched의 확인용 (제거예정)
        self.base_point=[[400,90],[560+4,240],[400,300+12],[240-4,240],[400,70]]                           # base_point
        self.fielder_point={'shoot':[400,130],'left':[250,240],'mid':[400,330],'right':[550,240]}   # fielders의 위치 dict
        self.fielder_info={0:'shoot',1:'left',2:'mid',3:'right'}                                    # 제거 예정
        self.p={'players':0,'fielders':1,'basemen':2}                                               # 매칭용
        self.players=[]                                                                             # 변형 예정
        self.fielders=[]                                                                            # fielders
        self.basemen=[]                                                                             # basemen
        self.f_objects=[self.players,self.fielders,self.basemen]                                    # f_objects
        self.picker_init()
        Ready.picker_location_init(self)
        self.fielders_init()       
        #Ready.fielders_location_init(self)         
        #self.basemen_init()
        Ready.basemen_location_init(self)                          

    def update(self):
        self.state_machine.update()
        pass
    
    def get_next_base(self,player):                                                         # 변형 예정
        if(player.destination==self.field_set_info[player.base]):
            player.base+=1
            if 1:
                return player.destination
            return self.field_set_info[player.base]
        return player.destination

    def handle_events(self,event):
        self.state_machine.handle_events()
        for i in range(0,len(self.basemen)):
            self.basemen[i].handle_event(event)
        for i in range(0,len(self.players)):
            self.players[i].handle_event(event)
        for i in range(0,len(self.fielders)):
            self.fielders[i].handle_event(event)

    def fielders_init(self):                                                                 # fielder 객체들 초기화용
        global fielders
        for i in range(1,4):
            player=Player(2)
            self.fielders.append(player)
            game_world.add_object(player,2)

    def basemen_init(self):                                                                 # fielder 객체들 초기화용
        global basemen
        for i in range(4):
            player=Player(2)
            self.basemen.append(player)
            game_world.add_object(player,2)

    def picker_init(self):
        global fielders
        picker=Picker()
        self.fielders.append(picker)
        game_world.add_object(picker,2)