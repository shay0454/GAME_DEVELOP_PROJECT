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
        else:
            control.handle_events(event)

    control.handle_events(None)

    
index=0            
field_set_info=[[400,30],[500,130],[400,230],[300,130],[400,30]]
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
