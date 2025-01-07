from __builtins__ import *
from __test_harness__ import *
from Utility import *
from matrix import *
from drone import *
from farmer import *

def create_sunflower_farmer(width, height, x_offset, y_offset, goal):
    MAX_GROW_TIME = 8.4
    plot_count = width * height

    default_plot = {
        "entity_type": None,
        "priority": 0,
        "timestamp": 0
    }

    plot_matrix = create_matrix_with_default_object(width, height, default_plot)

    def init_farm():
        print("Init!!!!")

        for x_index in range(width):
            for y_index in range(height):
                go_to(x_index + x_offset, y_index + y_offset)
                water_level = get_water()
                if water_level < 0.25:
                    use_item(Items.Water)
                    water_level = get_water()

                till()
    
                plant(Entities.Sunflower)
                #use_item(Items.Fertilizer)

                plot = plot_matrix[x_index][y_index]

                plot["entity_type"] = get_entity_type()
                plot["priority"] = measure()
                plot["ready_by"] = get_time() + calculate_adjusted_grow_time(MAX_GROW_TIME, water_level)

        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }
    
    def replant_farm():
        for x_index in range(width):
            for y_index in range(height):
                go_to(x_index + x_offset, y_index + y_offset)
                water_level = get_water()

                if water_level < 0.25:
                    use_item(Items.Water)
                    water_level = get_water()
    
                plant(Entities.Sunflower)
                #use_item(Items.Fertilizer)

                plot = plot_matrix[x_index][y_index]

                plot["entity_type"] = get_entity_type()
                plot["priority"] = measure()
                plot["ready_by"] = get_time() + calculate_adjusted_grow_time(MAX_GROW_TIME, water_level)

        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }
    
    def harvest_priority(priority):
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

                plot["entity_type"] = None
                plot["priority"] = None
                plot["ready_by"] = None
            else:
                ready_by_list.append(plot["ready_by"])

        return ready_by_list
        
    def maintain_farm():
        for priority in range(MAX_PRIORITY, 6, -1):
            ready_by = harvest_priority(priority)

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

    return init_farm
