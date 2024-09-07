def create_maze_plan():

	def do_prepare(is_last):
		if get_ground_type() != Grounds.Soil:
			till()
	
	def do_maintenance(is_last):
		while (get_entity_type() == Entities.Bush):
			use_item(Items.Fertilizer)
			trade(Items.Fertilizer)
		use_item(Items.Water_Tank)
			
	def do_plant(is_last):
		plant(Entities.Bush)
		
	def do_maze(is_last):
		print("HEllo!")
		
	return [do_prepare, do_plant, do_maintenance, do_maze]

def do_create_maze():
	clear()
	
	if get_ground_type() != Grounds.Turf:
		till()
	
	plant(Entities.Bush)
	
	while not can_harvest():
		pass
		
	do_a_flip()
	
	while get_entity_type() == Entities.Bush:
		if num_items(Items.Fertilizer) == 0:
			trade(Items.Fertilizer, 100)
		use_item(Items.Fertilizer)
				
def do_complete_maze():
	last = None
	
	def do_moves(directions):
		success = False
		
		for index in range(len(directions)):
			direction = directions[index]
			success = move(direction)
			if success:
				moved = direction
				break
				
		return direction
	
	while True:
		if get_entity_type() == Entities.Treasure:
			harvest()
			break

		if last == North:
			last = do_moves([West, North, East, South])
		elif last == East:
			last = do_moves([North, East, South, West])
		elif last == South:
			last = do_moves([East, South, West, North])
		elif last == West:
			last = do_moves([South, West, North, East])
		else:
			last = do_moves([North, West, East, South])
			
do_complete_maze()

		