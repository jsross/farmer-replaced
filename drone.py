from __builtins__ import *
from Utility import *

def follow_path(path):
    path_length = len(path)
    
    for index in range(path_length):
        coords = path[index]

        if not go_to(coords[0], coords[1]):
            return -index

    return 0

def go_to(dest_x, dest_y):
    start_op_count = get_tick_count()

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

    success = False

    while True:
        if current_x == dest_x and current_y == dest_y:
            success = True
            break
        
        if current_x < dest_x:
            if not move(East):
                break

            current_x += 1

        elif current_x > dest_x:
            if not move(West):
                break

            current_x -= 1

        if current_y < dest_y:
            if not move(North):
                break

            current_y += 1
           
        elif current_y > dest_y:
            if not move(South):
                break
            current_y -= 1

    quick_print("go_to: ", get_tick_count() - start_op_count)

    return success