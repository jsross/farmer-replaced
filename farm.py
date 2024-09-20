from __builtins__ import *
from Utility import *

def create_farm_plan():
	plan = create_matrix(get_world_size(), 2)

	apply_entity_type(plan, 0, 0,get_world_size(), get_world_size(), Entities.Pumpkin, fill_strategy_solid)
	apply_entity_type(plan, 0, 0,get_world_size() / 2, get_world_size() / 2, Entities.Tree,fill_strategy_checkerd)
	apply_entity_type(plan, 0, 0,get_world_size() / 2, get_world_size() / 2, Entities.Sunflower,fill_strategy_checkerd_alt)
	apply_entity_type(plan, get_world_size() / 2, get_world_size() / 2, get_world_size(), get_world_size(), Entities.Carrots,fill_strategy_solid)

	return plan

def do_harvest(plot):
	if plot["can_harvest"]:
		harvest()
		plot["can_harvest"] = False
		plot["entity_type"] = None

def handle_pumpkin(farm_land, coord):
	plot = farm_land["get_node"](coord)

	if get_ground_type() != Grounds.Soil:
		till()
		
	do_harvest(plot)

	plant(Entities.Pumpkin)

	use_item(Items.Water_Tank)

def handle_carrot(farm_land, coord):
	plot = farm_land["get_node"](coord)

	do_harvest(plot)
	
	if plot["ground_type"] != Grounds.Soil:
		till()
		plot["ground_type"] = Grounds.Soil
		plot["can_harvest"] = False
		plot["entity_type"] = None

	if(num_items(Items.Carrot_Seed) >= 0):
		trade(Items.Carrot_Seed, get_world_size() * get_world_size())

	if plot["entity_type"] != Entities.Carrots:
		if plant(Entities.Carrots):
			plot["entity_type"] = Entities.Carrots
			plot["can_harvest"] = False

	use_item(Items.Fertilizer)
	use_item(Items.Water_Tank)

def handle_grass(farm_land, coord):
	plot = farm_land["get_node"](coord)
	
	do_harvest(plot)
	
	if get_ground_type() != Grounds.Turf:
		till()
	
	plant(Entities.Grass)
	use_item(Items.Water_Tank)

def handle_bush(farm_land, coord):
	plot = farm_land["get_node"](coord)

	if get_ground_type() != Grounds.Turf:
		till()

	do_harvest(plot)
	
	plant(Entities.Bush)

	use_item(Items.Fertilizer)
	use_item(Items.Water_Tank)

def handle_sunflower(farm_land, coord):
	plot = farm_land["get_node"](coord)

	do_harvest(plot)

	if get_ground_type() != Grounds.Soil:
		till()

	use_item(Items.Fertilizer)
	use_item(Items.Water_Tank)
		
	plant(Entities.Sunflower)

def handle_tree(farm_land, coord):
	plot = farm_land["get_node"](coord)

	do_harvest(plot)

	if get_ground_type() != Grounds.Soil:
		till()

	plant(Entities.Tree)
	use_item(Items.Fertilizer)
	use_item(Items.Water_Tank)