from a_star import *

def create_maze_plan(drone, graph, game_board):
    drone_get_coords = drone["get_coords"]
    drone_follow_path = drone["follow_path"]
    drone_search = drone["search"]

    def check_is_treasure():
        return get_entity_type() == Entities.Treasure
    
    def do_create_maze():
        clear()
        plant(Entities.Bush)
    
        while not can_harvest():
            pass
            
        while get_entity_type() == Entities.Bush:
            if num_items(Items.Fertilizer) == 0:
                trade(Items.Fertilizer, 100)
            use_item(Items.Fertilizer)

    def execute_plan(iterations):
        drone["set_property"]("update_graph_on_success", False)
        success = drone_search(check_is_treasure)
        next_coords = measure()
        
        if success == False:
            print("Abort")
            
            return

        for _ in range(iterations):
            success = False

            while get_entity_type() == Entities.Treasure:
                if(num_items(Items.Fertilizer) >= 0):
                    trade(Items.Fertilizer, get_world_size() * get_world_size())
					
                use_item(Items.Fertilizer)
                
            drone["set_property"]("update_graph_on_success", False)

            path = a_star(graph, distance_dict, drone_get_coords(), next_coords)

            if path != None:
                success = drone_follow_path(path)

            if not success:
                drone["set_property"]("update_graph_on_success", True)
                success = best_guess_strategy(drone, graph, game_board, distance_dict, check_is_treasure)

            if success:
                next_coords = measure()

    new_maze_plan = {
        "do_create_maze": do_create_maze,
        "execute_plan": execute_plan
    }

    return new_maze_plan
    
