from __builtins__ import *
from graph import *
from farm import *

def create_navigator():
    
    graph = create_graph()
    
    add_edge = graph["add_edge"]
    remove_edge = graph["remove_edge"]
    get_connected = graph["get_connected"]
    get_edge_count = graph["get_edge_count"]
    
    def search(check_goal):
        print("Wall Follow")

        start_op_count = get_tick_count()
        
        last_move = None

        visited = {}

        while True:
            if check_goal():
                quick_print("do_wall_follow: ", get_tick_count() - start_op_count)

                return True

            if last_move == North:
                last_move = try_moves([West, North, East, South])
            elif last_move == East:
                last_move = try_moves([North, East, South, West])
            elif last_move == South:
                last_move = try_moves([East, South, West, North])
            elif last_move == West:
                last_move = try_moves([South, West, North, East])
            else:
                last_move = try_moves([West, North, East, South])
                
            current_coords = (get_pos_x(), get_pos_y())

            if current_coords in visited and visited[current_coords] == last_move:
                return False

            visited[(get_pos_x(), get_pos_y())] = last_move

    def best_guess_strategy(dest_coords):
        print("Best Guess")
        start_op_count = get_tick_count()
        visited_coords = []
        banned_edges = []

        # weights =  get_distance_map(dest_coords[0], dest_coords[1])

        last_coords = None
            
        while True:
            current_coords = (get_pos_x(), get_pos_y())

            if current_coords == dest_coords:
                quick_print("best_guess_strategy: ", get_tick_count() - start_op_count)

                return True

            #Dead end check
            if last_coords != None:
                last_neighbors = get_neighbors(last_coords[0],last_coords[1])
                last_neighbors.remove(current_coords)

                allowed_count = 0

                for last_neighbor in last_neighbors:
                    if not set([last_coords, last_neighbor]) in banned_edges:
                        allowed_count += 1
                
                if allowed_count == 0:
                    banned_edges.append(set([current_coords,last_coords]))

            neighbors = get_neighbors(current_coords[0], current_coords[1])

            if last_coords != None:
                neighbors.remove(last_coords)

            # TODO: Sort neighbords by distance to goal

            success = False

            for neighbor_coords in neighbors:
                edge = set([current_coords, neighbor_coords])

                if edge in banned_edges:
                    continue

                success = go_to(neighbor_coords[0], neighbor_coords[1])

                if success:
                    if not neighbor_coords in visited_coords:
                        visited_coords.append(neighbor_coords)

                    add_edge(edge)

                    break
                else:
                    banned_edges.append(edge)

            # If the drone was unable to go to any of the neighbors
            if not success:
                if last_coords != None: # If possible, go back to the last coords
                    go_to(last_coords[0], last_coords[1])
                else:
                    print("Error")
                    return False

            last_coords = current_coords
            

    def get_a_star_path(coord_start, coord_end):
        start_op_count = get_tick_count()
        
        distances_from_start = {}
                
        # The set of discovered nodes that may need to be (re-)expanded.
        # Initially, only the start node is known.
        # This is usually implemented as a min-heap or priority queue rather than a hash-set.
        set_open_coords = {coord_start}
        distances_from_start[coord_start] = 0
        weights = {
            coord_start: get_distance(coord_start, coord_end)
        }

        # For node n, came_from[n] is the node immediately preceding it on the cheapest path from the start
        # to n currently known.
        came_from = {}
        result_path = None
    
        while len(set_open_coords) > 0:
            # This operation can occur in O(Log(N)) time if openSet is a min-heap or a priority queue
            
            coord_current = find_lightest_node(set_open_coords, weights)

            if coord_current == coord_end:
                result_path = reconstruct_path(coord_current, came_from)

                break

            set_open_coords.remove(coord_current)

            neighbors = get_connected(coord_current)

            for neighbor in neighbors:
                #if this is the first time visiting this node, set some defaults
                if not neighbor in distances_from_start:
                    distances_from_start[neighbor] = 9999999999999

                if not neighbor in weights:
                    weights[neighbor] = 9999999999999

                # d(current,neighbor) is the weight of the edge from current to neighbor
                # tentative_gScore is the distance from start to the neighbor through current
                tenative_distance_from_start = distances_from_start[coord_current]  + 1

                if tenative_distance_from_start < distances_from_start[neighbor]:
                    # This path to neighbor is better than any previous one. Record it!
                    came_from[neighbor] = coord_current
                    distances_from_start[neighbor] = tenative_distance_from_start
                                    
                    # For node n, weight := distance_from_start + get_distance. Weight represents our current best guess as to
                    # how cheap a path could be from start to finish if it goes through n.
                    weights[neighbor]  = tenative_distance_from_start + get_distance(coord_end, neighbor)

                    set_open_coords.add(neighbor)

        quick_print("a_star: ", get_tick_count() - start_op_count)
        
        return result_path
    
    def try_coords(coords_list):
        current_coords = (get_pos_x(), get_pos_y())

        for coords in coords_list:
            if go_to(coords):
                add_edge(set([coords, current_coords]))
                
                return True
            else:
                remove_edge(set([coords, current_coords]))
        
        return False
    
    def try_moves(directions):
        start_coords = (get_pos_x(), get_pos_y())
        
        for direction in directions:
            if move(direction):
                edge = set([start_coords, (get_pos_x(), get_pos_y())])
                           
                add_edge(edge)

                return direction
            else:
                neighbor = get_neighbor(get_pos_x(), get_pos_y(), direction)

                edge = set([start_coords, neighbor])
                           
                remove_edge(edge)
    
        return False

    new_navigator = {
        "get_path": get_a_star_path,
        "search": search,
        "seak": best_guess_strategy
    }

    return new_navigator

def reconstruct_path(current, came_from):
    total_path = []

    while current in came_from:
        total_path.insert(0, current)
        
        current = came_from[current]
    
    if len(total_path) > 0:
        return total_path
    
    return None

def find_lightest_node(coords, weights):
    lightest = None
    lightest_weight = 9999999999999

    for current_coords in coords:
        current_weight = weights[current_coords]

        if current_weight < lightest_weight:
            lightest = current_coords
            lightest_weight = current_weight

    return lightest

def create_path(src_x, src_y, dest_x, dest_y):
    start_op_count = get_tick_count()

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

    quick_print("go_to: ", get_tick_count() - start_op_count)

    return path

def create_paths(coords_list):
    last_coords = (get_pos_x(),get_pos_y())
    paths = []

    for coords in coords_list:
        paths.append(create_path(last_coords[0],last_coords[1], coords[0], coords[1]))
        last_coords = coords

    return paths

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
