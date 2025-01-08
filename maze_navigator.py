from farmer import *
from graph import *

def create_maze_navigator(graph):

    add_edge = graph["add_edge"]
    remove_edge = graph["remove_edge"]
    in_cycle = graph["in_cycle"]

    def search(check_goal):
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
        if(dest_coords == None):
            print("Bad Argument. No dest_coords")

            return False

        start_op_count = get_tick_count()
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
           
    new_maze_plan = {
        "search": search,
        "seak": best_guess_strategy
    }

    return new_maze_plan