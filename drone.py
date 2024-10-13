from __builtins__ import *
from Utility import *
from wall_follow_strategy import *
from game_board import *

def create_drone(graph, game_board):
    game_board_get_neighbor = game_board["get_neighbor"]
    get_distance = game_board["get_distance"]
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
    
    def go_to(dest_x, dest_y):
        start_op_count = get_op_count()

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
                quick_print("go_to: ", get_op_count() - start_op_count)
                return True
            
            if current_x < dest_x:
                move(East)
                current_x += 1
            elif current_x > dest_x:
                move(West)
                current_x -= 1

            if current_y < dest_y:
                move(North)
                current_y += 1
            elif current_y > dest_y:
                move(South)
                current_y -= 1

    def execute_action_plan(plan):
        for action in plan:
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

    def go_home():
        current_coords = get_coords()
        
        if current_coords != (0,0):
            go_to((0,0))

    def scan(action):
        start_op_count = get_op_count()
        
        go_home()

        size = get_world_size()

        for x_index in range(size):
            for y_index in range(size):
                action()

                if x_index % 2 == 0:
                    if y_index < size - 1:
                        move(North)
                    else:
                        move(East)
                else:
                    if y_index < size - 1:
                        move(South)
                    else:
                        move(East)

        quick_print("scan: ", get_op_count() - start_op_count)
    
    def search(check_goal):
        return do_wall_follow(new_drone, check_goal)
        
    def set_property(name, value):
        properties[name] = value
    	
    new_drone = {
        "do_move": do_move,
        "follow_path": follow_path,
        "get_coords": get_coords,
        "get_last_move": get_last_move,
        "set_property": set_property,
        "search": search,
        "go_to": go_to,
        "scan": scan,
        "go_home": go_home,
        "execute_action_plan": execute_action_plan
    }

    return new_drone