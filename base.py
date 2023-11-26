from pico2d import draw_rectangle
import game_world
import play_mode
class Base_p:
    def __init__(self,x,y,num):
        self.size=[48,48]
        self.num=num
        self.x,self.y=x,y
        self.is_death=False
        self.player=None
        game_world.add_collision_pair('base:player',self,None)

    def get_bb(self):
        return self.x-self.size[0]//2,self.y-self.size[1]//2,self.x+self.size[0]//2,self.y+self.size[1]//2
    
    def update(self):
        if self.player!=None and not game_world.collide(self,self.player):
            self.player=None

    def handle_collision(self,group,other):
        if group=='base:player':
            print('player')
            self.player=other

class Base:
    def __init__(self):
        self.base_locations={'base1':[560+4,240],'base2':[400,400+12],'base3':[240-4,240],'base4':[400,90]}
        self.bases=[Base_p(*self.base_locations['base'+str(i+1)],(i+1)%4) for i in range(4)]

    def players_run(self):
         for i in range(3,-1,-1):
            if self.bases[i].player != None and self.bases[i].player.target_base%4==self.bases[i].num:
                self.bases[i].player.target_base+=1
                the_base='base'+str(self.bases[i].player.target_base)
                self.bases[i].player.goto(self.base_locations[the_base])
                self.bases[i].player.state_machine.change_state(play_mode.control.player_state_list['Idle'],('Change',0))

    def player_run(self,player):
        player.target_base+=1
        player.goto(self.base_locations['base'+player.target_base])
        pass

    def draw(self):
        for i in range(4):
            draw_rectangle(*self.bases[i].get_bb())

    def update(self):
        for i in range(4):
            self.bases[i].update()
        