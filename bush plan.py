def create_bush_plan():

	def do_harvest(is_last):
		if get_entity_type() == Entities.Hedge:
			return
			
		if can_harvest():
			harvest()

	def do_prepare(is_last):
		if get_ground_type() != Grounds.Turf:
			till()
			
	def do_plant(is_last):
		plant(Entities.Bush)
		
	def do_maintenance(is_last):
		use_item(Items.Fertilizer)
		use_item(Items.Water_Tank)
		
	return [do_maintenance, do_harvest, do_prepare,do_plant]
	