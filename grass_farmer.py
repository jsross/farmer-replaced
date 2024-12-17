from __builtins__ import *
from __test_harness__ import *
from Utility import *
from farmer import *

def handle_grass_plot():
    harvest()

def handle_grass_farm(width, height):
    execute_scan_pass(width, height, handle_grass_plot, None)

    return 0

def create_grass_farmer(width, height):
    def handle_farm():
        handle_grass_farm(width, height)
        
        return 0

    new_farmer = {
        "init_farm": handle_farm,
        "maintain_farm": handle_farm
    }

    return new_farmer