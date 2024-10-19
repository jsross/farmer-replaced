from __builtins__ import *
from Utility import *
from wall_follow_strategy import *
from game_board import *

def create_drone(graph, game_board):
    get_neighbor = game_board["get_neighbor"]
    get_plot = game_board["get_plot"]
    graph_add_edge = graph["add_edge"]
    graph_remove_edge = graph["remove_edge"]

    move_history = []

    properties = {
        "update_graph_on_success": True,
        "update_graph_on_failure": True
    }

    def follow_path(path):
        for direction in path:
            if not do_move(direction):
                return False

        return True
    
    def do_move(direction):
        start_op_count = get_op_count()

        starting_coords = get_coords()

        success = move(direction)

        if len(move_history) > 10:
            move_history.pop(0)

        if success:
            move_history.append(direction)
            
            if properties["update_graph_on_success"]:
                graph_add_edge(starting_coords, get_coords())
        else:
            quick_print("Bonk")

            if properties["update_graph_on_failure"]:
                target_coords = get_neighbor(starting_coords[0], starting_coords[1], direction)

                if target_coords != None:
                    graph_remove_edge(starting_coords, target_coords)

        quick_print("do_move: ", get_op_count() - start_op_count)

        return success
    
    def do_scan():
        plot = get_plot(get_coords())

        plot["entity_type"] = get_entity_type()
        plot["ground_type"] = get_ground_type()
        plot["measure"] = measure()
        plot["can_harvest"] = can_harvest()
        plot["water"] = get_water()
        plot["timestamp"] = get_time()
    
    def do_trade(seed_counts):
        for item_type in seed_counts:
            current_count = num_items(item_type)
            needed_count = seed_counts[item_type]
            to_buy = needed_count - current_count

            if to_buy > 0:
                trade(item_type, to_buy)

    def get_coords():
        current_coords = (get_pos_x(), get_pos_y())

        return current_coords
    
    def get_last_move():
        if len(move_history) > 0:
            return move_history[len(move_history) - 1]
        else:
            return None
        
    def execute_plot_plans(plot_plans, paths):
        for path in paths:
            plot_plan = plot_plans[get_pos_x()][get_pos_y()]
            execute_plot_plan(plot_plan)
            follow_path(path)

    def execute_plot_plan(plot_plan):
        for action in plot_plan:
            execute_action(action)

    def execute_action(action):
        func = action[0]
        arg_count = len(action) - 1

        if arg_count == 0:
            func()
        if arg_count == 1:
            func(action[1])
        if arg_count == 2:
            func(action[1],action[2])
        
    def set_property(name, value):
        properties[name] = value
    	
    new_drone = {
        "do_move": do_move,
        "do_trade": do_trade,
        "follow_path": follow_path,
        "get_coords": get_coords,
        "get_last_move": get_last_move,
        "set_property": set_property,
        "do_scan": do_scan,
        "execute_plot_plans": execute_plot_plans
    }

    return new_drone