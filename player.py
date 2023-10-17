from pico2d import *
import math
def is_hit():
    return 
class Hitting: #416 488
    @staticmethod
    def enter(player):
        print('hitter')
        player.draw_x,player.draw_y
    
    @staticmethod
    def exit():
        pass

    @staticmethod
    def do(player,e):
        if(player.is_swing):
            player.frame=(player.frame+1)%5
        if(e.type==SDL_KEYDOWN and e.key==SDLK_SPACE):
            player.is_swing=True

    @staticmethod
    def draw():
        pass


class Running:
    @staticmethod
    def enter():
        print('runner')

    @staticmethod
    def exit():
        pass
    
    @staticmethod
    def do():
        player.frame=(player.frame+1)%3
        pass

    @staticmethod
    def draw():
        pass
class Back_running:
    pass
class Rest:
    pass
class StateMachine:
    def __init__(self,player):
        self.player=player
        self.cur_state=Hitting
        self.state_table=[

        ]
class Player:
    def __init__(self):
        self.image=load_image('NES-Baseball-Players.png')
    
    def set_location(self,x,y):
        self.x,self.y=x,y
    def update(self):
        self.cur_state.do()
    def draw(self):
        self.image.clip_draw(0,320,208,160,200,300)

                   


