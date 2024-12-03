from __builtins__ import *

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