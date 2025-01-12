from __builtins__ import *
from __test_harness__ import *
from Utility import *
from matrix import *
from drone import *
from maze_navigator import *

MAX_PRIORITY = 15
NO_PRIORITY = 0

def create_maze_farmer(goal):
    graph = create_graph()

    world_size = get_world_size()
    n_substance = world_size * num_unlocked(Unlocks.Mazes)
    chest_value = (world_size ** 2) * num_unlocked(Unlocks.Mazes)

    maze_state = {
        "total_pending": 0,
        "iteration": 0
    }

    def init_maze():
        maze_state["total_pending"] = 0
        maze_state["iteration"] = 0

        plant(Entities.Bush)
        use_item(Items.Weird_Substance, n_substance)
        
        return {
            "status": 0,
            "next_pass": search_for_treasure,
            "delay": 0
        }
    
    def search_for_treasure():
        maze_state["iteration"] += 1
        result = search_for_goal(check_is_treasure, graph)

        if result == False:
            print("Treasure not found: Abort!")
            
            return {
                "status": -1,
                "next_pass": None,
                "delay": 0
            }
        
        maze_state["total_pending"] += chest_value
        
        return {
            "status": 0,
            "next_pass": goto_next_treasure,
            "delay": 0
        }

    def goto_next_treasure():
        maze_state["iteration"] += 1
        success = False
        
        current_coords = (get_pos_x(), get_pos_y())
        next_coords = measure()

        if next_coords == None:
            harvest()

            return {
                "status": 0,
                "next_pass": init_maze,
                "delay": 0
            }
        
        use_item(Items.Weird_Substance, n_substance)

        if 100 *  random() // 1 > 30:
            path = get_path(graph, current_coords, next_coords, get_distance)
        
            if path != None:
                follow_path(path)

                success = get_entity_type() == Entities.Treasure
        else:
            quick_print("Pathing Randomly skipped")
            
        if not success:
            success = seak_coords(next_coords, graph)

        if get_entity_type() != Entities.Treasure:
            return {
                "status": -1,
                "next_pass": None,
                "delay": 0
            }
        
        maze_state["total_pending"] += chest_value

        if num_items(Items.Gold) + maze_state["total_pending"] >= goal:
            harvest()
            return None
        
        return {
            "status": 0,
            "next_pass": goto_next_treasure,
            "delay": 0
        }

    return init_maze

def check_is_treasure():
    return get_entity_type() == Entities.Treasure