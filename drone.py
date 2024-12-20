from __builtins__ import *
from Utility import *
from farm import *

def do_scan():
    scan_results = {
        "entity_type": get_entity_type(),
        "ground_type": get_ground_type(),
        "measure": measure(),
        "can_harvest": can_harvest(),
        "water": get_water(),
        "timestamp": get_time()
    }

    return scan_results

def follow_path(path):
    path_length = len(path)
    
    for index in range(path_length):
        coords = path[index]

        if not go_to(coords[0], coords[1]):
            return index

    return True

def go_to(dest_x, dest_y):
    # start_op_count = get_tick_count()

    current_x = get_pos_x()
    current_y = get_pos_y()
    world_size = get_world_size()
    radius = world_size / 2
    
    x_multiplier = 0
    y_multiplier = 0

    if current_x < radius and dest_x > radius:
        x_multiplier = -1
    if current_x > radius and dest_x < radius:
        x_multiplier = 1
    
    if current_y < radius and dest_y > radius:
        y_multiplier = -1
    if current_y > radius and dest_y < radius:
        y_multiplier = 1

    dest_x += world_size * x_multiplier
    dest_y += world_size * y_multiplier

    while True:
        if current_x == dest_x and current_y == dest_y:
            return True
        
        if current_x < dest_x:
            if move(East):
                current_x += 1
            else:
                return False
        elif current_x > dest_x:
            if move(West):
                current_x -= 1
            else:
                return False

        if current_y < dest_y:
            if move(North):
                current_y += 1
            else:
                return False
        elif current_y > dest_y:
            if move(South):
                current_y -= 1
            else:
                return False

    # quick_print("go_to: ", get_tick_count() - start_op_count)