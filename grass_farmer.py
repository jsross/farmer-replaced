from __builtins__ import *
from __test_harness__ import *
from Utility import *
from farmer import *

def handle_grass_plot():
    harvest()

def handle_grass_farm(width, height, x_offset, y_offset):
    execute_scan_pass(width, height, handle_grass_plot, None, x_offset, y_offset)

    return 0

def create_grass_farmer(width, height, x_offset, y_offset):
    def handle_farm():
        return handle_grass_farm(width, height, x_offset, y_offset)

    new_farmer = {
        "init_farm": handle_farm,
        "maintain_farm": handle_farm
    }

    return new_farmer