from __builtins__ import *
from __test_harness__ import *
from Utility import *
from farmer import *

def handle_grass_plot():
    harvest()

def handle_grass_farm(width, height, x_offset, y_offset):
    execute_scan_pass(width, height, handle_grass_plot, None, x_offset, y_offset)

    return 0

def create_grass_farmer(width, height, x_offset, y_offset, goal):

    def handle_farm():
        
        handle_grass_farm(width, height, x_offset, y_offset)

        if num_items(Items.Hay) > goal:
            return None

        return {
            "status": 0,
            "next_pass": handle_farm,
            "delay": 0
        }

    return handle_farm