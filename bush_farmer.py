from __builtins__ import *
from __test_harness__ import *
from Utility import *
from farmer import *

def create_bush_farmer(width, height, x_offset, y_offset):
    
    def init_farm():
        go_to(x_offset, y_offset)

        return init_bush_farm(width, height, x_offset, y_offset)

    def maintain_farm():
        go_to(x_offset, y_offset)
        
        return maintain_bush_farm(width, height, x_offset, y_offset)
        
    new_farmer = {
        "init_farm": init_farm,
        "maintain_farm": maintain_farm
    }
     
    return new_farmer

def init_bush_farm(width, height, x_offset, y_offset):
    execute_scan_pass(width, height, init_bush_plot, None, x_offset, y_offset)

    return 0

def maintain_bush_farm(width, height, x_offset, y_offset):
    execute_scan_pass(width, height, maintain_bush_plot, None, x_offset, y_offset)

    return 0

def init_bush_plot():
    use_item(Items.Water)

    plant(Entities.Bush)

def maintain_bush_plot():
    if(can_harvest()):
        harvest()
        #use_item(Items.Fertilizer)
        use_item(Items.Water)
        plant(Entities.Bush)

    