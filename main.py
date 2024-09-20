from __builtins__ import *
from Utility import *
from drone import *
from a_star import *
from graph import *
from maze import *
from farm import *

harvest()

clear()

seedsNeeded = [0,0,0]

drone = create_drone()
game_board = create_graph(get_world_size())

do_create_maze()
do_complete_maze(game_board)

while True:
	next_coords = measure()

	while get_entity_type() == Entities.Treasure:
		use_item(Items.Fertilizer)

	treasure_found = False
            
	current_path = a_star(game_board, drone["get_coords"](), next_coords)
    
	if current_path != None:
		print("A Star")
		treasure_found = drone["follow_path"](current_path)
	
	if not treasure_found:
		print("Scan")
		do_complete_maze(game_board)
	
## do_complete_maze(game_board)



if current_path != None:
	drone["follow_path"](current_path)

     
#current_path = a_star(game_board, (4,5),(9,2))

#if current_path != None:
#	drone["follow_path"](current_path)

drone["register_entity_handler"](Entities.Bush, handle_bush)
# drone["register_entity_handler"](Entities.Cactus, handle_cactus)
drone["register_entity_handler"](Entities.Carrots, handle_carrot)
drone["register_entity_handler"](Entities.Grass, handle_grass)
#drone["register_entity_handler"](Entities.Hedge, handle_hedge)
drone["register_entity_handler"](Entities.Pumpkin, handle_pumpkin)
drone["register_entity_handler"](Entities.Sunflower, handle_sunflower)
drone["register_entity_handler"](Entities.Tree, handle_tree)

farm_plan = create_farm_plan()

def do_scan_farm():
    for xIndex in range(0, get_world_size()):
        for yIndex in range(0, get_world_size()):
            drone["go_to"]((xIndex,yIndex))
            drone["scan"]()
            drone["farm"]()

#demo_action_plan = []

#while True:
#	do_scan_farm()
#    drone["execute_action_plan"](demo_action_plan)