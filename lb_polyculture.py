from farmer import *
from poly_farmer import *

farm_size = get_world_size()

farm_goal = {
    Items.Hay: 100000,
    Items.Wood: 100000,
    Items.Carrot: 100000
}

execute_single_farmer(create_poly_farmer(farm_goal))