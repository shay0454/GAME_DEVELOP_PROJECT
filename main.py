import pico2d
import play_mode
import os
os.chdir(os.path.dirname(__file__))

pico2d.open_canvas()
play_mode.create_world()
while play_mode.running:
    play_mode.update_world()
    play_mode.render_world()
    play_mode.handle_events()
    play_mode.check_players()
    pico2d.delay(0.01)

play_mode.finish()

pico2d.close_canvas()