from __builtins__ import *

from Utility import *
from drone import *
from graph import *
from farm import *
from farm import *
from maze import *
from carrot_farmer import *
from dual_farmer import *
from pumpkin_farmer import *
from sunflower_farmer import *
from sort import *

MAX_PRIORITY = 15
NO_PRIORITY = 0

if num_items(Items.Empty_Tank) == 0:
    trade(Items.Empty_Tank, 1000)

farm_size = get_world_size()
my_farm = create_farm(farm_size, farm_size)

my_drone = create_drone()

def single_farm_demo():
    clear()
    create_grass_farmer(my_drone, farm_size, farm_size, 0, 0)["init_farm"]()

    clear()
    bush_farm = create_bush_farmer(my_drone, farm_size, farm_size, 0, 0)
    bush_farm["init_farm"]()
    bush_farm["maintain_farm"]()

    clear()
    carrot_farm = create_carrot_farmer(my_drone, farm_size, farm_size, 0, 0)
    carrot_farm["init_farm"]()
    carrot_farm["maintain_farm"]()

    clear()
    tree_farm = create_dual_farmer(my_drone, farm_size, farm_size, 0, 0, (Entities.Tree, Entities.Bush))
    tree_farm["init_farm"]()
    tree_farm["maintain_farm"]()
    tree_farm["maintain_farm"]()

    farmers_only = []
    
    farmers_only.append(create_pumpkin_farmer(my_farm, my_drone, 0, 0))
    farmers_only.append(create_sunflower_farmer(my_farm, my_drone, 0, 0))

    for farmer in farmers_only:
        clear()
        farmer["init_farm"]()

        for _ in range(3):
            result = farmer["maintain_farm"]()

            if result < 0:
                print("Farmer Failed")

                break

            if result > 0:
                wait_till(result)

def region_farm_demo():
    clear()

    regions = []
    region_width = farm_size / 2
    region_height = farm_size / 2
    pumpkin_farm = create_farm(region_width, region_height)
    sunflower_farm = create_farm(region_width, region_height)

    regions.append({ 0: 0, 1: create_sunflower_farmer(sunflower_farm, my_drone, 0, 0)}) # 0,0
    regions.append({ 0: 0, 1: create_dual_farmer(my_drone, region_width, region_height, 0, region_height, (Entities.Tree, Entities.Bush))}) #0, 1
    regions.append({ 0: 0, 1: create_pumpkin_farmer(pumpkin_farm, my_drone, region_width, 0)}) # 1,0
    regions.append({ 0: 0, 1: create_carrot_farmer(my_drone, region_width, region_height, region_width, region_height)}) # 1, 1
 
    for region in regions:
        farmer = region[1]
        region[0] = farmer["init_farm"]()

    for _ in range(3):
        TopDownMergeSort(regions, 0)

        for region in regions:
            wait_time = region[0]
            farmer = region[1]

            if wait_time > get_time():
                wait_till(wait_time)

            result = farmer["maintain_farm"]()

            if result < 0:
                print("Farmer Failed")

                break

def maze_demo():
    clear()
    maze_plan = create_maze_plan(my_drone, my_farm)

    for _ in range(10):
        maze_plan["do_create_maze"]()
        maze_plan["execute_plan"](5)

    harvest()

single_farm_demo()
region_farm_demo()
maze_demo()