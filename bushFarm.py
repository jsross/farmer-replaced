def doBushWork():
	planted = False
	
	if can_harvest():
		harvest()
		
	planted = plant(Entities.Bush)
	use_item(Items.Water_Tank)
	