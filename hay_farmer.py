from __builtins__ import *
from __test_harness__ import *
from Utility import *
from farmer import *

def handle_grass_plot(_x, _y):
    if not harvest():
        return -1
    
    return 0

def create_hay_farmer(width, height, x_offset, y_offset, goal):

    def handle_farm():
        execute_scan_pass(width, height, handle_grass_plot, x_offset, y_offset)

        if num_items(Items.Hay) > goal:
            return None

        return {
            "status": 0,
            "next_pass": handle_farm,
            "delay": 0
        }

    return handle_farm

def farm_hay(goal):
    farm_size = get_world_size()
    execute_single_farmer(create_hay_farmer(farm_size, farm_size, 0, 0, goal))