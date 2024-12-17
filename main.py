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
my_farm = create_farm(farm_size, farm_size)

my_drone = create_drone()

basic_demo()
farmer_demo()
region_demo()

#maze_demo()

def do_work():
    print("Do Work Demo")
    world_size = get_world_size()

    clear()
    
    farm_plans = []
    farm_plans.append((create_grass_farmer(world_size, world_size, 0, 0),1))
    farm_plans.append((create_dual_farmer(world_size, world_size, 0, 0, (Entities.Tree, Entities.Bush)),10))
    
    for _ in range(10):
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

# do_work()