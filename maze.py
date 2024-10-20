from a_star import *
from navigator import *

def create_maze_plan(drone, graph, game_board):
    navigator = create_navigator(drone, graph, game_board)

    search = navigator["search"]
    seak =  navigator["seak"]

    get_coords = drone["get_coords"]
    follow_path = drone["follow_path"]

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
        success = search(check_is_treasure)
        
        if success == False:
            print("Abort")
            
            return
        
        next_coords = measure()

        for _ in range(iterations):
            success = False

            while get_entity_type() == Entities.Treasure:
                if(num_items(Items.Fertilizer) >= 0):
                    trade(Items.Fertilizer, get_world_size() * get_world_size())
					
                use_item(Items.Fertilizer)

            success = seak(next_coords)

            if success:
                next_coords = measure()
            else:
                break

    new_maze_plan = {
        "do_create_maze": do_create_maze,
        "execute_plan": execute_plan
    }

    return new_maze_plan