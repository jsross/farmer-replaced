from __builtins__ import *

from Utility import *
from drone import *
from graph import *
from farm import *
from farm import *
from maze import *
from carrot_farmer import *
from dual_farmer import *

MAX_PRIORITY = 15
NO_PRIORITY = 0

farm_size = get_world_size()

my_drone = create_drone()
my_farm = create_farm(farm_size, farm_size)

grass_farmer = create_grass_farmer(my_drone, farm_size, farm_size, 0, 0)
grass_farmer["init_farm"]()

bush_farmer = create_bush_farmer(my_drone, farm_size, farm_size, 0, 0)
bush_farmer["init_farm"]()
bush_farmer["maintain_farm"]()

carrot_farmer = create_carrot_farmer(my_drone, farm_size, farm_size, 0, 0)
carrot_farmer["init_farm"]()
carrot_farmer["maintain_farm"]()

tree_farmer = create_dual_farmer(my_drone, farm_size, farm_size, 0, 0, (Entities.Tree, Entities.Carrots))
tree_farmer["init_farm"]()
tree_farmer["maintain_farm"]()

if num_items(Items.Empty_Tank) == 0:
    trade(Items.Empty_Tank, 1000)

pumpkin_farm = create_farm(get_world_size(), get_world_size())

pumpkin_farmer = create_pumpkin_farmer(pumpkin_farm, my_drone, 0, 0)

pumpkin_farmer["init_farm"]()

iterations = 4

for iteration in range(iterations):
    pumpkin_farmer["maintain_farm"]()

clear()

sunflower_farm = create_farm(get_world_size(), get_world_size())
sunflower_farmer = create_sunflower_farmer(sunflower_farm, my_drone, 0, 0)

sunflower_farmer["init_farm"]()

iterations = 100

for iteration in range(iterations):
    sunflower_farmer["maintain_farm"]()
        

#maze_plan = create_maze_plan(my_drone, my_farm)

#for maze_count in range(10):
#    maze_plan["do_create_maze"]()
#    maze_plan["execute_plan"](20)

# harvest()