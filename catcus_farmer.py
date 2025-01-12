from __builtins__ import *
from __test_harness__ import *
from Utility import *
from matrix import *
from farmer import *

def create_cactus_farmer(width, height, x_offset, y_offset, goal):
    size_matrix = create_matrix_with_default(width, height, 0)
    harvest_matrix = create_matrix_with_default(width, height, False)

    farm_stats = {
        "harvest_count": 0
    }

    def init_cactus_plot():
        x = get_pos_x()
        y = get_pos_y()

        till()

        if get_water() < 0.25:
            use_item(Items.Water)
            
        plant(Entities.Cactus)
        
        size_matrix[x][y] = measure()

        if can_harvest() and not harvest_matrix[x][y]:
            harvest_matrix[x][y] = True
            farm_stats["harvest_count"] += 1

    def replant_catcus_plot():
        x = get_pos_x()
        y = get_pos_y()

        if get_water() < 0.25:
            use_item(Items.Water)
            
        plant(Entities.Cactus)
        
        size_matrix[x][y] = measure()

        if can_harvest() and not harvest_matrix[x][y]:
            harvest_matrix[x][y] = True
            farm_stats["harvest_count"] += 1

    def init_farm():
        execute_scan_pass(width, height, init_cactus_plot, x_offset, y_offset)

        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }

    def maintain_farm():
        quick_print(size_matrix)

        # Test if sorted
        sorted = True
        
        x_length = len(size_matrix)

        for x_index in range(x_length):
            y_length = len(size_matrix[x_index])

            for y_index in range(y_length):
                current_value = size_matrix[x_index][y_index]

                if y_index + 1 < y_length and current_value > size_matrix[x_index][y_index + 1]:
                    sorted = False
                    break

                if x_index + 1 < x_length and current_value > size_matrix[x_index + 1][y_index]:
                    sorted = False
                    break

        print("Sorted: ", sorted)

        if(sorted):
            go_to(0,0)
            harvest()
            execute_scan_pass(width, height, replant_catcus_plot, x_offset, y_offset)
        else:
            execute_scan_pass(width, height, maintain_cactus_plot, x_offset, y_offset)

        if num_items(Items.Cactus) > goal:
            return None

        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }
    
    def maintain_cactus_plot():
        x = get_pos_x()
        y = get_pos_y()

        if get_water() < 0.25:
            use_item(Items.Water)

        if can_harvest() and not harvest_matrix[x][y]:
            harvest_matrix[x][y] = True
            farm_stats["harvest_count"] += 1
        
        while True:
            swap_happened = False

            north_coords =  get_neighbor(x, y, North)
            east_coords = get_neighbor(x, y, East)
            west_coords = get_neighbor(x, y, West)
            south_coords = get_neighbor(x, y, South)

            if north_coords != None and size_matrix[x][y] > size_matrix[north_coords[0]][north_coords[1]]:
                swap(North)
                swap_entries(size_matrix, (x,y), north_coords)
                swap_entries(harvest_matrix, (x,y), north_coords)
                swap_happened = True

            if east_coords != None and size_matrix[x][y] > size_matrix[east_coords[0]][east_coords[1]]:
                swap(East)
                swap_entries(size_matrix, (x,y), east_coords)
                swap_entries(harvest_matrix, (x,y), east_coords)
                swap_happened = True
            
            if west_coords != None and size_matrix[west_coords[0]][west_coords[1]] > size_matrix[x][y]:
                swap(West)
                swap_entries(size_matrix, (x,y), west_coords)
                swap_entries(harvest_matrix, (x,y), west_coords)
                swap_happened = True

            if south_coords != None and size_matrix[south_coords[0]][south_coords[1]] > size_matrix[x][y]:
                swap(South)
                swap_entries(size_matrix, (x,y), south_coords)
                swap_entries(harvest_matrix, (x,y), south_coords)
                swap_happened = True

            if not swap_happened:
                break
            
    return init_farm

