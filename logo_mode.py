import game_framework
import title_mode
from pico2d import *

def init():
    global image
    global running
    global logo_start_time
    image=[load_image('white_background.png'),load_image('loading.png')]
    logo_start_time=get_time()

def finish():
    pass

def update():
    global running
    global logo_start_time
    if get_time()-logo_start_time>=2.0:
        running =False
        game_framework.change_mode(title_mode)

def draw():
    clear_canvas()
    image[0].draw(400,300)
    image[1].clip_composite_draw(0,0,64,64,get_time()*15,'',400,300)
    update_canvas()

def handle_events():
    events=get_events()
