from __builtins__ import *

from Utility import *
from drone import *
from graph import *
from maze_navigator import *
from carrot_farmer import *
from dual_farmer import *
from pumpkin_farmer import *
from sunflower_farmer import *
from catcus_farmer import *
from sort import *

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
    
    farm_plans = []

    farm_plans.append((create_sunflower_farmer(world_size, world_size, 0, 0),2)) # 0,0
    farm_plans.append((create_cactus_farmer(world_size, world_size, 0, 0), 20)) # 0,0
    
    for _ in range(1):
        for farm_plan in farm_plans:
            farmer = farm_plan[0]
            iterations = farm_plan[1]

            clear()

            farmer["init_farm"]()

            for _ in range(iterations):
                result = farmer["maintain_farm"]()

                if result < 0:
                    print("Farmer Failed")

                    break

                if result > 0:
                    wait_till(result)
    
    clear()
    
    # maze_navigator = create_maze_navigator() 

    # for _ in range(10):
    #    maze_navigator["do_create_maze"]()
    #    maze_navigator["execute_plan"](20)
    #    harvest()

do_work()