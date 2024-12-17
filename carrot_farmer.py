from __builtins__ import *
from __test_harness__ import *
from Utility import *
from farmer import *

def init_carrot_plot():
    till()
    use_item(Items.Fertilizer)
    use_item(Items.Water)
    plant(Entities.Carrot)

def maintain_carrot_plot():
    if(can_harvest()):
        harvest()
        use_item(Items.Fertilizer)
        use_item(Items.Water)
        plant(Entities.Carrot)

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

