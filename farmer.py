from __builtins__ import *
from Utility import *
from game_board import *
from navigator import *

def create_farmer(drone, game_board):
	get_plot = game_board["get_plot"]
	get_plots = game_board["get_plots"]
	apply_property_value = game_board["apply_property_value"]
	do_scan = drone["do_scan"]
	do_trade = drone["do_trade"]

	execute_plot_plans = drone["execute_plot_plans"]

	def create_plan(_x, _y):
		return []

	def do_work(iterations):
		clear()

		size = get_world_size()
		start_op_count = get_op_count()

		#apply_property_value((0,0),(size,size), "Expected_Entity_Type", Entities.Carrots, fill_strategy_solid)
		#apply_property_value((0,0),(size,size), "Expected_Entity_Type", Entities.Tree, fill_strategy_checkerd)
		apply_property_value((0,0),(size,size), "Expected_Entity_Type", Entities.Pumpkin, fill_strategy_solid)

		scan_paths = create_scan_paths(size, size)
		
		prep_plot_plans = create_initial_plot_plans()
		do_trade(prep_plot_plans[1])

		execute_plot_plans(prep_plot_plans[0], scan_paths)

		maint_plan = create_maintenance_plan()

		for _ in range(iterations):
			do_trade(maint_plan[1])
			execute_plot_plans(maint_plan[0], scan_paths)

		quick_print("do_work: ", get_op_count() - start_op_count)
	
	def create_initial_plot_plans():
		start_op_count = get_op_count()
		size = get_world_size()

		plot_plans = create_matrix(get_world_size(), create_plan)

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

		quick_print("create_initial_plot_plans: ", get_op_count() - start_op_count)

		return (plot_plans, seed_counts)
	
	def create_maintenance_plan():
		start_op_count = get_op_count()
		size = get_world_size()

		plot_plans = create_matrix(get_world_size(), create_plan)

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
				plot_plan.append([handle_scan, x_index, y_index])
				
				if "seeds" in requirements:
					seed_counts[requirements["seeds"]] += 1

		quick_print("create_maintenance_plan: ", get_op_count() - start_op_count)

		return (plot_plans,seed_counts)
	
	def handle_scan(x,y):
		get_plot(x,y)["scan"] = do_scan()

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

	new_farmer = {
		"do_work": do_work
	}

	return new_farmer

def create_action_with_arg(func, arg):
	def execute():
		func(arg)
	
	return execute


