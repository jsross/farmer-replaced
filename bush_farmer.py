from __builtins__ import *
from __test_harness__ import *
from Utility import *
from farmer import *

def create_bush_farmer(width, height, x_offset, y_offset, goal):
    
    def init_farm():
        go_to(x_offset, y_offset)

        execute_scan_pass(width, height, init_bush_plot, x_offset, y_offset)

        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }

    def maintain_farm():
        go_to(x_offset, y_offset)
        execute_scan_pass(width, height, maintain_bush_plot, x_offset, y_offset)

        if num_items(Items.Wood) > goal:
            return None
        
        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }
     
    return init_farm

def init_bush_plot(_x, _y):
    maintain_plot_water()

    if not plant(Entities.Bush):
        return -1

    if num_unlocked(Items.Fertilizer) > 0:
        use_item(Items.Fertilizer)

    return 0

def maintain_bush_plot(_x, _y):
    maintain_plot_water()

    if(can_harvest()):
        harvest()

        if not plant(Entities.Bush):
            return -1
        if num_unlocked(Items.Fertilizer) > 0:
            use_item(Items.Fertilizer)
        
    return 0

def farm_bush(goal):
    farm_size = get_world_size()
    execute_single_farmer(create_bush_farmer(farm_size, farm_size, 0, 0, goal))

    