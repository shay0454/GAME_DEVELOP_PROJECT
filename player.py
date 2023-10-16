from pico2d import load_image
class HITTER:
    @staticmethod
    def enter():
        print('hitter')
    
    @staticmethod
    def exit():
        pass

    @staticmethod
    def do():
        pass

    @staticmethod
    def draw():
        pass


class Runner:
    @staticmethod
    def enter():
        print('runner')

    @staticmethod
    def exit():
        pass
    
    @staticmethod
    def do():
        pass

    @staticmethod
    def draw():
        pass


class Player:
    image=None
    if(image==None):
        image=load_image('NES-Baseball-Players.png')
    def __init__(self):
        pass
    def set_location(self,x,y):
        self.x,self.y=x,y

                   


