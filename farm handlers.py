		
def handle_pumpkin(x,y):
	if get_ground_type() != Grounds.Soil:
		till()
		
	if can_harvest():
		harvest()

	planted = plant(Entities.Pumpkin)

	use_item(Items.Water_Tank)

def handle_carrot(x,y):
	plot = game_board["get_node"]((x,y))
	
	if plot["can_harvest"]:
		harvest()
		plot["can_harvest"] = False
		plot["entity_type"] = None
	
	if plot["ground_type"] != Grounds.Soil:
		till()
		plot["ground_type"] = Grounds.Soil
		plot["can_harvest"] = False
		plot["entity_type"] = None

	if(num_items(Items.Carrot_Seed) >= 0):
		trade(Items.Carrot_Seed, get_world_size() * get_world_size())

	if plot["entity_type"] != Entities.Carrots:
		if plant(Entities.Carrots):
			plot["entity_type"] = Entities.Carrots
			plot["can_harvest"] = False

	use_item(Items.Fertilizer)
	use_item(Items.Water_Tank)

def handle_grass(x,y):
	planted = False
	
	if can_harvest():
		harvest()
	
	if get_ground_type() != Grounds.Turf:
		till()
	
	planted = plant(Entities.Grass)
	use_item(Items.Water_Tank)

def handle_bush(x, y):

	if get_ground_type() != Grounds.Turf:
		till()

	if can_harvest():
		harvest()
	
	plant(Entities.Bush)

	use_item(Items.Fertilizer)
	use_item(Items.Water_Tank)

def handle_sunflower(x,y):
	if can_harvest():
		harvest()

	if get_ground_type() != Grounds.Soil:
		till()

	use_item(Items.Fertilizer)
	use_item(Items.Water_Tank)
		
	plant(Entities.Sunflower)

def handle_tree(x,y):
	plot = game_board["get_node"]((x,y))
	
	if plot["can_harvest"]:
		harvest()
		plot["can_harvest"] = False

	if get_ground_type() != Grounds.Soil:
		till()

	plant(Entities.Tree)
	use_item(Items.Fertilizer)
	use_item(Items.Water_Tank)