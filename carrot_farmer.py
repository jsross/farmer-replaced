from __builtins__ import *
from __test_harness__ import *
from Utility import *
from farmer import *

def init_carrot_plot(_x, _y):
    till()

    maintain_plot_water()

    if not plant(Entities.Carrot):
        return -1

    if num_unlocked(Items.Fertilizer) > 0:
        use_item(Items.Fertilizer)

    return 0

def maintain_carrot_plot(_y, _x):
    maintain_plot_water()

    if(can_harvest()):
        harvest()
        
        if not plant(Entities.Carrot):
            return -1
        
        if num_unlocked(Items.Fertilizer) > 0:
            use_item(Items.Fertilizer)

    return 0

def create_carrot_farmer(width, height, x_offset, y_offset, goal):
    
    def init_farm():
        execute_scan_pass(width, height, init_carrot_plot, x_offset, y_offset)

        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }

    def maintain_farm():
        execute_scan_pass(width, height, maintain_carrot_plot, x_offset, y_offset)

        if num_items(Items.Carrot) > goal:
            return None

        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }
     
    return init_farm

def farm_carrots(goal):
    farm_size = get_world_size()
    execute_single_farmer(create_carrot_farmer(farm_size, farm_size, 0, 0, goal))