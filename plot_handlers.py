from __builtins__ import *
from __test_harness__ import *
from Utility import *

def handle_basic_region(drone, region, _):
    static_handlers = {
        Entities.Bush:handle_bush,
        Entities.Carrots: handle_carrot,
        Entities.Grass: handle_grass,
        Entities.Tree: handle_tree
    }

    plots = region["plots"]
    options = region["options"]
    entity_type = options["entity_type"]

    path = []

    for plot in plots:
        plot["priority"] = MAX_PRIORITY
        plot["action"] = static_handlers[entity_type]
        path.append(plot["coords"])

    drone["execute_plot_actions"](path)


def handle_carrot(plot):
    harvest()

    if get_ground_type() != Grounds.Soil:
        till()

    if(num_items(Items.Carrot_Seed) == 0):
        trade(Items.Carrot_Seed, get_world_size() * get_world_size())

    if get_entity_type() != Entities.Carrots:
        plant(Entities.Carrots)

def handle_grass(plot):
    harvest()
    
    if get_ground_type() != Grounds.Turf:
        till()
    
    plant(Entities.Grass)
    use_item(Items.Water_Tank)
	
def handle_bush(plot):
    if get_ground_type() != Grounds.Turf:
        till()

    harvest()
    
    plant(Entities.Bush)
	
	
def handle_tree(plot):
    harvest()

    if get_ground_type() != Grounds.Soil:
        till()

    plant(Entities.Tree)

