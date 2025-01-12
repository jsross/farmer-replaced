from tree_farmer import *

farm_size = get_world_size()

execute_single_farmer(create_tree_farmer(farm_size, farm_size, 0, 0, 100000))