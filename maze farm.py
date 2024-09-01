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