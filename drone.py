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
        
    def go_to(x, y):
        path = create_path(get_pos_x(), get_pos_y(), x, y)

        return follow_path(path)

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

def do_trade(needed_seed_counts):
	for item_type in needed_seed_counts:
		current_count = num_items(item_type)
		needed_count = needed_seed_counts[item_type]
		to_buy = needed_count - current_count

		if to_buy > 0:
			trade(item_type, to_buy)

		needed_seed_counts[item_type] = 0