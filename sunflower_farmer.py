from __builtins__ import *
from __test_harness__ import *
from Utility import *
from matrix import *
from drone import *

def create_sunflower_farmer(width, height, x_offset, y_offset, goal):
    GROW_TIME = 4
    plot_count = width * height

    default_plot = {
        "entity_type": None,
        "priority": 0,
        "can_harvest": False,
        "timestamp": 0
    }

    plot_matrix = create_matrix_with_default_object(width, height, default_plot)

    def init_farm():
        for x_index in range(width):
            for y_index in range(height):
                go_to(x_index + x_offset, y_index + y_offset)

                if get_water() < 0.25:
                    use_item(Items.Water)

                till()
    
                plant(Entities.Sunflower)
                use_item(Items.Fertilizer)

                plot = plot_matrix[x_index][y_index]

                plot["entity_type"] = get_entity_type()
                plot["priority"] = measure()
                plot["can_harvest"] = can_harvest()
                plot["timestamp"] = get_time()

        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": GROW_TIME
        }
    
    def replant_farm():
        for x_index in range(width):
            for y_index in range(height):
                go_to(x_index + x_offset, y_index + y_offset)

                if get_water() < 0.25:
                    use_item(Items.Water)
    
                plant(Entities.Sunflower)
                use_item(Items.Fertilizer)

                plot = plot_matrix[x_index][y_index]

                plot["entity_type"] = get_entity_type()
                plot["priority"] = measure()
                plot["can_harvest"] = can_harvest()
                plot["timestamp"] = get_time()

        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": GROW_TIME
        }
        
    def maintain_farm():
        for priority in range(MAX_PRIORITY, 1, -1):
            priority_plot_coords = select_coords_with_properties(plot_matrix, { "priority" : priority })

            for coords in priority_plot_coords:
                x_index = coords[0]
                y_index = coords[1]

                go_to(x_index + x_offset, y_index + y_offset)

                if get_water() < 0.25:
                    use_item(Items.Water)

                harvest()

                plot = plot_matrix[x_index][y_index]
                plot["entity_type"] = get_entity_type()
                plot["priority"] = measure()
                plot["can_harvest"] = can_harvest()
                plot["timestamp"] = get_time()

        if num_items(Items.Power) > goal:
            return None

        return {
            "status": 0,
            "next_pass": replant_farm,
            "delay": 0
        }

    return init_farm
