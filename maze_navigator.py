from farmer import *
from graph import *

def create_maze_navigator():

    graph = create_graph(get_distance)
    
    add_edge = graph["add_edge"]
    remove_edge = graph["remove_edge"]
    in_cycle = graph["in_cycle"]
    get_path = graph["get_path"]

    def check_is_treasure():
        return get_entity_type() == Entities.Treasure
    
    def do_create_maze():
        world_size = get_world_size()
        clear()
        plant(Entities.Bush)
    
        while not can_harvest():
            pass
            
        use_item(Items.Weird_Substance, world_size)

        for index in range(world_size):
            south_coords = (index, 0)
            east_coords = (0, index)

            south_neighbor = get_neighbor(south_coords[0], south_coords[1], South)
            remove_edge(set([south_coords, south_neighbor]))

            east_neighbor = get_neighbor(east_coords[0], east_coords[1], East)
            remove_edge(set([east_coords, east_neighbor]))

    def execute_plan(iterations):
        
        if search(check_is_treasure) == False:
            print("Treasure not found: Abort!")
            
            return

        for _ in range(1, iterations):
            success = False

            next_coords = measure()
            use_item(Items.Weird_Substance, get_world_size())
            
            path = get_path((get_pos_x(), get_pos_y()), next_coords)
            
            if path != None:
                follow_path(path)

                success = get_entity_type() == Entities.Treasure

            if not success:
                success = best_guess_strategy(next_coords)

            if get_entity_type() != Entities.Treasure:
                print("Treasure Not Found! Abort!")
                break

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
                last_neighbors.remove(current_coords)

                allowed_count = 0

                for last_neighbor in last_neighbors:
                    if not set([last_coords, last_neighbor]) in banned_edges:
                        allowed_count += 1

                last_edge = set([current_coords, last_coords])
                
                if allowed_count == 0:
                    banned_edges.append(last_edge)
                elif current_coords in visited_coords:
                    if in_cycle(last_edge):
                        print("Cycle!!!!!")
                        banned_edges.append(last_edge)
                        remove_edge(last_edge)

            visited_coords.append(current_coords)        

            neighbor_coords_list = get_neighbors(current_coords[0], current_coords[1])
            weighted_neighbors = []

            for neighbor_coords in neighbor_coords_list:
                weight = 0

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
           
    new_maze_plan = {
        "do_create_maze": do_create_maze,
        "execute_plan": execute_plan
    }

    return new_maze_plan