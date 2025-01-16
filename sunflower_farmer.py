from __builtins__ import *
from __test_harness__ import *
from Utility import *
from matrix import *
from drone import *
from farmer import *

def create_sunflower_farmer(width, height, x_offset, y_offset, goal):
    MAX_PRIORITY = 15
    NO_PRIORITY = 0
    MAX_GROW_TIME = 8.4

    plot_matrix = create_matrix_with_default(width, height, None)

    def init_farm():
        execute_scan_pass(width, height, _init_plot, x_offset, y_offset)

        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }
    
    def replant_farm():
        execute_scan_pass(width, height, _replant_plot, x_offset, y_offset)

        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }
        
    def maintain_farm():
        for priority in range(MAX_PRIORITY, 6, -1):
            ready_by = _harvest_priority(priority)

            if len(ready_by) > 0:
                break

        if num_items(Items.Power) > goal:
            return None
        
        if len(ready_by) > 0:
            min_ready = min(ready_by)
            delay = max((min_ready - get_time()), 0)

            quick_print("delay: ", delay)

            return {
                "status": 0,
                "next_pass": maintain_farm,
                "delay": delay
            }

        return {
            "status": 0,
            "next_pass": replant_farm,
            "delay": 0
        }

    def _create_plot():
        plot = {
            "entity_type": get_entity_type(),
            "priority": measure(),
        }

        if plot["entity_type"] != None:
            plot["ready_by"] = get_time() + calculate_adjusted_grow_time(MAX_GROW_TIME, get_water())

        return plot

    def _harvest_priority(priority):
        quick_print("handling priority: ", priority)
        ready_by_list = []
        priority_plot_coords = select_coords_with_properties(plot_matrix, { "priority" : priority })

        for coords in priority_plot_coords:
            x_index = coords[0]
            y_index = coords[1]

            go_to(x_index + x_offset, y_index + y_offset)
            plot = plot_matrix[x_index][y_index]
            
            if can_harvest():
                harvest()
                quick_print("harvest: ", (x_index, y_index), plot["priority"])
                plot_matrix[x_index][y_index] = None
            else:
                ready_by_list.append(plot["ready_by"])

        return ready_by_list
    
    def _init_plot(x, y):
        maintain_plot_water()

        till()
        plant(Entities.Sunflower)
        plot_matrix[x][y] = _create_plot()

        return 0

    def _replant_plot(x, y):
        maintain_plot_water()

        plant(Entities.Sunflower)
        plot_matrix[get_pos_x()][get_pos_y()] = _create_plot()

        return 0
    
    
    return init_farm

def farm_sunflowers(goal):
    farm_size = get_world_size()
    execute_single_farmer(create_sunflower_farmer(farm_size, farm_size, 0, 0, goal))