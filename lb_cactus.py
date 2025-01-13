from farmer import *
from cactus_farmer import *

farm_size = get_world_size()

execute_single_farmer(create_cactus_farmer(farm_size, farm_size, 0, 0, 100000))