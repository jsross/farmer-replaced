from __builtins__ import *
from __test_harness__ import *
from Utility import *

def init_grass_plot():
    harvest()

def maintain_grass_plot():
    harvest()

def create_grass_farmer(drone, width, height, x_offset, y_offset):
    go_to = drone["go_to"]

    def init_farm():
        clear()

        for x_index in range(width):
            for y_index in range(height):
                go_to(x_index + x_offset, y_index + y_offset)

                harvest()
        
        return 0

    def maintain_farm():
        for x_index in range(width):
            for y_index in range(height):
                go_to(x_index + x_offset, y_index + y_offset)

                harvest()

        return 0

    new_farmer = {
        "init_farm": init_farm,
        "maintain_farm": maintain_farm
    }

    return new_farmer