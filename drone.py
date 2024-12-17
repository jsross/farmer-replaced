from __builtins__ import *
from Utility import *
from farm import *

def create_drone():
    move_history = []

    def follow_path(path):
        path_length = len(path)
        
        for index in range(path_length):
            direction = path[index]

            if not do_move(direction):
                return index

        return True
    
    def do_move(direction):
        start_op_count = get_op_count()

        success = move(direction)

        if len(move_history) > 10:
            move_history.pop(0)

        if success:
            move_history.append(direction)
            
        quick_print("do_move: ", get_op_count() - start_op_count)

        return success
    
    def get_coords():
        current_coords = (get_pos_x(), get_pos_y())

        return current_coords
    
    def get_last_move():
        if len(move_history) > 0:
            return move_history[len(move_history) - 1]
        else:
            return None
        
    new_drone = {
        "do_move": do_move,
        "follow_path": follow_path,
        "get_coords": get_coords,
        "get_last_move": get_last_move,
        "go_to": go_to
    }

    return new_drone

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

def go_to(dest_x, dest_y):
    # start_op_count = get_op_count()

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

    path = []

    while True:
        if current_x == dest_x and current_y == dest_y:
            break
        
        if current_x < dest_x:
            move(East)
            path.append(East)

            current_x += 1

        elif current_x > dest_x:
            move(West)
            path.append(West)

            current_x -= 1

        if current_y < dest_y:
            move(North)
            path.append(North)

            current_y += 1
        elif current_y > dest_y:
            move(South)
            path.append(South)
            current_y -= 1

    # quick_print("go_to: ", get_op_count() - start_op_count)