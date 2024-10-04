from __builtins__ import *

from Utility import *
from drone import *
from a_star import *
from graph import *
from farm import *
from game_board import *
from wall_follow_strategy import *
from maze import *

harvest()
clear()

current_game_board = create_game_board(get_world_size())
current_graph = create_graph()

current_game_board["add_connections"](current_graph)

my_drone = create_drone(current_graph,current_game_board)
my_drone["set_property"]("update_graph_on_success", False)

farm_plan = create_farm_plan(my_drone, current_game_board)
# farm_plan["apply_normal_plan"]()
clear()
#farm_plan["apply_maze_plan"]()
farm_plan["execute_plan"](0)

maze_plan = create_maze_plan(my_drone, current_graph, current_game_board)

maze_plan["do_create_maze"]()
maze_plan["execute_plan"](50)

harvest()
     


