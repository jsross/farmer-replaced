from __builtins__ import *
from Utility import *

def create_drone(graph, game_board):
    game_board_get_neighbor = game_board["get_neighbor"]
    graph_add_edge = graph["add_edge"]
    graph_remove_edge = graph["remove_edge"]

    move_history = []

    def go_to(coord):
        x = coord[0]
        y = coord[1]
        
        while True:
            moved = False

            current_coords = get_coords()

            if current_coords[0] < x:
                moved = moved or move(East)
            elif current_coords[0] > x:
                moved = moved or move(West)

            if current_coords[1] < y:
                moved = moved or move(North)
            elif current_coords[1] > y:
                moved = moved or move(South)
                
            if not moved:
                break
            
        return coord == get_coords()
		
    def follow_path(path):
        for coord in path:
            if not go_to(coord):
                return False

        return True

    def do_move(direction):
        success = move(direction)
        
        start_ops = get_op_count()
        
        starting_coords = get_coords()

        if success:
            move_history.append(direction)
            graph_add_edge(starting_coords, get_coords())
        else:
            target_coords = game_board_get_neighbor(starting_coords, direction)

            if target_coords != None:
                graph_remove_edge(starting_coords, target_coords)

        quick_print(get_op_count() - start_ops)

        return success

    def get_coords():
        return (get_pos_x(), get_pos_y())
    
    def get_last_move():
        return move_history[len(move_history) - 1]
    	
    drone = {
        "go_to": go_to,
        "do_move": do_move,
        "follow_path": follow_path,
        "get_coords": get_coords,
        "get_last_move": get_last_move
    }

    return drone