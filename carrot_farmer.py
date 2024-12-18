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

def create_carrot_farmer(width, height, x_offset, y_offset):
    def init_farm():
        return init_carrot_farm(width, height, x_offset, y_offset)

    def maintain_farm():
        return maintain_carrot_farm(width, height, x_offset, y_offset)
        
    new_farmer = {
        "init_farm": init_farm,
        "maintain_farm": maintain_farm
    }
     
    return new_farmer

