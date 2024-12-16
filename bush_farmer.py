from __builtins__ import *
from __test_harness__ import *
from Utility import *

def create_bush_farmer(drone, width, height, x_offset, y_offset):
    go_to = drone["go_to"]
    plot_count = width * height

    def init_farm():
        trade(Items.Fertilizer, plot_count)

        for x_index in range(width):
            for y_index in range(height):
                go_to(x_index + x_offset, y_index + y_offset)
                
                init_bush_plot()
        
        return 0

    def maintain_farm():
        trade(Items.Fertilizer, plot_count)

        for x_index in range(width):
            for y_index in range(height):
                go_to(x_index + x_offset, y_index + y_offset)

                maintain_bush_plot()

        return 0
        
    new_farmer = {
        "init_farm": init_farm,
        "maintain_farm": maintain_farm
    }
     
    return new_farmer

def init_bush_plot():
    use_item(Items.Fertilizer)
    use_item(Items.Water_Tank)

    plant(Entities.Bush)

def maintain_bush_plot():
    if(can_harvest()):
        harvest()
        use_item(Items.Fertilizer)
        use_item(Items.Water_Tank)
        plant(Entities.Bush)

    