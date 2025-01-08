from __builtins__ import *
from __test_harness__ import *
from Utility import *
from matrix import *
from drone import *
from maze_navigator import *

def create_maze_farmer(goal):
    graph = create_graph(get_distance)

    world_size = get_world_size()
    n_substance = world_size * num_unlocked(Unlocks.Mazes)
    chest_value = (world_size ** 2) * num_unlocked(Unlocks.Mazes)

    get_path = graph["get_path"]
    remove_edge = graph["remove_edge"]

    maze_state = {
        "total_pending": 0,
        "iteration": 0
    }

    def init_maze():
        maze_state["total_pending"] = 0
        maze_state["iteration"] = 0

        plant(Entities.Bush)
        use_item(Items.Weird_Substance, n_substance)

        for index in range(world_size):
            south_coords = (index, 0)
            east_coords = (0, index)

            south_neighbor = get_neighbor(south_coords[0], south_coords[1], South)
            remove_edge(set([south_coords, south_neighbor]))

            east_neighbor = get_neighbor(east_coords[0], east_coords[1], East)
            remove_edge(set([east_coords, east_neighbor]))
        
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
            "next_pass": seak_next_treasure,
            "delay": 0
        }


    def seak_next_treasure():
        maze_state["iteration"] += 1
        success = False

        next_coords = measure()

        if next_coords == None:
            harvest()

            return {
                "status": 0,
                "next_pass": init_maze,
                "delay": 0
            }
        
        use_item(Items.Weird_Substance, n_substance)

        if 10 *  random() // 1 > 3:
            path = get_path((get_pos_x(), get_pos_y()), next_coords)
        
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
            "next_pass": seak_next_treasure,
            "delay": 0
        }

    return init_maze

def check_is_treasure():
    return get_entity_type() == Entities.Treasure