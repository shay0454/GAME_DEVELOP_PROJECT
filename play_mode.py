from pico2d import*
import game_world
import game_framework
from field import Field
from field_control import Field_control

def handle_events():
    global control
    events=get_events()
    for event in events:
        if event.type==SDL_KEYDOWN and event.key==SDLK_ESCAPE:
                game_framework.running=False
        else:
            control.handle_events(event)



def init():
    global field
    global control

    field=Field()
    game_world.add_object(field,0)
    
    control=Field_control()

    


def finish():
    pass


def update():
    game_world.update()
    control.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    control.draw()
    update_canvas()
