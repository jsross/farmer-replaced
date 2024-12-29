from __builtins__ import *
from __test_harness__ import *
from Utility import *
from farmer import *

def create_bush_farmer(width, height, x_offset, y_offset, goal):
    
    def init_farm():
        go_to(x_offset, y_offset)

        init_bush_farm(width, height, x_offset, y_offset)

        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }

    def maintain_farm():
        go_to(x_offset, y_offset)
        maintain_bush_farm(width, height, x_offset, y_offset)

        if num_items(Items.Wood) > goal:
            return None
        
        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }
     
    return init_farm

def init_bush_farm(width, height, x_offset, y_offset):
    execute_scan_pass(width, height, init_bush_plot, None, x_offset, y_offset)

    return 0

def maintain_bush_farm(width, height, x_offset, y_offset):
    execute_scan_pass(width, height, maintain_bush_plot, None, x_offset, y_offset)

    return 0

def init_bush_plot():
    if get_water() < 0.25:
        use_item(Items.Water)

    plant(Entities.Bush)
    use_item(Items.Fertilizer)

def maintain_bush_plot():
    if get_water() < 0.25:
        use_item(Items.Water)

    if(can_harvest()):
        harvest()

        plant(Entities.Bush)
        use_item(Items.Fertilizer)

    