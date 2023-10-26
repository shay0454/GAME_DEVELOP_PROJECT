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
            for i in range(5):
                players[i].handle_events(event)
            

def create_world():
    global running
    global field
    global players
    global game
    players=[]
    game=[]
    running=True

    field=Field()
    game_world.add_object(field,0)

    for i in range(5):
        players.append(Player(0))
        game_world.add_object(players[i])

def update_world():
    game_world.update()

def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()

open_canvas()
create_world()

while(running):
    update_world()
    render_world()
    handle_events()

close_canvas()