from __builtins__ import *
from Utility import *
from game_board import *

def create_farmer(drone, game_board):
	get_node = game_board["get_node"]
	drone_get_coords = drone["get_coords"]
	drone_scan = drone["scan"]
	apply_property_value = game_board["apply_property_value"]
	execute_action_plan = drone["execute_action_plan"]

	def do_work(iterations):
		start_op_count = get_op_count()

		plan = create_plan()

		for _ in range(iterations):
			execute_action_plan(plan)

		quick_print("do_work: ", get_op_count() - start_op_count)

	def create_plan():
		start_op_count = get_op_count()
		size = get_world_size()
		
		apply_property_value((0,0),(size,size), "Expected_Entity_Type", Entities.Carrots, fill_strategy_solid)
		apply_property_value((0,0),(size,size), "Expected_Entity_Type", Entities.Tree, fill_strategy_checkerd)
		apply_property_value((0,0),(size/2,size/2), "Expected_Entity_Type", Entities.Pumpkin, fill_strategy_solid)

		actions = []

		apply_scan_plan(actions, [plant_expected])

		actions.append([drone_scan, plant_expected])

		quick_print("create_plan: ", get_op_count() - start_op_count)

		return actions
	
	def apply_scan_plan(actions, action):
		start_op_count = get_op_count()

		size = get_world_size()

		for x_index in range(size):
			for y_index in range(size):
				actions.append(action)

				if x_index % 2 == 0:
					if y_index < size - 1:
						actions.append(move_north)
					else:
						actions.append(move_east)
				else:
					if y_index < size - 1:
						actions.append(move_south)
					else:
						actions.append(move_east)

		quick_print("create_scan_plan: ", get_op_count() - start_op_count)
		
		return actions

	def plant_expected():
		drone_coords = drone_get_coords()
		current_node = get_node(drone_coords)
		entity_type = current_node["Expected_Entity_Type"]

		entity_requirements = entity_requirements_map[entity_type]

		if "Grounds" in entity_requirements and get_ground_type() != entity_requirements["Grounds"]:
			till()

		if "Seeds" in entity_requirements:
			item_type = entity_requirements["Seeds"]

			if num_items(item_type) == 0:
				if not trade(item_type, get_world_size() ** 2):
					quick_print("Unable to trade for item: ", item_type)
			
		plant(entity_type)

	def handle_pumpkin():
		if get_ground_type() != Grounds.Soil:
			till()
		
		harvest()

		if(num_items(Items.Pumpkin_Seed) == 0):
			trade(Items.Pumpkin_Seed, get_world_size() * get_world_size())

		plant(Entities.Pumpkin)

		#use_item(Items.Water_Tank)
	
	def handle_carrot():
		harvest()

		if get_ground_type() != Grounds.Soil:
			till()

		if(num_items(Items.Carrot_Seed) == 0):
			trade(Items.Carrot_Seed, get_world_size() * get_world_size())

		if get_entity_type() != Entities.Carrots:
			plant(Entities.Carrots)

		#use_item(Items.Fertilizer)
		#use_item(Items.Water_Tank)

	def handle_grass():
		harvest()
		
		if get_ground_type() != Grounds.Turf:
			till()
		
		plant(Entities.Grass)
		#use_item(Items.Water_Tank)
	
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
		#use_item(Items.Fertilizer)
		#use_item(Items.Water_Tank)
	
	def handle_cactus():
		pass

	def handle_hedge():
		pass

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

	entity_requirements_map = {
		Entities.Grass: {
			"Grounds": Grounds.Turf
		},
		Entities.Carrots: {
			"Grounds": Grounds.Soil,
			"Seeds": Items.Carrot_Seed
		},
		Entities.Tree: {
			"Grounds": Grounds.Turf
		},
		Entities.Pumpkin: {
			"Grounds": Grounds.Soil,
			"Seeds": Items.Pumpkin_Seed
		}
	}

	move_north = [move, North]
	move_east = [move, East]
	move_south = [move, South]
	move_west = [move, West]

	new_farmer = {
		"do_work": do_work
	}

	return new_farmer

def create_action_with_arg(func, arg):
	def execute():
		func(arg)
	
	return execute


