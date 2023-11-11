from pico2d import *
import game_framework
import play_mode
def init():
    global image,temp,button
    image=load_image('white_background.png')
    temp=load_font('ENCR10B.TTF', 50)
    button=load_image('start_button.png') #https://www.flaticon.com/free-icon/start-button_5261929

def finish():
    global temp,image
    del temp,image

def handle_events():
    events=get_events()
    for event in events:
        if event.type==SDL_MOUSEBUTTONDOWN:
            if(event.x>=300 and event.x<=500 and event.y<=600-50-1 and event.y>=600-250-1):
                game_framework.change_mode(play_mode)
        elif event.type==SDL_KEYDOWN and event.key==SDLK_ESCAPE:
            game_framework.quit()
        

def update():
    pass

def draw():
    clear_canvas()
    image.draw(400,300)
    temp.draw(275,450,'BASEBALL')
    temp.draw(275,400,'  GAME  ')
    button.draw(400,200,400,300)
    update_canvas()
