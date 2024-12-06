from __builtins__ import *

from Utility import *
from drone import *
from graph import *
from farm import *
from farm import *
from maze import *

MAX_PRIORITY = 15
NO_PRIORITY = 0

clear()

my_farm = create_farm(get_world_size())
my_drone = create_drone(my_farm)

if num_items(Items.Empty_Tank) == 0:
    trade(Items.Empty_Tank, 1000)

farmer = create_farmer(my_drone, my_farm)
farmer["do_work"](50)

#maze_plan = create_maze_plan(my_drone, my_farm)

#for maze_count in range(10):
#    maze_plan["do_create_maze"]()
#    maze_plan["execute_plan"](20)

# harvest()