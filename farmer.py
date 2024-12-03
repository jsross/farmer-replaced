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

	do_trade = drone["do_trade"]

	needed_item_counts = {
		Items.Carrot_Seed: 0,
		Items.Cactus_Seed: 0,
		Items.Fertilizer: 0,
		Items.Pumpkin_Seed: 0,
		Items.Sunflower_Seed: 0
	}

	execute_plot_plans = drone["execute_plot_plans"]

	def do_work(iterations):
		clear()

		size = get_world_size()
		start_op_count = get_op_count()

		#create_region(Entities.Carrots, (0,0), (size,size), fill_strategy_solid)

		width = size/2
		height = size/2

		create_region(Entities.Carrots, (0,0), width, height, fill_strategy_checkerd)
		create_region(Entities.Tree, (0,0), width, height, fill_strategy_checkerd_alt)
		create_region(Entities.Pumpkin, (0, size/2), width, height, fill_strategy_solid)
		create_region(Entities.Sunflower, (size/2, 0), width, height, fill_strategy_solid )
		create_region(Entities.Bush, (size/2, size/2), width, height, fill_strategy_solid)

		regions = get_regions()

		for current_iteration in range(iterations):
			for region in regions:
				region_type = region["type"]

				if current_iteration == 0 and region_type in init_plan_factories:
					create_plan = init_plan_factories[region_type]
					create_plan(region)

				if current_iteration > 0 and region_type in mid_plan_factories:
					create_plan = mid_plan_factories[region_type]
					create_plan(region)

				if region_type in static_handlers:
					region_plots = region["plots"]
					region_handler = static_handlers[region_type]

					for plot in region_plots:
						plot_plan = plot["plan"]
						plot_plan.append([region_handler, plot])
						plot["priority"] = MAX_PRIORITY
	
			do_trade(needed_item_counts)

			for priority in range(MAX_PRIORITY, 1, -1):
				properties = {
					"priority": priority
				}

				coords = select_coords(properties)
				execute_plot_plans(farm, coords)

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