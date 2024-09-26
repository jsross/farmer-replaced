from __builtins__ import *
from Utility import *

def create_drone(graph, game_board):
    game_board_get_neighbor = game_board["get_neighbor"]
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
                target_coords = game_board_get_neighbor(starting_coords[0], starting_coords[1], direction)

                if target_coords != None:
                    graph_remove_edge(starting_coords, target_coords)

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
        
    def set_property(name, value):
        properties[name] = value
    	
    drone = {
        "do_move": do_move,
        "follow_path": follow_path,
        "get_coords": get_coords,
        "get_last_move": get_last_move,
        "set_property": set_property
    }

    return drone