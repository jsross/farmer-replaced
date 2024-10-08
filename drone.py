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
    
    def go_to(dest_coords):
        start_op_count = get_op_count()
        
        path = get_shortest_path(dest_coords)
        success = follow_path(path)
        
        quick_print("go_to: ", get_op_count() - start_op_count)
        
        return success
    
    def get_shortest_path(dest_coords):
        start_op_count = get_op_count()
        current_coords = get_coords()

        current_x = current_coords[0]
        current_y = current_coords[1]

        world_size = get_world_size()
        neg_world_size = world_size * -1
        radius = world_size / 2

        min_x = current_x - radius
        max_x = current_x + radius
        min_y = current_y - radius
        max_y = current_y + radius

        coords = set()
        coords.add(dest_coords)

        def add_coords(to_add):
            x = to_add[0]
            y = to_add[1]

            if min_x <= x <= max_x and min_y <= y <= max_y:
                coords.add(to_add)

        add_coords(translate_coords(dest_coords, 0, world_size))
        add_coords(translate_coords(dest_coords, world_size, world_size))
        add_coords(translate_coords(dest_coords, world_size, 0))
        add_coords(translate_coords(dest_coords, world_size, neg_world_size))
        add_coords(translate_coords(dest_coords, 0, neg_world_size))
        add_coords(translate_coords(dest_coords, neg_world_size, neg_world_size))
        add_coords(translate_coords(dest_coords, neg_world_size, 0))
        add_coords(translate_coords(dest_coords, neg_world_size, world_size))
        
        closest_coords = find_closest(current_coords, coords)

        closets_x = closest_coords[0]
        closets_y = closest_coords[1]
        
        path = []

        while True:
            if current_x == closets_x and current_y == closets_y:
                break
            
            if current_x < closets_x:
                path.append(East)
                current_x += 1
            elif current_x > closets_x:
                path.append(West)
                current_x -= 1

            if current_y < closets_y:
                path.append(North)
                current_y += 1
            elif current_y > closets_y:
                path.append(South)
                current_y -= 1

        quick_print("get_shortest_path: ", get_op_count() - start_op_count)
        
        return path
                

    def search(check_goal):
        return do_wall_follow(new_drone, check_goal)
        
    def set_property(name, value):
        properties[name] = value
    
    def find_closest(target, coord_set):
        start_op_count = get_op_count()
        closest = None
        closest_dist = Infinity

        for current_coords in coord_set:
            current_distance = get_distance(target, current_coords)

            if current_distance < closest_dist:
                closest = current_coords
                closest_dist = current_distance

        quick_print("find_closest: ", get_op_count() - start_op_count)

        return closest
    	
    new_drone = {
        "do_move": do_move,
        "follow_path": follow_path,
        "get_coords": get_coords,
        "get_last_move": get_last_move,
        "set_property": set_property,
        "search": search,
        "go_to": go_to
    }

    return new_drone