from __builtins__ import *
from __test_harness__ import *
from Utility import *
from matrix import *
from farmer import *
from drone import *

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

def create_pumpkin_farmer(width, height, x_offset, y_offset, goal):

    can_harvest_matrix = create_matrix_with_default(width, height, False) 

    def init_farm():
        init_pumpkin_farm(width, height, x_offset, y_offset)

        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }
    
    def maintain_farm():
        maintain_pumpkin_farm(can_harvest_matrix, width, height, x_offset, y_offset)

        if num_items(Items.Pumpkin) > goal:
            return None

        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }

    return init_farm

             