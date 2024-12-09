from __builtins__ import *
from __test_harness__ import *
from Utility import *
from drone import *
from farm import *

def create_sunflower_farmer(farm, drone, x_offset, y_offset):
    go_to = drone["go_to"]
    select_coords = farm["select_coords"]
    find_first = farm["find_first"]
    get_plot = farm["get_plot"]
    get_max_value = farm["get_max_value"]
    
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

        
        
        return 0
    
    def replant_farm():
        item_counts = {
            Items.Pumpkin_Seed: plot_count,
            Items.Fertilizer: plot_count
        }

        do_trade(item_counts)

        for x_index in range(width):
            for y_index in range(height):
                go_to(x_index + x_offset, y_index + y_offset)
    
                use_item(Items.Fertilizer)
                use_item(Items.Water_Tank)
                plant(Entities.Sunflower)

                plot = get_plot(x_index, y_index)

                plot["entity_type"] = get_entity_type()
                plot["priority"] = measure()
                plot["can_harvest"] = can_harvest()
                plot["timestamp"] = get_time()

        new_farmer["maintain_farm"] = maintain_farm
        
        return 0
        
    def maintain_farm():
        max_timestamp = get_max_value("timestamp")

        if max_timestamp + 6 > get_time():
            return max_timestamp + 6
        
        #All Ready

        for priority in range(MAX_PRIORITY, 1, -1):
            priority_plot_coords = select_coords({ "priority" : priority })

            for coords in priority_plot_coords:
                x_index = coords[0]
                y_index = coords[1]

                go_to(x_index, y_index)
                plot = get_plot(x_index, y_index)

                harvest()

                plot["entity_type"] = get_entity_type()
                plot["priority"] = measure()
                plot["can_harvest"] = can_harvest()
                plot["timestamp"] = get_time()


        new_farmer["maintain_farm"] = replant_farm

        return 0

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
