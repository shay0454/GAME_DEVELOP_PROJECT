from pico2d import*
import game_world
import os
os.chdir(os.path.dirname(__file__))
from player import Player
from field import Field

def handle_events():
    global running 
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
field_set_info=[[400,60],[600,260],[400,460],[200,260],[400,60]]
def create_world():
    global running
    global field
    global player
    global game
    players=[]
    game=[]
    running=True

    field=Field()
    game_world.add_object(field,0)

    player=Player(0)
    players.append(player)
    game_world.add_object(player)

def update_world():
    game_world.update()

def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()

open_canvas()
create_world()
player.goto((400,60))
while(running):
    update_world()
    render_world()
    handle_events()
    check_players()
    if index<5 and player.x==player.destination[0] and player.y==player.destination[1]:
        player.destination=field_set_info[index]
        index+=1
    delay(0.01)

close_canvas()