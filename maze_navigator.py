from farmer import *
from graph import *

def seak_coords(dest_coords, graph):
    start_op_count = get_tick_count()

    if(dest_coords == None):
        print("Bad Argument. No dest_coords")

        return False
    
    add_edge = graph["add_edge"]
    remove_edge = graph["remove_edge"]
    in_cycle = graph["in_cycle"]
    
    visited_coords = []
    banned_edges = []

    last_coords = None
        
    while True:
        current_coords = (get_pos_x(), get_pos_y())

        if current_coords == dest_coords:
            quick_print("best_guess_strategy: ", get_tick_count() - start_op_count)

            return True

        #Dead end check
        if last_coords != None:
            last_neighbors = get_neighbors(last_coords[0], last_coords[1])

            allowed_count = 0

            for direction in last_neighbors:
                neighbor_coords = last_neighbors[direction]

                if neighbor_coords == current_coords:
                    continue

                if not set([last_coords, neighbor_coords]) in banned_edges:
                    allowed_count += 1

            last_edge = set([current_coords, last_coords])
            
            if allowed_count == 0:
                banned_edges.append(last_edge)
            elif current_coords in visited_coords:
                if in_cycle(last_edge):
                    quick_print("Cycle Found")
                    banned_edges.append(last_edge)
                    remove_edge(last_edge)

        visited_coords.append(current_coords)        

        neighbors = get_neighbors(current_coords[0], current_coords[1])
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
                add_edge(edge)

                break
            else:
                banned_edges.append(edge)

        # If the drone was unable to go to any of the neighbors
        if not success:
            print("Error")

            return False

        last_coords = current_coords

def try_directions(directions):
    length = len(directions)

    for index in range(length):
        direction = directions[index]

        if move(direction):
            return index

    return -1

def search_for_goal(check_goal, graph):
    start_op_count = get_tick_count()

    remove_edge = graph["remove_edge"]
    add_edge = graph["add_edge"]

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
            remove_edge(set([start_coords, neighbor_coords]))

        add_edge(set([start_coords, (get_pos_x(), get_pos_y())]))