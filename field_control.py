import pico2d
import copy
import game_world
from defensive import *
from offensive import *
from base import *
from field_control_function import *
from ball_location_test import *
# 모든 player가 도착했는지 확인용
def is_all_arrive(control):
    for object_list in control.players:
        for player in object_list:
            if not is_arrive_(player,('CHECK',0)):
                return False
    return True

def is_objects_arrive(objects):
    for player in objects:
        if not is_arrive_(player,('CHECK',0)):
            return False
    return True

def delete_player(control,player):
    for object_list in control.players:
        if player in object_list:
            object_list.remove(player)
class Ready:
    @staticmethod
    def enter(control):
        control.runners_stop()
        if len(control.batter)==0:
            control.create_batter()
        control.recheck_variable()       
        control.defenders_init()
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
        if control.basemen[0].ball_picked:
            control.state_machine.change_state(End)
        elif control.ball!=None and control.is_hit:
            control.batter[0].state_machine.change_state(control.player_state_list['Idle'])
            control.state_machine.change_state(Hitted)

class Hitted:
    @staticmethod
    def enter(control):
        print('control_hit')
        control.draw_ball_on_ground()
        control.do_field_active_hit()

    @staticmethod
    def exit(control):
        control.delete_point_ball_on_ground()
        pass

    @staticmethod
    def do(control):
        control.check_is_foul()
        control.check_frist_catch()
        pass

class Catch:
    @staticmethod
    def enter(control):
        defender_stop(control)
        control.check_hitted_ball_out()
        pass

    @staticmethod
    def exit(control):
        pass

    @staticmethod
    def do(control):
        control.check_player_collision()
        pass

