from matrix import *
from farmer import *
from graph import *

def seak_coords(dest_coords, graph):
    start_op_count = get_tick_count()

    if(dest_coords == None):
        print("Bad Argument. No dest_coords")

        return False
    
    visited_coords = set()
    banned_edges = []

    last_coords = None
    current_coords = (get_pos_x(), get_pos_y())

    while True:
        visited_coords.add(current_coords)

        print_graph(graph, banned_edges)

        neighbors = get_neighbor_map(current_coords[0], current_coords[1])
        weighted_neighbors = []

        for direction in neighbors:
            weight = 0
            neighbor_coords = neighbors[direction]

            if neighbor_coords == last_coords:
                weight = 99
            elif neighbor_coords in visited_coords:
                weight = 98
            else:
                weight = get_distance(neighbor_coords, dest_coords)

            weighted_neighbors.append((weight, neighbor_coords))

        TopDownMergeSort(weighted_neighbors, 0)

        success = False

        for weighted_neighbor in weighted_neighbors:
            neighbor_coords = weighted_neighbor[1]
            edge = set([current_coords, neighbor_coords])

            if edge in banned_edges:
                continue

            success = go_to(neighbor_coords[0], neighbor_coords[1])

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
        
        # Cycle Check
        if current_coords in visited_coords:
            neighbors = get_neighbors(graph, current_coords)

            if len(neighbors) > 2:
                if in_cycle(graph, last_edge):
                    quick_print("Cycle Found")
                    if not last_edge in banned_edges:
                        banned_edges.append(last_edge)

        #Dead end check
        last_neighbors = get_neighbors(graph, last_coords)
        last_neighbors.remove(current_coords)

        last_neighbor_count = 0

        for last_neighbor in last_neighbors:
            if not set([last_coords, last_neighbor]) in banned_edges:
                last_neighbor_count += 1
        
        if last_neighbor_count == 0:
            if not last_edge in banned_edges:
                banned_edges.append(last_edge)

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