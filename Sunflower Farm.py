def create_sunflower_plan():
	def do_harvest(is_last):
		if can_harvest():
			harvest()

	def do_prepare(is_last):
		if get_ground_type() != Grounds.Soil:
			till()
	
	def do_maintenance(is_last):
		use_item(Items.Fertilizer)
		use_item(Items.Water_Tank)
			
	def do_plant(is_last):
		plant(Entities.Sunflower)
		
	return [do_prepare, do_plant, do_maintenance, do_harvest]
	