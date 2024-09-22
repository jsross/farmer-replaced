from wall_follow_strategy import *
from a_star import *

def create_maze_plan(drone, graph):

    def check_is_treasure():
        return get_entity_type() == Entities.Treasure
    
    def do_create_maze():
        clear()
        
        if get_ground_type() != Grounds.Turf:
            till()
        
        plant(Entities.Bush)
        
        while not can_harvest():
            pass
            
        while get_entity_type() == Entities.Bush:
            if num_items(Items.Fertilizer) == 0:
                trade(Items.Fertilizer, 100)
            use_item(Items.Fertilizer)

    def execute_plan(iterations):
        
        do_wall_follow(drone, check_is_treasure)

        for _ in range(iterations):
            next_coords = measure()

            while get_entity_type() == Entities.Treasure:
                use_item(Items.Fertilizer)

            treasure_found = False
                    
            current_path = a_star(graph, drone["get_coords"](), next_coords)
            
            if current_path != None:
                treasure_found = drone["follow_path"](current_path)
            
            if not treasure_found:
                do_wall_follow(drone, check_is_treasure)

    new_maze_plan = {
        "do_create_maze": do_create_maze,
        "execute_plan": execute_plan
    }

    return new_maze_plan
    
