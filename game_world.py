from pico2d import*

objects=[[],[],[],[]]

def add_object(o,depth=2):
    objects[depth].append(o)


def update():
    for layer in objects:
        for o in layer:
            o.update()


def render():
    for layer in objects:
        for o in layer:
            o.draw()


def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            return
        
    return ValueError("does not exist")