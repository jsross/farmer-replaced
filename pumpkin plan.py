def create_pumpkin_plan():

	def do_harvest(isLast):
		if isLast and seedsNeeded[0] == 0 and can_harvest():
			harvest()

	def do_prepare(isLast):
		if get_ground_type() != Grounds.Soil:
			till()
	
	def do_maintenance(isLast):
		use_item(Items.Fertilizer)
		use_item(Items.Water_Tank)
			
	def do_plant(isLast):
		while not can_harvest():
			if get_entity_type() == None:
				if plant(Entities.Pumpkin):
					seedsNeeded[0] = seedsNeeded[0] + 1
		
	return [do_prepare, do_plant, do_maintenance, do_harvest]
		
		