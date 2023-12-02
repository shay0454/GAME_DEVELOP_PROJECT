from pico2d import*

objects=[[],[],[],[]] # 0 : field, 1 : base, 2: player, 3: ball

collision_pairs ={}

def add_collision_pair(group,a,b):
    if not group in collision_pairs: 
        print(f'Added new group {group}')
        collision_pairs[group]=[[],[]]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def add_object(o,depth=2):
    objects[depth].append(o)

def add_objects(obj_s,depth=2):
    for o in obj_s:
        objects[depth].append(o)

def update():
    for layer in objects:
        for o in layer:
            o.update()


def render():
    for layer in objects:
        for o in layer:
            o.draw()

def remove_collision_object(o):
    for pairs in  collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)

def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            return
        
    return ValueError("does not exist")
def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a,b):
                    a.handle_collision(group,b)
                    b.handle_collision(group,a)

def collide(a,b):
    left_a,bottom_a,right_a,top_a=a.get_bb()
    left_b,bottom_b,right_b,top_b=b.get_bb()
    
    if left_a>right_b: return False
    if right_a<left_b: return False
    if top_a<bottom_b: return False
    if bottom_a>top_b: return False

    return True
