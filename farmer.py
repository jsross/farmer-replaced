from __builtins__ import *
from Utility import *
from game_board import *

def create_farmer(drone, game_board):
	get_plot = game_board["get_plot"]
	get_plots = game_board["get_plots"]
	apply_property_value = game_board["apply_property_value"]
	do_scan = drone["do_scan"]
	execute_action_plan = drone["execute_action_plan"]

	def create_plan(x, y):
		return []
	
	plot_plans = create_matrix(get_world_size(), create_plan)

	def do_work(iterations):
		start_op_count = get_op_count()

		prep_plan = create_initial_prep_plan()

		execute_action_plan(prep_plan)

		for _ in range(iterations):
			execute_action_plan(create_maintenance_plan())

		quick_print("do_work: ", get_op_count() - start_op_count)

	def create_initial_prep_plan():
		start_op_count = get_op_count()
		size = get_world_size()
		
		apply_property_value((0,0),(size,size), "Expected_Entity_Type", Entities.Carrots, fill_strategy_solid)
		apply_property_value((0,0),(size,size), "Expected_Entity_Type", Entities.Tree, fill_strategy_checkerd)
		apply_property_value((0,0),(size/2,size/2), "Expected_Entity_Type", Entities.Pumpkin, fill_strategy_solid)

		seed_counts = {
			Items.Cactus_Seed: 0,
			Items.Carrot_Seed: 0,
			Items.Pumpkin_Seed: 0,
			Items.Sunflower_Seed: 0
		}
		
		for x_index in range(size):
			for y_index in range(size):
				plot = get_plot((x_index, y_index))
				plot_plan = plot_plans[x_index][y_index]

				entity_type = plot["Expected_Entity_Type"]
				requirements = requirements_map[entity_type]

				if "grounds" in requirements and requirements["grounds"]  == Grounds.Soil:
					plot_plan.append([till])

				if "seeds" in requirements:
					seed_counts[requirements["seeds"]] += 1

				plot_plan.append([plant, entity_type])
				plot_plan.append([do_scan])

		plan = create_scan_plan()

		for item_type in seed_counts:
			required_count = seed_counts[item_type]

			if required_count > 0:
				plan.insert(0, [trade, item_type, required_count])
		
		plan.insert(0, [clear])

		quick_print("create_initial_prep_plan: ", get_op_count() - start_op_count)

		return plan
	
	def create_maintenance_plan():
		start_op_count = get_op_count()
		
		size = get_world_size()

		seed_counts = {
			Items.Cactus_Seed: 0,
			Items.Carrot_Seed: 0,
			Items.Pumpkin_Seed: 0,
			Items.Sunflower_Seed: 0
		}

		for x_index in range(size):
			for y_index in range(size):
				plot = get_plot((x_index, y_index))
				plot_plan = plot_plans[x_index][y_index]

				entity_type = plot["Expected_Entity_Type"]
				requirements = requirements_map[entity_type]

				if "harvest_test" in requirements:
					if requirements["harvest_test"]():
						plot_plan.append([harvest])
				else:
					plot_plan.append([harvest])
					
				plot_plan.append([plant, entity_type])
				plot_plan.append([do_scan])
				
				if "seeds" in requirements:
					seed_counts[requirements["seeds"]] += 1
		
		plan = create_scan_plan()

		for item_type in seed_counts:
			required_count = seed_counts[item_type]

			if required_count > 0:
				plan.insert(0, [trade, item_type, required_count])

		quick_print("create_maintenance_plan: ", get_op_count() - start_op_count)

		return plan
		
	def create_scan_plan():
		size = get_world_size()

		plan = []
		
		current_x = 0
		current_y = 0

		for x_index in range(size):
			for y_index in range(size):
				plot_plan = plot_plans[current_x][current_y]

				while len(plot_plan) > 0:
					plan.append(plot_plan.pop(0))

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

		return plan
	
	def can_harvest_pumpkin():
		plots = get_plots(Entities.Pumpkin)

		def can_harvest_plot(item, _):
			return item["can_harvest"] 
		
		results = find_in_array(plots, can_harvest_plot)
	
		if len(results) == len(plots):
			return True
		
		return False

	requirements_map = {
		Entities.Bush: {
			"grow_speed": 4.0
		},
		Entities.Carrots: {
			"grounds": Grounds.Soil,
			"seeds": Items.Carrot_Seed,
			"grow_speed": 6.0
		},
		Entities.Cactus: {
			"grounds": Grounds.Soil,
			"seeds": Items.Cactus_Seed,
			"grow_speed": 6.0
		},
		Entities.Grass: {
			"grounds": Grounds.Turf,
			"grow_speed": 0.5
		},
		Entities.Pumpkin: {
			"grounds": Grounds.Soil,
			"seeds": Items.Pumpkin_Seed,
			"grow_speed": 2.0,
			"harvest_test": can_harvest_pumpkin
		},
		Entities.Sunflower: {
			"grounds": Grounds.Soil,
			"seeds": Items.Sunflower_Seed,
			"grow_speed": 5.0
		},
		Entities.Tree: {
			"grounds": Grounds.Turf,
			"grow_speed": 7.0
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


