from wall_follow_strategy import *
from a_star import *

def create_maze_plan(drone, graph):

    def check_is_treasure():
        return get_entity_type() == Entities.Treasure
    
    def do_create_maze():
    
        while not can_harvest():
            pass
            
        while get_entity_type() == Entities.Bush:
            if num_items(Items.Fertilizer) == 0:
                trade(Items.Fertilizer, 100)
            use_item(Items.Fertilizer)

    def execute_plan(iterations):
        drone["set_property"]("update_graph_on_success", False)
		succss = do_wall_follow(drone, check_is_treasure)
        next_coords = measure()
        
        if succss == False:
            print("Abort")
            
            return

        for _ in range(iterations):

            while get_entity_type() == Entities.Treasure:
                if(num_items(Items.Fertilizer) >= 0):
					trade(Items.Fertilizer, get_world_size() * get_world_size())
					
                use_item(Items.Fertilizer)

            treasure_found = False
            
            current_path = a_star(graph, drone["get_coords"](), next_coords)
            
            if current_path != None and len(current_path) > 0:
                print("Following Path")
                drone["set_property"]("update_graph_on_success", False)
                treasure_found = drone["follow_path"](current_path)
            else:
                print("Path Not Found!")
            
            if not treasure_found:
                print("Searching")
				if do_wall_follow(drone, check_is_treasure):
					drone["set_property"]("update_graph_on_success", True)
					next_coords = measure()

    new_maze_plan = {
        "do_create_maze": do_create_maze,
        "execute_plan": execute_plan
    }

    return new_maze_plan
    
