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
		success = do_wall_follow(drone, check_is_treasure)
        next_coords = measure()
        
        if success == False:
            print("Abort")
            
            return

        for _ in range(iterations):

            while get_entity_type() == Entities.Treasure:
                if(num_items(Items.Fertilizer) >= 0):
					trade(Items.Fertilizer, get_world_size() * get_world_size())
					
                use_item(Items.Fertilizer)
                
            drone["set_property"]("update_graph_on_success", False)
            success = drone["go_to"](next_coords, a_star)
            
            if not success:
                print("Searching")
                drone["set_property"]("update_graph_on_success", True)
                success = drone["search"](check_is_treasure, do_wall_follow)

				if success:
					next_coords = measure()

    new_maze_plan = {
        "do_create_maze": do_create_maze,
        "execute_plan": execute_plan
    }

    return new_maze_plan
    
