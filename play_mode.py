from pico2d import*
import game_world
from player import Player
from field import Field,Field_control

def handle_events():
    global running,player
    events=get_events()
    for event in events:
        if(event.type==SDL_KEYDOWN):
            if event.key==SDLK_ESCAPE:
                running=False
        else:
            player.handle_event(event)

def check_players():
    player.handle_event(None)
    
index=0            
field_set_info=[[400,30],[500,130],[400,230],[300,130],[400,30]]
def init():
    global running
    global field
    global player
    global game
    global control
    game=[]
    running=True

    field=Field()
    game_world.add_object(field,0)
    
    control=Field_control()
    player=Player(1)



def finish():
    pass


def update():
    control.update()
    game_world.update()
    check_players()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
