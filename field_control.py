from pico2d import *
field =[None,None,None,None,None] # 홈, 1루, 2루, 3루, 홈
DE_lEN=3
def field_set():
    global field
    global strike,out
    global game_info
    field=[None,None,None,None,None]
    game_info={'is_hit':False,'is_out':False,'is_catch':False}
    strike, out=0,0
def hitted():
    for i in range(4):
        if field[i] != None:
            field[i].run()

    for i in range(DE_LEN):
        field[i].catch()

def catched():
    for i in range(4):
        pass


def info_update(e):
    if game_info['is_hit']:
        for i in range(4):
            pass

