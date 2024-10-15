from __builtins__ import *
from Utility import *
from game_board import *

def create_farmer(drone, game_board):
	get_plot = game_board["get_node"]
	apply_property_value = game_board["apply_property_value"]
	do_till = drone["do_till"]
	do_plant = drone["do_plant"]
	execute_action_plan = drone["execute_action_plan"]

	def do_work(iterations):
		start_op_count = get_op_count()

		prep_plan = create_initial_prep_plan()

		execute_action_plan(prep_plan)

		quick_print("do_work: ", get_op_count() - start_op_count)

	def create_initial_prep_plan():
		start_op_count = get_op_count()
		size = get_world_size()
		
		apply_property_value((0,0),(size,size), "Expected_Entity_Type", Entities.Carrots, fill_strategy_solid)
		apply_property_value((0,0),(size,size), "Expected_Entity_Type", Entities.Tree, fill_strategy_checkerd)
		#Sapply_property_value((0,0),(size/2,size/2), "Expected_Entity_Type", Entities.Pumpkin, fill_strategy_solid)

		seed_counts = {
			Items.Cactus_Seed: 0,
			Items.Carrot_Seed: 0,
			Items.Pumpkin_Seed: 0,
			Items.Sunflower_Seed: 0
		}

		plan = []
		plan.append([clear])

		def create_plan(_,_):
			return []
		
		current_x = 0
		current_y = 0

		for x_index in range(size):
			for y_index in range(size):
				plot = get_plot((current_x, current_y))

				entity_type = plot["Expected_Entity_Type"]
				requirements = requirements_map[entity_type]

				if "Grounds" in requirements and requirements["Grounds"]  == Grounds.Soil:
					plan.append([do_till])

				if "Seeds" in requirements:
					item_type = requirements["Seeds"]

					seed_counts[item_type] += 1

				plan.append([do_plant, entity_type])

				if x_index % 2 == 0:
					if y_index < size - 1:
						plan.append(move_north)
						current_y += 1
					else:
						plan.append(move_east)
						current_x += 1
				else:
					if y_index < size - 1:
						plan.append(move_south)
						current_y -= 1
					else:
						plan.append(move_east)
						current_x += 1

		for item_type in seed_counts:
			required_count = seed_counts[item_type]

			if required_count > 0:
				plan.insert(0, [trade, item_type, required_count])


		quick_print("create_plan: ", get_op_count() - start_op_count)

		return plan
	

	requirements_map = {
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


