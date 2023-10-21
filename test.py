from pico2d import *
import os
os.chdir(os.path.dirname(__file__))
x,y=400,300
dir_x,dir_y=0,0
running=True
frame=0
face,updown='',0
def handle_event():
    global running, x,y,dir_x,dir_y,face,updown
    events=get_events()
    for e in events:
        if e.type==SDL_KEYDOWN:
            if e.key==SDLK_ESCAPE:
                running=False
            elif e.key==SDLK_d:
                dir_x+=1
                face=''
            elif e.key==SDLK_a:
                dir_x-=1
                face='h'
            elif e.key==SDLK_w:
                dir_y+=1
                updown=1
            elif e.key==SDLK_s:
                dir_y-=1
                updown=0
        elif e.type==SDL_KEYUP:
            if e.key==SDLK_d:
                dir_x-=1
            elif e.key==SDLK_a:
                dir_x+=1
            elif e.key==SDLK_w:
                dir_y-=1
            elif e.key==SDLK_s:
                dir_y+=1

def update():
    global frame,x,y,face
    frame=(frame+1)%6
    x+=dir_x*10
    y+=dir_y*10

def draw(a):
    global frame,x
    if a==1:
        ch.clip_composite_draw((frame//3)*16+18,320+24-updown*24,16,20,0,face,x,y,80,60)
    elif a==2:
        list=[0,2,5,8,12,15]
        list_1=[16,24,24,24,24,24]
        list_2=[24,24,0,0,0,24]
        ch.clip_composite_draw(list[frame]*8,488-72,list_1[frame],32,0,'',x-list_2[frame],y,80*(list_1[frame])/24,60)


open_canvas()
ch=load_image('Baseball_Players.png')
while(running):
    clear_canvas()
    handle_event()
    update()
    draw(2)
    update_canvas()
    delay(0.3)
close_canvas()