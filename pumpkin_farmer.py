from __builtins__ import *
from __test_harness__ import *
from Utility import *
from matrix import *
from farmer import *
from drone import *


def create_pumpkin_farmer(width, height, x_offset, y_offset, goal):

    can_harvest_matrix = create_matrix_with_default(width, height, False)

    def init_pumpkin_plot(x, y):
        till()
        
        maintain_plot_water()

        plant(Entities.Pumpkin)

        return 0
    
    def replant_pumpkin_plot(x, y):
        maintain_plot_water()

        plant(Entities.Pumpkin)

        can_harvest_matrix[x][y] = can_harvest()

        return 0
    
    def maintain_pumpkin_plot(x, y):
        maintain_plot_water()

        if get_entity_type() == None:
            plant(Entities.Pumpkin)

        can_harvest_matrix[x][y] = can_harvest()

        return 0

    def init_farm():
        execute_scan_pass(width, height, init_pumpkin_plot, x_offset, y_offset)
        
        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }
    
    def maintain_farm():
        coords = select_coords_from_matrix_with_value(can_harvest_matrix, False)

        if(len(coords)==0):
            go_to(x_offset, y_offset)
            harvest()
            
            execute_scan_pass(width, height, replant_pumpkin_plot, x_offset, y_offset)
        else:
            quick_print("Path: ", coords)
            execute_path_action(coords, maintain_pumpkin_plot, x_offset, y_offset)

        if num_items(Items.Pumpkin) > goal:
            return None

        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }

    return init_farm

def farm_pumpkins(goal):
    farm_size = get_world_size()
    execute_single_farmer(create_pumpkin_farmer(farm_size, farm_size, 0, 0, goal))

             