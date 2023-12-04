from pico2d import delay

# picker 도착지 초기화
def picker_destination_init(control,picker):
    picker.goto(control.picker_location)

# fielders 도착지 초기화
def fielders_destination_init(control,fielders):
    for fielder in fielders:
        fielder.goto(control.fielder_locations[fielders.index(fielder)-1])

# basemen 도착지 초기화
def basemen_destination_init(control,basemen):
    for baseman in control.basemen:
        baseman.goto(control.base_locations[basemen.index(baseman)])
    catcher_destination_init(control,control.basemen[0])

# catcher 도착지 초기화
def catcher_destination_init(control,catcher):
    catcher.goto(control.catcher_location)

# batter 도착지 초기화
def batter_destination_init(control,batter):
     batter.goto([*control.batter_location])

# picker 상태를 Shoot으로 변경
def set_picker_Shoot(control):
    control.picker[0].state_machine.change_state(control.player_state_list['Shoot'],('CHANGE',0))

# batter 상태를 Hit으로 변경
def set_batter_Hit(control):
    control.batter[0].state_machine.change_state(control.player_state_list['Hit'])

def set_the_catcher_Ready(control):
    control.basemen[0].state_machine.change_state(control.player_state_list['The_Catcher'],('CHANGE',0))

def change_state_Start(control):
    control.state_machine.change_state(control.state_list['Start'])
# Start 전에 셋팅
def set_Start(control):
    print('set_start')
    print(control.fielders[0].state_machine.cur_state)
    set_picker_Shoot(control)
    set_batter_Hit(control)
    set_the_catcher_Ready(control)

#수비수 모두 현 위치에서 정지
def defender_stop(control):
    fielder_stop(control)
    picker_stop(control)
    
#투수 현 위치에서 정지
def picker_stop(control):
    control.picker[0].stop()

#fiedlers 현 위치에서 정지
def fielder_stop(control):
    for fielder in control.fielders:
        fielder.stop()

def baseman_stop(control):
    for baseman in control.basemen:
        baseman.stop()

def batter_run(control):
    batter=control.batter[0]
    control.runners.append(batter)
    control.runners[-1].goto([560,230])
    control.batter=[]

# 모든 player 도착지 초기화
def players_destination_init(control):
    picker_destination_init(control,control.picker[0])
    fielders_destination_init(control,control.fielders)
    basemen_destination_init(control,control.basemen)
    batter_destination_init(control,control.batter[0]) 

# picker 위치 초기화
def picker_location_init(control,picker):
    picker.location=control.picker_location

# catcher 위치 초기화
def catcher_location_init(control,catcher):
    catcher.location = control.catcher_location

# fielders 위치 초기화
def fielders_location_init(control,fielders):
    for fielder in fielders:
        fielder.location=control.fielder_locations[fielders.index(fielder)-1]

# basemen 위치 초기화
def basemen_location_init(control,basemen):
    for baseman in control.basemen:
        baseman.location=control.base_locations[basemen.index(baseman)]
    catcher_location_init(control,control.basemen[0])

# batter 위치 초기화
def batter_location_init(control,batter):
    batter.location = [*control.batter_location]

def players_location_init(control):
    picker_location_init(control,control.picker[0])
    fielders_location_init(control,control.fielders)
    basemen_location_init(control,control.basemen)
    batter_location_init(control,control.batter[0]) 

def all_players_stop(control):
    for object_list in control.players:
        for player in object_list:
            player.state_machine.change_state(control.player_state_list['Idle'],('CHANGE',0))