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

	execute_plot_actions = drone["execute_plot_actions"]

	def do_work(iterations):
		clear()

		size = get_world_size()
		start_op_count = get_op_count()

		width = size / 2
		height = size / 2

		create_region((0, 0), width, height, handle_sunflower_region, None)
		create_region((0, size/2), width, height, handle_basic_region, {"entity_type":Entities.Bush})
		create_region((size/2, 0), width, height, handle_basic_region, {"entity_type":Entities.Bush})
		create_region((size/2, size/2), width, height, handle_pumpkin_region, None )

		regions = get_regions()

		for iteration in range(iterations):
			for region in regions:
				handle_region = region["handler"]

				handle_region(drone, region, iteration)

		quick_print("do_work: ", get_op_count() - start_op_count)
	
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

	