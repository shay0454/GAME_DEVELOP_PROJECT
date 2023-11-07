from pico2d import *
import logo_mode as start_mode
#import title_mode as start_mode
#import play_mode as start_mode
import game_framework
import os
os.chdir(os.path.dirname(__file__))

open_canvas()
game_framework.run(start_mode)
close_canvas()