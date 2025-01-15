from __builtins__ import *
from __test_harness__ import *
from Utility import *
from matrix import *
from drone import *

def create_dino_farmer(goal):
    state = {
        "path_history": [],
        "iteration": 0
    }

    def add_to_path_history(coords):
        path_history = state["path_history"]
        iteration = state["iteration"]

        path_history.insert(0, coords)

        if len(path_history) > iteration + 1:
            path_history.pop(-1)



    def init_farm():
        change_hat(Hats.Dinosaur_Hat)
        state["path_history"] = []
        state["iteration"] = 0

        add_to_path_history((get_pos_x(), get_pos_y()))

        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }
    
    def maintain_farm():
        state["iteration"] += 1
        path_history = state["path_history"]

        dest_coords = measure()

        if dest_coords == None:
            change_hat(Hats.Straw_Hat)

            return {
                "status": -1,
                "next_pass": None,
                "delay": 0
            }
        
        dest_x = dest_coords[0]
        dest_y = dest_coords[1]

        success = False

        while True:
            current_x = get_pos_x()
            current_y = get_pos_y()

            quick_print(path_history)

            if current_x == dest_x and current_y == dest_y:
                success = True
                break

            neighbors = get_neighbor_map(current_x, current_y)

            min_distance = 1000000
            next_direction = None

            for direction in neighbors:
                neighbor_coords = neighbors[direction]

                if neighbor_coords in path_history:
                    continue

                neighbor_distance = get_distance(neighbor_coords, dest_coords)

                if neighbor_distance < min_distance:
                    min_distance = neighbor_distance
                    next_direction = direction

            if next_direction == None:
                break

            if not move(next_direction):
                break

            add_to_path_history((get_pos_x(), get_pos_y()))

        if not success:
            change_hat(Hats.Straw_Hat)

            if num_items(Items.Bone) > goal:
                return None
            else:
                return {
                    "status": 0,
                    "next_pass": init_farm,
                    "delay": 0
                }

        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }

    return init_farm

def farm_dinos(goal):
    execute_single_farmer(create_dino_farmer(goal))
