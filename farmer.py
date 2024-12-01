from __builtins__ import *
from Utility import *
from farm import *
from navigator import *

def create_farmer(drone, farm):
	get_plot = farm["get_plot"]
	create_region = farm["create_region"]
	get_regions = farm["get_regions"]
	apply_property_value = farm["apply_property_value"]

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

		scan_paths = create_scan_paths(size, size)

		regions = get_regions()

		for current_iteration in range(iterations):
			for region in regions:
				region_type = region["type"]
				region_plots = region["plots"]

				if current_iteration == 0 and region_type in init_plan_factories:
					create_plan = init_plan_factories[region_type]
					create_plan(region)

				if current_iteration > 0 and region_type in mid_plan_factories:
					create_plan = mid_plan_factories[region_type]
					create_plan(region)

				for plot in region_plots:
					plot_plan = plot["plan"]

					if region_type in region_handlers:
						region_handler = region_handlers[region_type]
						plot_plan.append([region_handler])

					needed_item_counts[Items.Fertilizer] += 1
					
					plot_plan.append([use_item, Items.Fertilizer])
					plot_plan.append([use_item, Items.Water_Tank])
					
					plot_plan.append([handle_scan, plot])

			do_trade(needed_item_counts)
			execute_plot_plans(farm, scan_paths)

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
	
	region_handlers = {
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

	init_plan_factories = {
		Entities.Pumpkin: create_initial_pumpkin_plan
	}

	def create_maintence_pumpkin_plan(region):
		plots = region["plots"]
		anchor_coords = region["anchor_coords"]
		height = region["height"]

		def not_ready_test(plot, _):
			return not plot["can_harvest"]

		not_ready = find_in_array(plots, not_ready_test)

		if len(not_ready) > 0:
			needed_item_counts[Items.Pumpkin_Seed] += len(not_ready) 
			for plot in not_ready:
				plot["plan"].append([plant, Entities.Pumpkin])
		else:
			#TODO: Get anchor. Determine if path will hit anchor or anchor + height first.
			if anchor_coords[0] % 2:
				anchor = get_plot(anchor_coords)
			else:
				anchor = get_plot((anchor_coords[0], anchor_coords[1] + height - 1))

			anchor["plan"].append([harvest])
			needed_item_counts[Items.Pumpkin_Seed] += len(plots)

			for plot in plots:
				plot["plan"].append([plant, Entities.Pumpkin])

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