from __builtins__ import *
from Utility import *
from game_board import *

def create_farmer(drone, game_board):
	get_node = game_board["get_node"]
	drone_do_move = drone["do_move"]
	drone_get_coords = drone["get_coords"]
	drone_scan = drone["scan"]
	apply_property_value = game_board["apply_property_value"]

	def do_work(iterations):
		start_op_count = get_op_count()

		plan = create_plan()

		for _ in range(iterations):
			execute_plan(plan)

		quick_print("do_work: ", get_op_count() - start_op_count)

	def create_plan():
		start_op_count = get_op_count()
		size = get_world_size()
		
		apply_property_value((0,0),(size,size), "Expected_Entity_Type", Entities.Carrots, fill_strategy_solid)
		apply_property_value((0,0),(size,size), "Expected_Entity_Type", Entities.Tree, fill_strategy_checkerd)
		actions = []

		actions.append((drone_scan, handle_expected_entity))

		quick_print("create_plan: ", get_op_count() - start_op_count)

		return actions

	def handle_expected_entity():
		drone_coords = drone_get_coords()
		current_node = get_node(drone_coords)

		entity_type = current_node["Expected_Entity_Type"]
		handler = entity_handlers[entity_type]

		handler()

	
	def execute_plan(plan):
		start_op_count = get_op_count()

		for action in plan:
			action[0](action[1])
		
		quick_print("execute_plan: ", get_op_count() - start_op_count)

	def handle_pumpkin():
		if get_ground_type() != Grounds.Soil:
			till()
		
		harvest()

		if(num_items(Items.Pumpkin_Seed) == 0):
			trade(Items.Pumpkin_Seed, get_world_size() * get_world_size())

		plant(Entities.Pumpkin)

		use_item(Items.Water_Tank)
	
	def handle_carrot():
		harvest()

		if get_ground_type() != Grounds.Soil:
			till()

		if(num_items(Items.Carrot_Seed) == 0):
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
		current_node = get_node(current_coords)
		
		if "entity_type" in current_node:
			entity_type = current_node["entity_type"]

			if entity_type in entity_handlers:
				handler = entity_handlers[entity_type]
				handler()
	
	def do_move(args):
		move(args[0])

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

	new_farmer = {
		"do_work": do_work
	}

	return new_farmer

def create_action(func, arg):

	def execute():
		func(arg)
	
	return execute