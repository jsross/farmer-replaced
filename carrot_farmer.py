from __builtins__ import *
from __test_harness__ import *
from Utility import *

def create_carrot_farmer(drone, width, height, x_offset, y_offset):
    go_to = drone["go_to"]

    def init_farm():
        for x_index in range(width):
            for y_index in range(height):
                go_to(x_index + x_offset, y_index + y_offset)

                init_carrot_plot()

    def maintain_farm():
        for x_index in range(width):
            for y_index in range(height):
                go_to(x_index + x_offset, y_index + y_offset)

                maintain_carrot_plot()
        
    new_farmer = {
        "init_farm": init_farm,
        "maintain_farm": maintain_farm
    }
     
    return new_farmer

def init_carrot_plot():
    till()

    plant(Entities.Carrots)

def maintain_carrot_plot():
    if(can_harvest()):
        harvest()

    plant(Entities.Carrots)