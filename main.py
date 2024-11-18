from __builtins__ import *

from Utility import *
from drone import *
from a_star import *
from graph import *
from farm import *
from game_board import *
from wall_follow_strategy import *
from maze import *

clear()

current_game_board = create_game_board(get_world_size())

my_drone = create_drone()

if num_items(Items.Empty_Tank) == 0:
    trade(Items.Empty_Tank, 1000)

farmer = create_farmer(my_drone, current_game_board)
farmer["do_work"](100)

# current_game_board["add_connections"](current_graph)

#maze_plan = create_maze_plan(my_drone, current_game_board)

#for maze_count in range(10):
#    maze_plan["do_create_maze"]()
#    maze_plan["execute_plan"](20)

#harvest()