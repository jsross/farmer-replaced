from __builtins__ import *
from __test_harness__ import *
from Utility import *
from drone import *
from farm import *

def create_sunflower_farmer(farm, drone, x_offset, y_offset):
    go_to = drone["go_to"]
    select_coords = farm["select_coords"]
    get_plot = farm["get_plot"]
    
    width = farm["width"]
    height = farm["height"]
    plot_count = width * height

    def init_farm():
        clear()
        
        item_counts = {
            Items.Pumpkin_Seed: plot_count,
            Items.Fertilizer: plot_count
        }

        do_trade(item_counts)

        for x_index in range(width):
            for y_index in range(height):
                go_to(x_index + x_offset, y_index + y_offset)
                
                till()
    
                use_item(Items.Fertilizer)
                use_item(Items.Water_Tank)
                plant(Entities.Sunflower)

                plot = get_plot(x_index, y_index)

                plot["entity_type"] = get_entity_type()
                plot["priority"] = measure()
                plot["can_harvest"] = can_harvest()
                plot["timestamp"] = get_time()
        
    def maintain_farm():
        not_planted_coords = select_coords({ "entity_type" : None })

        if len(not_planted_coords) == plot_count:
            for coords in not_planted_coords:
                x_index = coords[0]
                y_index = coords[1]

                go_to(x_index + x_offset, y_index + y_offset)
                plot = get_plot(x_index, y_index)

                use_item(Items.Fertilizer)
                use_item(Items.Water_Tank)
                plant(Entities.Sunflower)

                plot["entity_type"] = get_entity_type()
                plot["priority"] = measure()
                plot["can_harvest"] = can_harvest()
                plot["timestamp"] = get_time()

        else:
            for priority in range(MAX_PRIORITY, 1, -1):
                priority_plot_coords = select_coords({ "priority" : priority })
                not_ready_count = 0

                for coords in priority_plot_coords:
                    x_index = coords[0]
                    y_index = coords[1]

                    plot = get_plot(x_index, y_index)

                    if plot["can_harvest"] == False and get_time() - plot["timestamp"] < 6:
                        not_ready_count += 1

                        continue
                    
                    go_to(x_index, y_index)

                    harvest()

                    plot["entity_type"] = get_entity_type()
                    plot["priority"] = measure()
                    plot["can_harvest"] = can_harvest()
                    plot["timestamp"] = get_time()

                if not_ready_count > 0:
                    break

    new_farmer = {
        "init_farm": init_farm,
        "maintain_farm": maintain_farm
    }

    return new_farmer

def plant_sunflower_plot(plot):
    use_item(Items.Fertilizer)
    use_item(Items.Water_Tank)
    plant(Entities.Sunflower)

    merge(plot, do_scan())

def harvest_sunflower_plot(plot):
    harvest()
    merge(plot, do_scan())
