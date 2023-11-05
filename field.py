from pico2d import *
import game_world
from player import Player
import os
os.chdir(os.path.dirname(__file__))
class Field: #1024 1024
    def __init__(self):
        self.image=load_image('SNES-Human_Baseball_JPN-Saitama.png')

    def update(self):
        pass
    
    def draw(self):
        self.image.draw(400,450)


class Field_control:

    def defend_init(self):
        global players
        for i in range(3):
            player=Player(2)
            self.players.append(player)
            game_world.add_object(player,2)
            player.goto(self.f_info_for_d[self.p[i]])
            
    def __init__(self):
        field =[None,None,None,None,None] # 홈, 1루, 2루, 3루, 홈
        strike,out=0,0
        catched=False
        self.f_info_for_p=[[400,30],[500,130],[400,230],[300,130],[400,30]]
        self.f_info_for_d={'shoot':[400,200],'left':[350,240],'mid':[400,330],'right':[450,240]}
        location={'shoot':0,'left':1,'mid':2,'right':3}
        self.p=['shoot','left','mid','right']
        self.players=[]
        for i in range(4):
            player=Player(2)
            self.players.append(player)
            game_world.add_object(player,2)
            player.goto(self.f_info_for_d[self.p[i]])
        
    def update(self):
        pass
        
        
    def get_next_base(self,player):
        if(player.destination==self.field_set_info[player.base]):
            player.base+=1
            if not catched:
                return player.destination
            return self.field_set_info[player.base]
        return player.destination

