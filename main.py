from pico2d import *
import logo_mode as start_mode
#import title_mode as start_mode
#import play_mode as start_mode
import game_framework


open_canvas(800,800,True)
game_framework.run(start_mode)
close_canvas()