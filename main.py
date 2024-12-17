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
single_farmer_demo()
region_demo()

# maze_demo()