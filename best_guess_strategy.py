from graph import *

def best_guess_strategy(drone, graph, game_board, distance_dict, check_goal):
    start_op_count = get_op_count()

    drone_do_move = drone["do_move"]
    get_coords = drone["get_coords"]
    gb_get_direction = game_board["get_direction"]
    graph_get_connected = graph["get_connected"]

    last_coords = None
    dead_ends = set()
    visited = {}

    def find_lightest(coords):
        current_lightest = coords[0]
        lightest_weight = distance_dict[current_lightest]
 
        for current_coord in coords:
            current_weight = distance_dict[current_coord]
            if current_weight < lightest_weight:
                current_lightest = current_coord
                lightest_weight = current_weight
        
        return current_lightest
    
    current_coords = get_coords()
        
    while True:
        if check_goal():
            quick_print("best_guess_strategy: ", get_op_count() - start_op_count)

            return True

        neighbors = list(graph_get_connected(current_coords))
        
        if len(neighbors) == 0:
            exit(1)

        if last_coords in neighbors:
            neighbors.remove(last_coords)
 
        for dead_end in dead_ends:
            if dead_end in neighbors:
                neighbors.remove(dead_end)

        if len(neighbors) == 0:
            direction = gb_get_direction(current_coords, last_coords)
        else:
            unvisited = []

            for neighbor in neighbors:
                if not neighbor in visited:
                    unvisited.append(neighbor)

            if len(unvisited) > 0:
                lightest = find_lightest(unvisited)
            else:
                lightest = find_lightest(neighbors)
        
            lightest = find_lightest(neighbors)
            direction = gb_get_direction(current_coords, lightest)

        success = drone_do_move(direction)
        
        if success:
            last_coords = current_coords
            current_coords = get_coords()

            if current_coords in visited and visited[current_coords] == direction:
                quick_print("best_guess_strategy: ", get_op_count() - start_op_count)
                return False

            visited[current_coords] = direction

            if last_coords != None and not last_coords in dead_ends:
                Last_neighbors = list(graph_get_connected(last_coords))
                Last_neighbors.remove(current_coords)

                dead_end_count = 0

                for neighbor in Last_neighbors:
                    if neighbor in dead_ends:
                        dead_end_count += 1
                
                if dead_end_count >= len(Last_neighbors):
                    dead_ends.add(last_coords)
            