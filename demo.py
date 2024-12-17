from __builtins__ import *
from grass_farmer import *
from bush_farmer import *
from carrot_farmer import *
from tree_farmer import *
from pumpkin_farmer import *
from dual_farmer import *
from sunflower_farmer import *

def basic_demo():
    clear()

    world_size = get_world_size()

    for _ in range(2):
        handle_grass_farm(world_size, world_size, 0, 0)

    clear()

    init_bush_farm(world_size, world_size, 0, 0)

    for _ in range(1):
        maintain_bush_farm(world_size, world_size, 0, 0)

    clear()

    init_carrot_farm(world_size, world_size, 0, 0)

    for _ in range(2):
        maintain_carrot_farm(world_size, world_size, 0, 0)

    clear()

    init_tree_farm(world_size, world_size)

    for _ in range(2):
        maintain_tree_farm(world_size, world_size)

    clear()

    init_pumpkin_farm(world_size, world_size, 0, 0)

    pumpkin_matrix = create_matrix_with_default(world_size, world_size, False)

    for _ in range(10):
        maintain_pumpkin_farm(pumpkin_matrix, world_size, world_size, 0, 0)

    clear()

def single_farmer_demo():
    world_size = get_world_size()

    clear()
    create_grass_farmer(world_size, world_size, 0, 0)["init_farm"]()

    clear()
    
    bush_farm = create_bush_farmer(world_size, world_size, 0, 0)
    bush_farm["init_farm"]()
    bush_farm["maintain_farm"]()

    clear()
    carrot_farm = create_carrot_farmer(world_size, world_size, 0, 0)
    carrot_farm["init_farm"]()
    carrot_farm["maintain_farm"]()

    clear() 
    tree_farm = create_dual_farmer(world_size, world_size, 0, 0, (Entities.Tree, Entities.Bush))
    tree_farm["init_farm"]()
    tree_farm["maintain_farm"]()
    tree_farm["maintain_farm"]()

    farmers_only = []
    
    farmers_only.append(create_pumpkin_farmer(world_size, world_size, 0, 0))
    farmers_only.append(create_sunflower_farmer(world_size, world_size, 0, 0))

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

def region_demo():
    clear()

    world_size = get_world_size()

    regions = []
    region_width = world_size / 2
    region_height = world_size / 2

    regions.append({ 0: 0, 1: create_sunflower_farmer(region_width, region_height, 0, 0)}) # 0,0
    regions.append({ 0: 0, 1: create_dual_farmer(region_width, region_height, 0, region_height, (Entities.Tree, Entities.Bush))}) #0, 1
    regions.append({ 0: 0, 1: create_pumpkin_farmer(region_width, region_height, region_width, 0)}) # 1,0
    regions.append({ 0: 0, 1: create_carrot_farmer(region_width, region_height, region_width, region_height)}) # 1, 1
 
    for region in regions:
        farmer = region[1]
        region[0] = farmer["init_farm"]()

    for _ in range(5): 
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