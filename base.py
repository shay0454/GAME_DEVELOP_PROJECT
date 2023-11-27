from pico2d import draw_rectangle
import game_world
import play_mode
class Base_p:
    def __init__(self,x,y,num):
        self.size=[24,24]
        self.num=num
        self.x,self.y=x,y
        self.is_death=False
        self.player=None
        game_world.add_collision_pair('base:player',self,None)

    def draw(self):
        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.x-self.size[0]//2,self.y-self.size[1]//2,self.x+self.size[0]//2,self.y+self.size[1]//2
    
    def update(self):
        if self.player!=None and not game_world.collide(self,self.player):
            self.player=None

    def handle_collision(self,group,other):
        if group=='base:player' and self.player!=other:
            print('in base')
            self.player=other

class Base:
    def __init__(self):
        self.base_locations={'base0':[400,76],'base1':[558,232],'base2':[400,392+12],'base3':[242,232]}
        self.bases=[Base_p(*self.base_locations['base'+str(i)],(i)) for i in range(4)]

    def players_run(self):
         for i in range(len(self.bases)-1,-1,-1):
            if self.bases[i].player != None and self.bases[i].player.state_machine.cur_state==play_mode.control.player_state_list['Idle'] and self.bases[i].player.target_base%4==self.bases[i].num:
                self.bases[i].player.target_base=(self.bases[i].player.target_base+1)%4
                the_base='base'+str(self.bases[i].player.target_base)
                self.bases[i].player.goto(self.base_locations[the_base]) # 고칠곳 (아래)
                self.bases[i].player.state_machine.change_state(play_mode.control.player_state_list['Idle'],('Change',0))

    def player_run(self,player):
        player.target_base+=1
        player.goto(self.base_locations['base'+player.target_base])
        pass

    def draw(self):
        for i in range(len(self.bases)):
            self.bases[i].draw()

    def update(self):
        for i in range(len(self.bases)):
            self.bases[i].update()
        