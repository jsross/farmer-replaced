from __builtins__ import *
from __test_harness__ import *
from Utility import *
from matrix import *
from drone import *

def create_maze_farmer(goal):
    graph = create_graph(get_distance)
    navigator = create_maze_navigator(graph)

    get_path = graph["get_path"]
    remove_edge = graph["remove_edge"]

    search = navigator["search"]
    seak = navigator["seak"]

    farm_state = {
        "iteration": 0 
    }

    def init_farm():
        world_size = get_world_size()
        plant(Entities.Bush)
    
        use_item(Items.Weird_Substance, world_size)

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
            "delay": 2
        }
    
    def search_for_treasure():
        farm_state["iteration"] += 1
        result = search(check_is_treasure)

        if result == False:
            print("Treasure not found: Abort!")
            
            return {
                "status": -1,
                "next_pass": None,
                "delay": 0
            }
        
        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }
        
    
    def maintain_farm():
        farm_state["iteration"] += 1
        success = False

        next_coords = measure()

        if next_coords == None:
            harvest()
            return {
                "status": -1,
                "next_pass": None,
                "delay": 0
            }
        
        use_item(Items.Weird_Substance, get_world_size())
        
        path = get_path((get_pos_x(), get_pos_y()), next_coords)
        
        if path != None:
            follow_path(path)

            success = get_entity_type() == Entities.Treasure

        if not success:
            success = seak(next_coords)

        if get_entity_type() != Entities.Treasure:
            return {
                "status": -1,
                "next_pass": None,
                "delay": 0
            }
        
        if farm_state["iteration"] >= goal:
            harvest()
            return None
        
        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }

    return init_farm

def check_is_treasure():
    return get_entity_type() == Entities.Treasure