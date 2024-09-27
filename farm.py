from __builtins__ import *
from Utility import *

def create_farm_plan(drone, game_board):
	game_board_get_node = game_board["get_node"]
	drone_do_move = drone["do_move"]
	drone_get_coords = drone["get_coords"]
	plant_plan = create_matrix(get_world_size(), 2)

	def do_scan_farm():
		for _ in range(0, get_world_size()):
			for _ in range(0, get_world_size()):
				farm()
				drone_do_move(North)
			drone_do_move(East)

	def execute_plan(iterations):
		for _ in range(iterations):
			do_scan_farm()

	def apply_normal_plan():
		#apply_entity_type(plant_plan, 0, 0,get_world_size(), get_world_size(), Entities.Pumpkin, fill_strategy_solid)
		#apply_entity_type(plant_plan, 0, 0,get_world_size() / 2, get_world_size() / 2, Entities.Tree,fill_strategy_checkerd)
		#apply_entity_type(plant_plan, 0, 0,get_world_size(), get_world_size(), Entities.Sunflower,fill_strategy_solid)
		apply_entity_type(plant_plan, 0, 0, 1, 1, Entities.Bush, fill_strategy_solid)

	def handle_pumpkin():
		if get_ground_type() != Grounds.Soil:
			till()
			
		harvest()

		plant(Entities.Pumpkin)

		use_item(Items.Water_Tank)
	
	def handle_carrot():
		harvest()

		if get_ground_type() != Grounds.Soil:
			till()

		if(num_items(Items.Carrot_Seed) >= 0):
			trade(Items.Carrot_Seed, get_world_size() * get_world_size())

		if get_entity_type() != Entities.Carrots:
			plant(Entities.Carrots)

		use_item(Items.Fertilizer)
		use_item(Items.Water_Tank)

	def handle_grass():
		harvest()
		
		if get_ground_type() != Grounds.Turf:
			till()
		
		plant(Entities.Grass)
		use_item(Items.Water_Tank)
	
	def handle_bush():
		if get_ground_type() != Grounds.Turf:
			till()

		harvest()
		
		plant(Entities.Bush)

		use_item(Items.Fertilizer)
		use_item(Items.Water_Tank)
	
	def handle_sunflower():
		harvest()

		if get_ground_type() != Grounds.Soil:
			till()

		use_item(Items.Fertilizer)
		use_item(Items.Water_Tank)

		if(num_items(Items.Sunflower_Seed) >= 0):
			trade(Items.Sunflower_Seed, get_world_size() * get_world_size())
			
		plant(Entities.Sunflower)
	
	def handle_tree():
		harvest()

		if get_ground_type() != Grounds.Soil:
			till()

		plant(Entities.Tree)
		use_item(Items.Fertilizer)
		use_item(Items.Water_Tank)
	
	def handle_cactus():
		pass

	def handle_hedge():
		pass

	def farm():
		current_coords = drone_get_coords()
		
		entity_type = plant_plan[current_coords[0]][current_coords[1]]

		if entity_type in entity_handlers:
			handler = entity_handlers[entity_type]
			handler()

	entity_handlers = {
		Entities.Bush:handle_bush,
		Entities.Cactus: handle_cactus,
		Entities.Carrots: handle_carrot,
		Entities.Grass: handle_grass,
		Entities.Hedge: handle_hedge,
		Entities.Pumpkin: handle_pumpkin,
		Entities.Sunflower: handle_sunflower,
		Entities.Tree: handle_tree
	}

	apply_normal_plan()
	
	new_farm_plan = {
		"execute_plan": execute_plan
	}

	return new_farm_plan