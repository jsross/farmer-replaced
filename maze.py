from __builtins__ import *

def do_create_maze():
	clear()
	
	if get_ground_type() != Grounds.Turf:
		till()
	
	plant(Entities.Bush)
	
	while not can_harvest():
		pass
		
	while get_entity_type() == Entities.Bush:
		if num_items(Items.Fertilizer) == 0:
			trade(Items.Fertilizer, 100)
		use_item(Items.Fertilizer)
				
def do_complete_maze(graph):
	last = None
	
	def do_moves(directions):
		success = False
		
		for index in range(len(directions)):
			direction = directions[index]
			success = move(direction)

			if success:
				break
			
			current_coord = (get_pos_x(), get_pos_y())
			graph["remove_connection"](current_coord, direction)
				
		return direction
	
	while True:
		if get_entity_type() == Entities.Treasure:
			return True

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
			

		