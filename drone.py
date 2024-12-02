from __builtins__ import *
from Utility import *
from wall_follow_strategy import *
from farm import *

def create_drone():
    move_history = []

    def follow_path(path):
        for index in range(len(path)):
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

    def execute_plot_plans(game_board, coords_list):
        get_plot = game_board["get_plot"]

        for coords in coords_list:
            go_to(coords[0], coords[1])
            plot = get_plot(get_coords())

            execute_plot_plan(plot["plan"])

    def execute_plot_plan(plot_plan):
        while len(plot_plan) > 0:
            action = plot_plan.pop(0)
            execute_action(action)

    def execute_action(action):
        func = action[0]
        arg_count = len(action) - 1

        if arg_count == 0:
            func()
        if arg_count == 1:
            func(action[1])
        if arg_count == 2:
            func(action[1], action[2])
        
    new_drone = {
        "do_move": do_move,
        "do_trade": do_trade,
        "follow_path": follow_path,
        "get_coords": get_coords,
        "get_last_move": get_last_move,
        "do_scan": do_scan,
        "execute_plot_plans": execute_plot_plans
    }

    return new_drone