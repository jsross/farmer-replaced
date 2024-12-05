from __builtins__ import *
from __test_harness__ import *
from Utility import *
from farm import *
from navigator import *
from sunflower import *
from pumpkin import *
from plot_handlers import *

def create_farmer(drone, farm):
	create_region = farm["create_region"]
	get_regions = farm["get_regions"]
	select_coords = farm["select_coords"]

	needed_item_counts = {
		Items.Carrot_Seed: 0,
		Items.Cactus_Seed: 0,
		Items.Fertilizer: 0,
		Items.Pumpkin_Seed: 0,
		Items.Sunflower_Seed: 0
	}

	execute_plot_actions = drone["execute_plot_actions"]

	def do_work(iterations):
		clear()

		size = get_world_size()
		start_op_count = get_op_count()

		#create_region(Entities.Carrots, (0,0), (size,size), fill_strategy_solid)
 
		width = size/2
		height = size/2

		#create_region(Entities.Carrots, (0,0), width, height, fill_strategy_checkerd)
		#create_region(Entities.Tree, (0,0), width, height, fill_strategy_checkerd_alt)
		create_region(Entities.Pumpkin, (0, 0), size, size, fill_strategy_solid)
		#create_region(Entities.Sunflower, (size/2, 0), width, height, fill_strategy_solid)
		#create_region(Entities.Bush, (size/2, size/2), width, height, fill_strategy_solid)

		regions = get_regions()

		for region in regions:
			region_type = region["type"]
			region_plots = region["plots"]

			if region_type in init_plan_factories:
				create_plan = init_plan_factories[region_type]
				create_plan(region)

			if region_type in static_handlers:
				region_handler = static_handlers[region_type]

				for plot in region_plots:
					plot["priority"] = MAX_PRIORITY
					plot["action"] = region_handler
		
		for priority in range(MAX_PRIORITY, 1, -1):
			properties = {
				"priority": priority
			}

			coords = select_coords(properties)
			execute_plot_actions(coords)

		for _ in range(1, iterations):
			for region in regions:
				region_type = region["type"]

				if region_type in mid_plan_factories:
					create_plan = mid_plan_factories[region_type]
					create_plan(region)

			do_trade(needed_item_counts)

			for priority in range(MAX_PRIORITY, 1, -1):
				properties = {
					"priority": priority
				}

				coords = select_coords(properties)
				execute_plot_actions(coords)

		quick_print("do_work: ", get_op_count() - start_op_count)
	
	static_handlers = {
		Entities.Bush:handle_bush,
		Entities.Carrots: handle_carrot,
		Entities.Grass: handle_grass,
		Entities.Tree: handle_tree
	}

	init_plan_factories = {
		Entities.Pumpkin: apply_initial_pumpkin_plan,
		Entities.Sunflower: apply_init_sunflower_plan
	}

	mid_plan_factories = {
		Entities.Pumpkin: apply_maintence_pumpkin_plan,
		Entities.Sunflower: apply_maintence_sunflower_plan
	}

	new_farmer = {
		"do_work": do_work
	}

	return new_farmer

def do_trade(needed_seed_counts):
	for item_type in needed_seed_counts:
		current_count = num_items(item_type)
		needed_count = needed_seed_counts[item_type]
		to_buy = needed_count - current_count

		if to_buy > 0:
			trade(item_type, to_buy)

		needed_seed_counts[item_type] = 0

	