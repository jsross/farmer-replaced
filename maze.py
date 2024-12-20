from navigator import *

def create_maze_plan():
    navigator = create_navigator()

    search = navigator["search"]
    seak =  navigator["seak"]
    get_path = navigator["get_path"]

    def check_is_treasure():
        return get_entity_type() == Entities.Treasure
    
    def do_create_maze():
        clear()
        plant(Entities.Bush)
    
        while not can_harvest():
            pass
            
        while get_entity_type() == Entities.Bush:
            use_item(Items.Weird_Substance, get_world_size())

    def execute_plan(iterations):
        success = search(check_is_treasure)
        
        if success == False:
            print("Abort")
            
            return

        for _ in range(1, iterations):
            next_coords = measure()
            
            use_item(Items.Weird_Substance, get_world_size())
            
            #path = get_path((get_pos_x(), get_pos_y()), next_coords)
            
            #if path != None:
            #    follow_result = follow_path(path)
                
            #    if follow_result:
            #        continue

            success = seak(next_coords)

            if not success:
                print("Failure")
           
    new_maze_plan = {
        "do_create_maze": do_create_maze,
        "execute_plan": execute_plan
    }

    return new_maze_plan