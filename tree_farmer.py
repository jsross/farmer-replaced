from __builtins__ import *
from __test_harness__ import *
from Utility import *
from bush_farmer import *

def init_tree_farm(width, height):
    execute_dual_scan_pass(width, height, init_tree_plot, init_bush_plot)

    return 0

def maintain_tree_farm(width, height):
    execute_dual_scan_pass(width, height, maintain_tree_plot, maintain_bush_plot)

    return 0

def init_tree_plot():
    if get_water() < 0.25:
        use_item(Items.Water)

    plant(Entities.Tree)
    use_item(Items.Fertilizer)

def maintain_tree_plot():
    if get_water() < 0.25:
        use_item(Items.Water)

    if(can_harvest()):
        harvest()
        
        plant(Entities.Tree)
        use_item(Items.Fertilizer)

def create_tree_farmer(width, height, x_offset, y_offset, goal):

    def init_farm():
        for x_index in range(width):
            for y_index in range(height):
                go_to(x_index + x_offset, y_index + y_offset)

                rem = y_index % 2

                if (x_index - rem ) % 2 == 0:
                    init_tree_plot()
                else:
                    init_bush_plot()

        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 1
        }

    def maintain_farm():
        for x_index in range(width):
            for y_index in range(height):
                go_to(x_index + x_offset, y_index + y_offset)

                rem = y_index % 2

                if (x_index - rem ) % 2 == 0:
                    maintain_tree_plot()
                else:
                    maintain_bush_plot()

        if num_items(Items.Wood) > goal:
            return None
        
        return {
            "status": 0,
            "next_pass": maintain_farm,
            "delay": 0
        }
        
    return init_farm