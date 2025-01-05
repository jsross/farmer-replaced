from __builtins__ import *
from __test_harness__ import *
from Utility import *
from matrix import *
from drone import *
from grass_farmer import *
from bush_farmer import *
from tree_farmer import *
from carrot_farmer import *

def create_poly_farmer():
    init_plot_map = {
        Entities.Grass: handle_grass_plot,
        Entities.Bush: init_bush_plot,
        Entities.Tree: init_tree_plot,
        Entities.Carrot: init_carrot_plot
    }

    maintain_plot_map = {
        Entities.Grass: handle_grass_plot,
        Entities.Bush: maintain_bush_plot,
        Entities.Tree: maintain_tree_plot,
        Entities.Carrot: maintain_carrot_plot
    }

    world_size = get_world_size()
    plots = create_matrix_with_default(world_size, world_size, None)

    def handle_plot():
        x = get_pos_x()
        y = get_pos_y()

        plot = plots[x][y]

        if plot != None:
            entity_type = plot["entity_type"]

            if not plot["initialized"]:
                init_plot_map[entity_type]()
                plot["initialized"] = True
            else:
                maintain_plot_map[entity_type]()

        companion = get_companion()
        entity_type = companion[0]
        companion_coords = companion[1]
        if plots[companion_coords[0]][companion_coords[1]] == None:
            plots[companion_coords[0]][companion_coords[1]] = {
                "entity_type": entity_type,
                "initialized": False
            }

    def handle_farm():
        execute_scan_pass(world_size, world_size, handle_plot, None, 0, 0)

        return {
            "status": 0,
            "next_pass": handle_farm,
            "delay": 0
        }

    return handle_farm
