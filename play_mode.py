from pico2d import*
import game_world
from field import Field
from field_control import Field_control

def handle_events():
    global running,control
    events=get_events()
    for event in events:
        if(event.type==SDL_KEYDOWN):
            if event.key==SDLK_ESCAPE:
                running=False

    control.handle_events(None)


def init():
    global running
    global field
    global control
    running=True

    field=Field()
    game_world.add_object(field,0)
    
    control=Field_control()


def finish():
    pass


def update():
    control.update()
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
