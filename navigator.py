from __builtins__ import *

def create_navigator(drone, graph, game_board):
    
    add_edge = graph["add_edge"]
    remove_edge = graph["remove_edge"]
    get_connected = graph["get_connected"]
    get_edge_count = graph["get_edge_count"]
    
    get_last_move = drone["get_last_move"]
    get_coords = drone["get_coords"]
    do_move = drone["do_move"]
    follow_path = drone["follow_path"]

    get_neighbor = game_board["get_neighbor"]
    get_distance = game_board["get_distance"]
    get_direction = game_board["get_direction"]

    def search(check_goal):
        start_op_count = get_op_count()
        
        last_move = None

        visited = {}

        def try_moves(directions):
            success = False
            last_coords = get_coords()
            
            for direction in directions:
                success = do_move(direction)
                
                if success:
                    add_edge(last_coords, get_coords())

                    break
                else:
                    remove_edge(get_coords(), get_neighbor(get_pos_x(), get_pos_y(), direction))
            
            return success

        while True:
            if check_goal():
                quick_print("do_wall_follow: ", get_op_count() - start_op_count)

                return True

            if last_move == North:
                try_moves([West, North, East, South])
            elif last_move == East:
                try_moves([North, East, South, West])
            elif last_move == South:
                try_moves([East, South, West, North])
            elif last_move == West:
                try_moves([South, West, North, East])
            else:
                try_moves([West, North, East, South])
                
            current_coords = get_coords()

            last_move = get_last_move()

            if current_coords in visited and visited[current_coords] == last_move:
                return False

            visited[get_coords()] = get_last_move()

    def seak(dest_coords):
        success = False

        quick_print("edge count: ", get_edge_count())
        
        path = get_a_star_path(get_coords(), dest_coords)

        if(path != None and len(path) > 0):
            success = follow_path(path)

        if success:
            return True
        
        best_guess_strategy(dest_coords)

    def best_guess_strategy(dest_coords):
        start_op_count = get_op_count()

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

    def get_a_star_path(coord_start, coord_end):
        start_op_count = get_op_count()
        weights = {}
        distances_from_start = {}

        def reconstruct_path(current):
            total_path = []

            while current in cameFrom:
                next = cameFrom[current]

                current_x = current[0]
                current_y = current[1]
                
                next_x = next[0]
                next_y = next[1]
                
                if next_x > current_x:
                    total_path.insert(0, West)
                elif next_x < current_x:
                    total_path.insert(0, East)
                elif next_y > current_y:
                    total_path.insert(0, South)
                elif next_y < current_y:
                    total_path.insert(0, North)
                
                current = next
            
            if len(total_path) > 0:
                return total_path
            
            return None

        def find_lightest_node(set_coords):
            lightest = None

            for current_coord in set_coords:
                if lightest == None:
                    lightest = current_coord
                else:
                    if weights[current_coord] < weights[lightest]:
                        lightest = current_coord

            return lightest
                
        # The set of discovered nodes that may need to be (re-)expanded.
        # Initially, only the start node is known.
        # This is usually implemented as a min-heap or priority queue rather than a hash-set.
        set_open_coords = {coord_start}

        distances_from_start[coord_start] = 0

        # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from the start
        # to n currently known.
        cameFrom = {}
        result_path = None
    
        while len(set_open_coords) > 0:
            # This operation can occur in O(Log(N)) time if openSet is a min-heap or a priority queue
            
            coord_current = find_lightest_node(set_open_coords)

            if coord_current == coord_end:
                result_path = reconstruct_path(coord_current)
                break 

            set_open_coords.remove(coord_current)

            neighbors = get_connected(coord_current)

            for neighbor in neighbors:
                #if this is the first time visiting this node, set some defaults
                if not neighbor in distances_from_start:
                    distances_from_start[neighbor] = Infinity

                if not neighbor in weights:
                    weights[neighbor] = Infinity

                # d(current,neighbor) is the weight of the edge from current to neighbor
                # tentative_gScore is the distance from start to the neighbor through current
                tenative_distance_from_start = distances_from_start[coord_current]  + 1

                if tenative_distance_from_start < distances_from_start[neighbor]:
                    # This path to neighbor is better than any previous one. Record it!
                    cameFrom[neighbor] = coord_current
                    distances_from_start[neighbor] = tenative_distance_from_start
                                    
                    # For node n, weight := distance_from_start + get_distance. Weight represents our current best guess as to
                    # how cheap a path could be from start to finish if it goes through n.
                    weights[neighbor]  = tenative_distance_from_start + get_distance(coord_end, neighbor)

                    set_open_coords.add(neighbor)

        quick_print("a_star: ", get_op_count() - start_op_count)
        
        return result_path

    new_navigator = {
        "search": search,
        "seak": seak
    }

    return new_navigator

def create_path(src_x, src_y, dest_x, dest_y):
    start_op_count = get_op_count()

    current_x = src_x
    current_y = src_y

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
            path.append(East)
            current_x += 1
        elif current_x > dest_x:
            path.append(West)
            current_x -= 1

        if current_y < dest_y:
            path.append(North)
            current_y += 1
        elif current_y > dest_y:
            path.append(South)
            current_y -= 1

    quick_print("go_to: ", get_op_count() - start_op_count)

    return path

def create_scan_paths(width, height):
    paths = []

    current_x = 0
    current_y = 0

    for x_index in range(width):
        for y_index in range(height):
            if x_index % 2 == 0:
                if y_index < height - 1:
                    paths.append([North])
                    current_y += 1
                else:
                    paths.append([East])
                    current_x += 1
            else:
                if y_index < height - 1:
                    paths.append([South])
                    current_y -= 1
                else:
                    paths.append([East])
                    current_x += 1

    return paths
