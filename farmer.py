from __builtins__ import *
from Utility import *
from farm import *
from navigator import *

def create_farmer(drone, farm):
	create_region = farm["create_region"]
	get_regions = farm["get_regions"]
	select_coords = farm["select_coords"]

	max_priority = 15
	no_priority = 0

	do_scan = drone["do_scan"]
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
		create_region(Entities.Pumpkin, (size/2, 0), width, height, fill_strategy_solid )
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
						plot_plan.append([region_handler])
						plot["priority"] = max_priority
						plot_plan.append([handle_scan, plot])
			
			do_trade(needed_item_counts)

			for priority in range(max_priority, 1, -1):
				properties = {
					"priority": priority
				}

				coords = select_coords(properties)
				paths = create_paths(coords)
				execute_plot_plans(farm, paths)

		quick_print("do_work: ", get_op_count() - start_op_count)
	
	def handle_scan(plot):
		scan = do_scan()
		
		for key in scan:
			plot[key] = scan[key]

	def handle_carrot():
		harvest()

		if get_ground_type() != Grounds.Soil:
			till()

		if(num_items(Items.Carrot_Seed) == 0):
			trade(Items.Carrot_Seed, get_world_size() * get_world_size())

		if get_entity_type() != Entities.Carrots:
			plant(Entities.Carrots)

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
	
	def handle_sunflower():
		harvest()

		if get_ground_type() != Grounds.Soil:
			till()

		if(num_items(Items.Sunflower_Seed) >= 0):
			trade(Items.Sunflower_Seed, get_world_size() * get_world_size())
			
		plant(Entities.Sunflower)
	
	def handle_tree():
		harvest()

		if get_ground_type() != Grounds.Soil:
			till()

		plant(Entities.Tree)
	
	static_handlers = {
		Entities.Bush:handle_bush,
		Entities.Carrots: handle_carrot,
		Entities.Grass: handle_grass,
		Entities.Sunflower: handle_sunflower,
		Entities.Tree: handle_tree
	}

	def create_initial_pumpkin_plan(region):
		plots = region["plots"]
		needed_item_counts[Items.Pumpkin_Seed] += len(plots)

		for plot in plots:
			plot["plan"].append([till])
			plot["plan"].append([plant, Entities.Pumpkin])
			plot["priority"] = max_priority

	init_plan_factories = {
		Entities.Pumpkin: create_initial_pumpkin_plan
	}

	def create_maintence_pumpkin_plan(region):
		plots = region["plots"]

		def not_ready_test(plot, _):
			return not plot["can_harvest"]

		not_ready = find_in_array(plots, not_ready_test)

		if len(not_ready) == 0:
			for index in range(len(plots)):
				plot = plots[index]
				plot_plan = plot["plan"]

				if index == 0:
					plot_plan.append([harvest])
					plot["priority"] = 15
				else:
					plot["priority"] = 14 

				plot_plan.append([plant, Entities.Pumpkin])
				plot_plan.append([use_item, Items.Fertilizer])
				plot_plan.append([use_item, Items.Water_Tank])
				plot_plan.append([handle_scan, plot])

				needed_item_counts[Items.Pumpkin_Seed] += len(not_ready)
		else:
			for plot in plots:
				if not plot["can_harvest"]:
					plot["priority"] = max_priority
					plot_plan = plot["plan"]

					plot_plan.append([plant, Entities.Pumpkin])
					plot_plan.append([use_item, Items.Fertilizer])
					plot_plan.append([use_item, Items.Water_Tank])
					plot_plan.append([handle_scan, plot])

					needed_item_counts[Items.Pumpkin_Seed] += len(not_ready)
				else:
					plot["priority"] = no_priority

	mid_plan_factories = {
		Entities.Pumpkin: create_maintence_pumpkin_plan
	}

	new_farmer = {
		"do_work": do_work
	}

	return new_farmer

def create_action_with_arg(func, arg):
	def execute():
		func(arg)
	
	return execute