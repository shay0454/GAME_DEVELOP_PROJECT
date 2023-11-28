
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
    batter.goto(control.batter_location)

# picker 상태를 Shoot으로 변경
def set_picker_Shoot(control):
    control.picker[0].state_machine.change_state(control.player_state_list['Shoot'],('CHANGE',0))

# batter 상태를 Hit으로 변경
def set_batter_Hit(control):
    control.batter[0].state_machine.change_state(control.player_state_list['Hit'])

# Start 전에 셋팅
def set_Start(control):
    control.state_machine.change_state(control.state_list['Start'])
    print(control.fielders[0].state_machine.cur_state)
    set_picker_Shoot(control)
    set_batter_Hit(control)

# 모든 player 도착지 초기화
def players_destination_init(control):
    picker_destination_init(control,control.picker[0])
    fielders_destination_init(control,control.fielders)
    basemen_destination_init(control,control.basemen)
    batter_destination_init(control,control.batter[0]) 