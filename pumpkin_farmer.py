from __builtins__ import *
from __test_harness__ import *
from Utility import *
from drone import *

def create_pumpkin_farmer(farm, drone, x_offset, y_offset):
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
                go_to(x_offset + x_index, y_offset + y_index)
                
                till()
    
                use_item(Items.Fertilizer)
                use_item(Items.Water_Tank)
                plant(Entities.Pumpkin)

                plot = get_plot(x_index, y_index)
                plot["can_harvest"] = can_harvest()
                plot["timestamp"] = get_time()
        
        return 0
    
    def maintain_farm():
        not_ready_coords = select_coords({"can_harvest" : False })
        not_ready_count = len(not_ready_coords)

        if not_ready_count > 0:
            item_counts = {
                Items.Pumpkin_Seed: not_ready_count,
                Items.Fertilizer: not_ready_count
            }
            
            do_trade(item_counts)

            for coords in not_ready_coords:
                x_index = coords[0]
                y_index = coords[1]

                go_to(x_offset + x_index, y_offset + y_index)

                plant(Entities.Pumpkin)
                use_item(Items.Fertilizer)
                use_item(Items.Water_Tank)

                plot = get_plot(x_index, y_index)
                plot["can_harvest"] = can_harvest()
                plot["timestamp"] = get_time()
        else:
            item_counts = {
                Items.Pumpkin_Seed: plot_count,
                Items.Fertilizer: plot_count
            }

            do_trade(item_counts)

            for x_index in range(width):
                for y_index in range(height):
                    go_to(x_offset + x_index, y_offset + y_index)

                    if x_index == 0 and y_index == 0:
                        harvest()

                    use_item(Items.Fertilizer)
                    use_item(Items.Water_Tank)
                    plant(Entities.Pumpkin)

                    plot = get_plot(x_index, y_index)
                    plot["can_harvest"] = can_harvest()
                    plot["timestamp"] = get_time()
                    
        return 0

    new_farmer = {
        "init_farm": init_farm,
        "maintain_farm": maintain_farm
    }

    return new_farmer