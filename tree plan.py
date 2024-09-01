def create_tree_plan():

	def do_harvest(is_last):
		if can_harvest():
			harvest()

	def do_prepare(is_last):
		if get_ground_type() != Grounds.Soil:
			till()
			
	def do_plant(is_last):
		plant(Entities.Tree)
		use_item(Items.Fertilizer)
		use_item(Items.Water_Tank)
	
	return [do_harvest, do_prepare, do_plant]