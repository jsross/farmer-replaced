from __builtins__ import *
from __test_harness__ import *
from Utility import *
from farmer import *

def init_carrot_plot():
    till()

    if get_water() < 0.25:
        use_item(Items.Water)

    plant(Entities.Carrot)
    use_item(Items.Fertilizer)

def maintain_carrot_plot():
    if get_water() < 0.25:
        use_item(Items.Water)

    if(can_harvest()):
        harvest()
        
        plant(Entities.Carrot)
        use_item(Items.Fertilizer)

def init_carrot_farm(width, height, x_offset, y_offset):
    execute_scan_pass(width, height, init_carrot_plot, None, x_offset, y_offset)

    return 0

def maintain_carrot_farm(width, height, x_offset, y_offset):
    execute_scan_pass(width, height, maintain_carrot_plot, None, x_offset, y_offset)

    return 0

def create_carrot_farmer(width, height, x_offset, y_offset, goal):
    
    def init_farm():
        init_carrot_farm(width, height, x_offset, y_offset)

        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }

    def maintain_farm():
        maintain_carrot_farm(width, height, x_offset, y_offset)

        if num_items(Items.Carrot) > goal:
            return None

        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }
     
    return init_farm

