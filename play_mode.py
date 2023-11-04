from pico2d import*
import game_world

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
field_set_info=[[400,30],[500,130],[400,230],[300,130],[400,30]]
def init():
    global running
    global field
    global player
    global game
    players=[]
    game=[]
    running=True

    field=Field()
    game_world.add_object(field,0)

    player=Player()
    players.append(player)
    game_world.add_object(player,2)


def finish():
    pass


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

open_canvas()
init()
player.goto([400,30])
while running:
    handle_events()
    update()
    draw()

    check_players()
    if player.base<5 and player.destination==[player.x,player.y]:
        player.pre_base=player.destination
        player.destination=field_set_info[player.base]
        player.base+=1
        player.base_dir=1
    delay(0.01)
finish()
close_canvas()