class End:
    @staticmethod
    def enter(control):
        print('game end')
        control.time=get_time()
        pass

    @staticmethod
    def exit(control):
        control.check_strike_or_foul()
        control.check_strike_over()
        control.check_out()
        control.reset_game()

    @staticmethod
    def do(control):
        if get_time()-control.time>1:
            control.state_machine.change_state(Ready)
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
        self.strike,self.out,self.score=0,0,0    
        self.font=load_font('ENCR10B.TTF',15)
        self.state_machine=Field_statement(self)
        self.base=Base()
        self.base_locations=[base.location for base in self.base.bases]                    # base_locations
        self.fielder_locations=[[250,440],[400,530],[550,440]]                             
        self.catcher_location,self.picker_location,self.batter_location=[400,20],[400,230],[400-25,70]
        self.ball=None
        self.is_ground,self.is_hit,self.is_foul=False,False,False
        self.is_strike,self.ball_picked=False,False
        self.location_player_with_ball=[]
        self.batter,self.picker,self.runners,self.fielders,self.basemen=[],[],[],[],[]
        self.players=[self.batter,self.runners,self.picker,self.basemen,self.fielders]            # players
        self.point_draw,self.expect_ball_location,expect_ball_time=[],[],[]
        self.out_list=[]
        self.state_list={'Ready':Ready,'Start':Start,'Hitted':Hitted,'Catch':Catch,'End':End}
        self.player_state_list={'Idle':Idle,'Run':Run,'Shoot':Shoot,'Hit':Hit,'Hitting':Hitting,'The_Catcher':The_Catcher}
        self.create_defenders()
        self.state_machine.cur_state.enter(self)  
                  
    def update(self):
        self.state_machine.update()
        self.base.update()
    
    def draw(self):
        self.font.draw(100,120,f'strike : {self.strike}',(256,256,256))
        self.font.draw(100,100,f'   out : {self.out}',(256,256,256))
        self.font.draw(100,80,f' score : {self.score}',(256,256,256))
        pass

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

    def create_fielders(self):                                                                 # fielder 객체들 초기화용
        for i in range(3):
            player=Player('fielder')
            self.fielders.append(player)
        game_world.add_objects(self.fielders,2)
        
    def create_basemen(self): 
        player=Player('The_Catcher')           
        self.basemen.append(player)                                                     # fielder 객체들 초기화용
        for i in range(1,4):
            player=Player('baseman')
            self.basemen.append(player)
        game_world.add_objects(self.basemen,2)

    def create_picker(self):
        picker=Player('picker')
        self.picker.append(picker)
        game_world.add_objects(self.picker,2)

    def create_batter(self):
        batter=Batter()
        self.batter.append(batter)
        game_world.add_objects(self.batter,2)

    def fielders_init(self):
        for player in self.fielders:
            player.ball_picked,player.already_shoot=False,False
            game_world.add_collision_pair('ball:defender',None,player)
            game_world.add_collision_pair('base:defender',None,player)

    def basemen_init(self):
        for player in self.basemen:
            player.ball_picked,player.already_shoot=False,False
            game_world.add_collision_pair('ball:defender',None,player)
            game_world.add_collision_pair('base:defender',None,player)

    def picker_init(self):
        self.picker[0].ball_picked,self.picker[0].already_shoot=False,False
        pass

    def create_defenders(self):
        self.create_fielders()
        self.create_basemen()
        self.create_picker()

    def defenders_init(self):
        self.fielders_init()
        self.basemen_init()
        self.picker_init()

    def draw_ball_on_ground(self):
        if self.ball==None:
            return
        self.expect_ball_location=[]
        for location in self.ball.locations_when_ball_on_ground:
            point=Ball_ground_location(*location)
            self.point_draw.append(point)
            self.expect_ball_location.append([point.x,point.y])
            game_world.add_object(point,1)
        self.expect_ball_time=[*self.ball.times_when_ball_on_ground]

    def delete_point_ball_on_ground(self):
        for point in self.point_draw:
            game_world.remove_object(point)
        self.point_draw=[]

    def go_to_ball_point(self,fielder):
        for i in range(len(self.expect_ball_location)):
            location=[*self.expect_ball_location[i]]
            if distance_less_than(location[0]-fielder.location[0],location[1]-fielder.location[1],self.expect_ball_time[i]*fielder.RUN_SPEED_PPS):
                fielder.goto(location)
                return
        fielder.goto(self.expect_ball_location[len(self.expect_ball_location)-1])

    def go_to_ball_point_defend(self):
            for fielder in self.fielders:
                self.go_to_ball_point(fielder)
            self.go_to_ball_point(self.picker[0])
        
    def find_base(self):
        for runner in self.runners:
            if not self.base.is_player_in_base(runner):
                if not(runner in self.out_list):
                    return runner.target_base
        return -1        
    
    def runners_back_run(self):
        for runner in self.runners:
            runner.target_base=(runner.target_base-1)
            if runner.target_base>0:
                runner.goto(self.base_locations[runner.target_base])

    def batter_run(self):
        self.runners.append(self.batter[0])
        self.batter[0].goto([560,230])

    def runners_stop(self):
        for runner in self.runners:
            runner.stop()

    def player_stop(self,player):
        for objs in self.players:
            if player in objs:
                player.stop()
    
    def check_frist_catch(self):
        for player in self.fielders:
            if player.ball_picked:
                self.state_machine.change_state(Catch)
        for player in self.basemen:
            if player.ball_picked:
                self.state_machine.change_state(Catch)

    def do_field_active_hit(self):
        location=self.ball.locations_when_ball_on_ground[len(self.ball.locations_when_ball_on_ground)-1]
        self.angle=math.atan2(location[1]-20,location[0]-400)
        if self.angle>PI/4 and self.angle<PI*3/4:
            self.batter_run()
            self.basemen[0].goto(self.base_locations[0])
            game_world.add_collision_pair('ball:defender',None,self.picker[0])

    def recheck_variable(self):
        self.base_locations=[[*base.location] for base in self.base.bases]                    
        self.players=[self.batter,self.runners,self.picker,self.basemen,self.fielders]         

    def check_is_foul(self):
        if self.angle>PI/4 and self.angle<PI*3/4:
            self.base.runners_run()
            self.go_to_ball_point_defend()
        else:
            self.is_foul=True
            self.state_machine.change_state(End)
            
    def check_hitted_ball_out(self):
        if not self.is_ground:
            do_out_batter(self)
            self.runners_back_run()

    def check_strike_or_foul(self):
        if self.is_strike:
            self.strike+=1
        elif self.is_foul:
            game_world.remove_object(self.ball)
            self.ball=None
            self.strike+=1
        else:
            for location_obj in self.expect_ball_location:
                game_world.remove_object(location_obj)
            self.expect_ball_location,self.expect_ball_time=[],[]
        if not(self.is_strike or self.is_foul):
            self.batter=[]

    def check_strike_over(self):
        if self.strike==3:
            self.strike=0
            do_out_batter(self)

    def check_out(self):
        print('---------------')
        for out in self.out_list:
            self.strike=0
            print(out)
            delete_player(self,out)
            game_world.remove_object(out)
            self.out+=1
        self.out_list.clear()

    def reset_game(self):
        self.picker[0].state_machine.change_state(self.player_state_list['Idle'],('CHANGE',0))
        game_world.remove_collision_object(self.picker[0])
        self.is_strike,self.is_foul,self.is_hit,self.is_ground=False,False,False,False
        for player in self.runners:
            player.base_dir=1

    def check_player_collision(self):
        if self.ball_picked:
            for player in self.fielders:
                if distance_less_than(player.location[0]-self.location_player_with_ball[0],player.location[1]-self.location_player_with_ball[1],24):
                    game_world.remove_collision_object(player)
                else:
                    game_world.add_collision_pair('ball:defender',None,player)

def distance_less_than(x,y,r):
    return True if x*x+y*y<r*r else False
