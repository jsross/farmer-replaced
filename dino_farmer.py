from __builtins__ import *
from __test_harness__ import *
from Utility import *
from matrix import *
from drone import *

def create_dino_farmer():
    state = {
        "path_history": []
    }

    def init_farm():
        change_hat(Hats.Dinosaur_Hat)
        state["path_history"] = []
        state["path_history"].append((0,0))

        next_coords = measure()

        if not go_to(next_coords[0], next_coords[1]):
            return -1

        state["path_history"].append(next_coords)

        return 0
    
    def maintain_farm():
        next_coords = measure()

        if next_coords == None:
            change_hat(Hats.Straw_Hat)
            return -1

        if not go_to(next_coords[0], next_coords[1]):
            change_hat(Hats.Straw_Hat)
            return -1
        
        state["path_history"].append(next_coords)

        return 0

    new_farmer = {
        "init_farm": init_farm,
        "maintain_farm": maintain_farm
    }

    return new_farmer
