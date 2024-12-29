from __builtins__ import *
from grass_farmer import *
from bush_farmer import *
from carrot_farmer import *
from tree_farmer import *
from pumpkin_farmer import *
from dual_farmer import *
from sunflower_farmer import *
from maze_navigator import *

def basic_demo():
    print("Basic Demo")
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

    for _ in range(5):
        maintain_pumpkin_farm(pumpkin_matrix, world_size, world_size, 0, 0)

    clear()

def farmer_demo():
    print("Farmer Demo")
    world_size = get_world_size()

    clear()
    
    farm_plans = []
    farm_plans.append((create_grass_farmer(world_size, world_size, 0, 0),1))
    farm_plans.append((create_bush_farmer(world_size, world_size, 0, 0), 2))
    farm_plans.append((create_carrot_farmer(world_size, world_size, 0, 0),2))
    farm_plans.append((create_dual_farmer(world_size, world_size, 0, 0, (Entities.Tree, Entities.Bush)),2))
    farm_plans.append((create_pumpkin_farmer(world_size, world_size, 0, 0),4))
    farm_plans.append((create_sunflower_farmer(world_size, world_size, 0, 0),1))
    
    for _ in range(2):
        for farm_plan in farm_plans:
            farmer = farm_plan[0]
            iterations = farm_plan[1]

            clear()

            farmer["execute_pass"]()

            for _ in range(iterations):
                result = farmer["maintain_farm"]()

                if result < 0:
                    print("Farmer Failed")

                    break

                if result > 0:
                    wait_till(result)
    

def region_demo():
    print("Region Demo")
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
        region[0] = farmer["execute_pass"]()

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
    print("Maze Demo")
    clear()
    maze_navigator = create_maze_navigator() 

    for _ in range(10):
        maze_navigator["do_create_maze"]()
        maze_navigator["execute_plan"](20)
        harvest()