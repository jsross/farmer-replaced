from graph import *

def best_guess_strategy(drone, graph, game_board, dest_coords):
    start_op_count = get_op_count()

    do_move = drone["do_move"]
    get_coords = drone["get_coords"]
    get_direction = game_board["get_direction"]
    get_distance = game_board["get_distance"]
    get_neighbor = game_board["get_neighbor"]
    add_edge = graph["add_edge"]
    remove_edge = graph["remove_edge"]
    get_connected = graph["get_connected"]

    last_coords = None
    dead_ends = set()
    visited = {}

    def find_lightest(coords):
        current_lightest = None
        lightest_weight = Infinity
 
        for current_coord in coords:
            current_weight = get_distance(dest_coords, current_coord)
            if current_weight < lightest_weight:
                current_lightest = current_coord
                lightest_weight = current_weight
        
        return current_lightest
    
    current_coords = get_coords()
        
    while True:
        if current_coords == dest_coords:
            quick_print("best_guess_strategy: ", get_op_count() - start_op_count)

            return True

        neighbors = list(get_connected(current_coords))
        
        if len(neighbors) == 0:
            exit(1)

        if last_coords in neighbors:
            neighbors.remove(last_coords)
 
        for dead_end in dead_ends:
            if dead_end in neighbors:
                neighbors.remove(dead_end)

        if len(neighbors) == 0:
            direction = get_direction(current_coords, last_coords)
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
            direction = get_direction(current_coords, lightest)

        success = do_move(direction)
        
        if success:
            last_coords = current_coords
            current_coords = get_coords()
            add_edge(last_coords, current_coords)

            if current_coords in visited and visited[current_coords] == direction:
                quick_print("best_guess_strategy: ", get_op_count() - start_op_count)
                return False

            visited[current_coords] = direction

            if last_coords != None and not last_coords in dead_ends:
                Last_neighbors = list(get_connected(last_coords))
                Last_neighbors.remove(current_coords)

                dead_end_count = 0

                for neighbor in Last_neighbors:
                    if neighbor in dead_ends:
                        dead_end_count += 1
                
                if dead_end_count >= len(Last_neighbors):
                    dead_ends.add(last_coords)
        else:
            target_coords = get_neighbor(current_coords[0], current_coords[1], direction)

            if target_coords != None:
                remove_edge(current_coords, target_coords)
            