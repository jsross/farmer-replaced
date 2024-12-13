from __builtins__ import *
from __test_harness__ import *
from Utility import *
from farmer import *
from drone import *
from farm import *

def init_pumpkin_plot():
    till()
    
    if get_water() < 0.25:
        use_item(Items.Water)

    plant(Entities.Pumpkin)

def replant_pumpkin_plot():
    if get_water() < 0.25:
        use_item(Items.Water)

    plant(Entities.Pumpkin)

def maintain_pumpkin_plot():
    if get_water() < 0.25:
        use_item(Items.Water)
    
    plant(Entities.Pumpkin)

    return can_harvest()

def init_pumpkin_farm(width, height, x_offset, y_offset):
    execute_scan_pass(width, height, init_pumpkin_plot, None, x_offset, y_offset)

    return 0

def maintain_pumpkin_farm(matrix, width, height, x_offset, y_offset):
    coords = select_coords_from_matrix_with_value(matrix, False)

    if(len(coords)==0):
        go_to(x_offset, y_offset)
        harvest()
        
        execute_scan_pass(width, height, replant_pumpkin_plot, matrix, x_offset, y_offset)

    execute_path_action(coords, maintain_pumpkin_plot, x_offset, y_offset, matrix)

    return 0

def create_pumpkin_farmer(width, height, x_offset, y_offset):

    can_harvest_matrix = create_matrix_with_default(width, height, False) 

    def init_farm():
        return init_pumpkin_farm(width, height, x_offset, y_offset)
    
    def maintain_farm():
        return maintain_pumpkin_farm(can_harvest_matrix, width, height, x_offset, y_offset)

    new_farmer = {
        "init_farm": init_farm,
        "maintain_farm": maintain_farm
    }

    return new_farmer

             