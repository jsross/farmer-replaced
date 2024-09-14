clear()

seedsNeeded = [0,0,0]

drone = create_drone()
game_board = create_graph(get_world_size())

current_path = a_star(game_board, (0,1),(5,5))
drone["follow_path"](current_path)
current_path = a_star(game_board, (5,5),(9,3))
drone["follow_path"](current_path)

farm_plan = create_matrix(get_world_size(),2)

def fill_strategy_checkerd(x,y):
	rem = y % 2
	fill = (x - rem ) % 2 == 0
	return fill

def fill_strategy_checkerd_alt(x,y):
	rem = y % 2
	fill = (x - rem ) % 2 == 1
	
	return fill
	
def fill_strategy_solid(x,y):
	return True

apply_entity_type(farm_plan, 0, 0,get_world_size(), get_world_size(), Entities.Grass, fill_strategy_solid)
apply_entity_type(farm_plan, 0, 0,get_world_size() / 2, get_world_size() / 2, Entities.Tree,fill_strategy_checkerd)
apply_entity_type(farm_plan, 0, 0,get_world_size() / 2, get_world_size() / 2, Entities.Sunflower,fill_strategy_checkerd_alt)
apply_entity_type(farm_plan, get_world_size() / 2, get_world_size() / 2, get_world_size(), get_world_size(), Entities.Carrots,fill_strategy_solid)

drone["register_entity_handler"](Entities.Bush, handle_bush)
# drone["register_entity_handler"](Entities.Cactus, handle_cactus)
drone["register_entity_handler"](Entities.Carrots, handle_carrot)
drone["register_entity_handler"](Entities.Grass, handle_grass)
#drone["register_entity_handler"](Entities.Hedge, handle_hedge)
drone["register_entity_handler"](Entities.Pumpkin, handle_pumpkin)
drone["register_entity_handler"](Entities.Sunflower, handle_sunflower)
drone["register_entity_handler"](Entities.Tree, handle_tree)

def do_scan_farm():
    for xIndex in range(0, get_world_size()):
        for yIndex in range(0, get_world_size()):
            drone["go_to"]((xIndex,yIndex))
            drone["scan"]()
            drone["farm"]()

demo_action_plan = [do_scan_farm]

while True:
    drone["execute_action_plan"](demo_action_plan)