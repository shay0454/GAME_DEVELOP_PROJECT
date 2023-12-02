from pico2d import draw_rectangle
import game_world
import play_mode
class Base_p:
    def __init__(self,x,y,num):
        self.size=[24,24]
        self.location=[x,y] #x,y
        self.num=num
        self.player=None
        game_world.add_object(self,1)
        game_world.add_collision_pair('base:player',self,None)

    def draw(self):
        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.location[0]-self.size[0]//2,self.location[1]-self.size[1]//2,self.location[0]+self.size[0]//2,self.location[1]+self.size[1]//2
    
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

    def runners_run(self):
         for i in range(len(self.bases)-1,-1,-1):
            if self.bases[i].player != None and self.bases[i].player.state_machine.cur_state==play_mode.control.player_state_list['Idle'] and self.bases[i].player.target_base%4==self.bases[i].num:
                if self.bases[i].player.base_dir==1:
                    self.player_run(self.bases[i].player)

    def player_run(self,player):
        player.target_base=(player.target_base+player.base_dir)%4
        player.goto(self.base_locations['base'+str(player.target_base)])
        pass

    def draw(self):
        for i in range(len(self.bases)):
            self.bases[i].draw()

    def update(self):
        for i in range(len(self.bases)):
            self.bases[i].update()
        