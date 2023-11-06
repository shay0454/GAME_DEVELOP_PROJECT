import time
stack=[]
def change_mode(mode):
    global stack
    if len(stack)>0: 
        stack[-1].finish() #있을 시 종료 후, 해당 모드 삭제
        stack.pop
    stack.append(mode) #모드 add,init
    mode.init()

def push_mode(mode):
    global stack
    if len(stack)>0: #있을 시 pause
        stack[-1].pause()
    stack.append(mode) #모드 add,init
    mode.init()

def pop_mode(mode):
    global stack
    if len(stack)>0:
        stack.finish()
        stack.pop()

    if len(stack)>0:
        stack[-1].resume()

def quit():
    global running
    running = False

def run(start_mode):
    global running,stack
    running=True
    stack=[start_mode]
    start_mode.init()

    global frame_time
    frame_time=0.0
    cur_time=time.time()
    while running:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
        frame_time=time.time-cur_time
        frame_rate=1/frame_time
        cur_time+=frame_time

    # running == False 일 시
    while len(stack)>0:
        stack[-1].finish()
        stack.pop()
