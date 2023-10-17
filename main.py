from pico2d import*
import os
os.chdir(os.path.dirname(__file__))
from player import Player
from field import Field

def handle_events():
    global running 
    events=get_events
    for event in events:
        if(event.type==SDL_KEYDOWN):
            if event.key==SDLK_ESCAPE:
                running=False

def set_game():
    global running
    global field
    global players
    global game
    game=[]
    
    field=Field()
    game.append(field)

    players=Player()
    game.append(players)

def update_game():
    for obj in game:
        obj.update()

def render_game():
    for obj in game:
        obj.draw()

open_canvas()
set_game()
render_game()
update_canvas()
delay(50)
close_canvas()