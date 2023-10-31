from pico2d import *
from main import players
field =[None,None,None,None,None] # 홈, 1루, 2루, 3루, 홈
strike,out

DE_lEN=3
class Field_control:
    def field_set():
        global field
        global strike,out
        global game_info
        field=[None,None,None,None,None]
        field_set_info=[[400,60],[600,90],[400,120],[200,90]]
        game_info={'is_hit':False,'is_out':False,'is_catch':False}
        strike, out=0,0
        for i in range(5):
            players[i].goto(field_set_info[i])
    '''
    def hitted():
        for i in range(4):
            if field[i] != None:
                field[i].run()

        for i in range(5):
            field[i].catch()

    def catched():
        for i in range(4):
            pass

    def run_to_next(e):
        for player in field:
            pass
            
    def info_update(e):
        if game_info['is_hit']:
            run_to_next()
    '''