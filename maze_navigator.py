from matrix import *
from farmer import *
from graph import *

def seak_coords(dest_coords, graph):
    start_op_count = get_tick_count()

    if(dest_coords == None):
        print("Bad Argument. No dest_coords")

        return False
    
    tested_edges = []
    traversed_edges = []
    banned_edges = []

    last_coords = None
    current_coords = (get_pos_x(), get_pos_y())

    while True:
        #print_graph(graph, banned_edges)

        neighbor_map = get_neighbor_map(current_coords[0], current_coords[1])
        weighted_neighbors = []

        for direction in neighbor_map:
            neighbor_coords = neighbor_map[direction]
            neighbor_coords = neighbor_map[direction]
            neighbor_edge = set([current_coords, neighbor_coords])

            if neighbor_edge in banned_edges:
                continue

            weighted_neighbor = {
                "coords": neighbor_coords,
                "direction": direction,
                "weight": get_distance(neighbor_coords, dest_coords),
                "edge": neighbor_edge
            }

            if neighbor_coords == last_coords:
                weighted_neighbor["weight"] = 999
            elif neighbor_edge in tested_edges:
                weighted_neighbor["weight"] =  997

            weighted_neighbors.append(weighted_neighbor)

        TopDownMergeSort(weighted_neighbors, "weight")

        success = False

        for weighted_neighbor in weighted_neighbors:
            neighbor_coords = weighted_neighbor["coords"]
            direction = weighted_neighbor["direction"]
            edge = weighted_neighbor["edge"]

            success = move(direction)

            if not edge in tested_edges:
                tested_edges.append(edge)

            if success:
                add_edge(graph, edge)

                break
            else:
                remove_edge(graph, edge)

        # If the drone was unable to go to any of the neighbors
        if not success:
            print("Error")

            return False
        
        last_coords = current_coords
        current_coords = (get_pos_x(), get_pos_y())
        last_edge = set([current_coords, last_coords])

        if current_coords == dest_coords:
            return True

        #Dead end check
        last_neighbors = get_neighbors(graph, last_coords)
        last_neighbors.remove(current_coords)

        last_neighbor_count = 0

        for direction in neighbor_map:
            neighbor_coords = neighbor_map[direction]
            neighbor_edge = set([last_coords, neighbor_coords])

            if neighbor_coords == current_coords:
                continue

            if neighbor_edge in banned_edges:
                continue

            if not neighbor_coords in last_neighbors and neighbor_edge in tested_edges:
                continue

            last_neighbor_count += 1
        
        if last_neighbor_count == 0 and not last_edge in banned_edges:
            banned_edges.append(last_edge)

        # Cycle Check
        if last_edge in traversed_edges:
            if len(weighted_neighbors) > 2:
                if in_cycle(graph, last_edge):
                    quick_print("Cycle Found")
                    if not last_edge in banned_edges:
                        banned_edges.append(last_edge)
        else:
            traversed_edges.append(last_edge)

def try_directions(directions):
    length = len(directions)

    for index in range(length):
        direction = directions[index]

        if move(direction):
            return index

    return -1

def search_for_goal(check_goal, graph):
    start_op_count = get_tick_count()

    search_order = {
        North: [West, North, East, South],
        East: [North, East, South, West],
        South: [East, South, West, North],
        West: [South, West, North, East],
        None: [West, North, East, South]
    }
    
    last_move = None

    while True:
        if check_goal():
            quick_print("search: ", get_tick_count() - start_op_count)

            return True
        
        start_coords = (get_pos_x(), get_pos_y())
        
        directions = search_order[last_move]
        result = try_directions(directions)

        if result < 0:
            return False
        
        last_move = directions[result]
        
        for index in range(result):
            blocked_direction = directions[index]
            neighbor_coords = get_neighbor(start_coords[0], start_coords[1], blocked_direction)
            
            if neighbor_coords != None:
                neighbor_edge = set([start_coords, neighbor_coords])
                remove_edge(graph, neighbor_edge)

        current_coords = (get_pos_x(), get_pos_y())
        new_edge = set([start_coords, current_coords])
        add_edge(graph, new_edge)