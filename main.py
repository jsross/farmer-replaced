from __builtins__ import *

from Utility import *
from drone import *
from graph import *
from carrot_farmer import *
from pumpkin_farmer import *
from sunflower_farmer import *
from catcus_farmer import *
from maze_farmer import *
from dino_farmer import *
from sort import *
from poly_farmer import *

# clear()

# harvest()
# harvest()
# harvest()
# harvest()
# harvest()

# while True:
#    if can_harvest():
#        harvest()

# while True:
#    if can_harvest():
#        harvest()
#    plant(Entities.Bush)
#    move(North)

MAX_PRIORITY = 15
NO_PRIORITY = 0

farm_size = get_world_size()

#basic_demo()
#farmer_demo()
#region_demo()
#maze_demo()

def do_work():
    print("Do Work Demo")
    world_size = get_world_size()

    clear()
    
    farmers = []


    farmers.append(create_maze_farmer(512000))
    unlock(Unlocks.Dinosaurs)

    # farmers.append(create_grass_farmer(world_size, world_size, 0, 0, 1000)) # 0,0
    # farmers.append(create_bush_farmer(world_size, world_size, 0, 0, 1000))
    # farmers.append(create_carrot_farmer(world_size, world_size, 0, 0, 1000))
    # farmers.append(create_tree_farmer(world_size, world_size, 0, 0, 1000))
    # farmers.append(create_pumpkin_farmer(world_size, world_size, 0, 0, 100000))
    # farmers.append(create_sunflower_farmer(world_size, world_size, 0, 0, num_items(Items.Power) + 20000))
    # farmers.append(create_poly_farmer())
    #farmers.append(create_cactus_farmer(world_size, world_size, 0, 0, 1000))
    #farmers.append(create_dino_farmer(1000))
    
    #farmers.append(create_maze_farmer(256000))

    
    
    for farmer in farmers:
        clear()

        result = farmer()

        while result != None:
            status = result["status"]
            next_pass = result["next_pass"]
            delay = result["delay"]
            
            if status < 0:
                print("Farmer Failed")

                break

            if delay > 0:
                wait_till(get_time() + delay)

            result = next_pass()
    
    clear()
    
    # maze_navigator = create_maze_navigator()

    # for _ in range(10):
    #    maze_navigator["do_create_maze"]()
    #    maze_navigator["execute_plan"](20)
    #    harvest()

do_work()