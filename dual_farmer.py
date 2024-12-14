from __builtins__ import *
from __test_harness__ import *
from Utility import *
from carrot_farmer import *
from tree_farmer import *
from bush_farmer import *
from grass_farmer import *

def create_dual_farmer(drone, width, height, x_offset, y_offset, entities):
    go_to = drone["go_to"]

    init_plot_map = {
        Entities.Carrots: init_carrot_plot,
        Entities.Tree: init_tree_plot,
        Entities.Bush: init_bush_plot,
        Entities.Grass: init_grass_plot
    }

    maintain_plot_map = {
        Entities.Carrots: maintain_carrot_plot,
        Entities.Tree: maintain_tree_plot,
        Entities.Bush: maintain_bush_plot,
        Entities.Grass: maintain_grass_plot
    }

    init_plot_funcs = (init_plot_map[entities[0]], init_plot_map[entities[1]])
    maintain_plot_funcs = (maintain_plot_map[entities[0]], maintain_plot_map[entities[1]])

    def init_farm():
        for x_index in range(width):
            for y_index in range(height):
                go_to(x_index + x_offset, y_index + y_offset)

                rem = y_index % 2

                if (x_index - rem ) % 2 == 0:
                    init_plot_funcs[0]()
                else:
                    init_plot_funcs[1]()
        
        return 0

    def maintain_farm():
        for x_index in range(width):
            for y_index in range(height):
                go_to(x_index + x_offset, y_index + y_offset)

                rem = y_index % 2

                if (x_index - rem ) % 2 == 0:
                    maintain_plot_funcs[0]()
                else:
                    maintain_plot_funcs[1]()
        
        return 0
        
    new_farmer = {
        "init_farm": init_farm,
        "maintain_farm": maintain_farm
    }

    return new_farmer