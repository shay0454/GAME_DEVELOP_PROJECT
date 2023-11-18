from pico2d import*
import game_world
from field import Field
from field_control import Field_control
from bat import Bat

def handle_events():
    global running,control
    events=get_events()
    for event in events:
        if event.type==SDL_KEYDOWN and event.key==SDLK_ESCAPE:
                running=False
        else:
            control.handle_events(event)

    control.handle_events(('CHECK',0))


def init():
    global running
    global field
    global control
    running=True

    field=Field()
    game_world.add_object(field,0)
    bat=Bat()
    game_world.add_object(bat,2)
    game_world.add_collision_pair('ball:bat',None,bat)
    control=Field_control()

    


def finish():
    pass


def update():
    control.update()
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
