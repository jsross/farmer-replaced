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

        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }
    
    def maintain_farm():
        next_coords = measure()

        if next_coords == None:
            change_hat(Hats.Straw_Hat)

            return {
                "status": -1,
                "next_pass": None,
                "delay": 0
            }

        if not go_to(next_coords[0], next_coords[1]):
            change_hat(Hats.Straw_Hat)

            return {
                "status": -1,
                "next_pass": None,
                "delay": 0
            }
        
        state["path_history"].append(next_coords)

        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }

    return init_farm
