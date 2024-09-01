def doGrassWork():
	planted = False
	
	if can_harvest():
		harvest()
	
	if get_ground_type() != Grounds.Turf:
		till()
	
	planted = plant(Entities.Grass)
	use_item(Items.Water_Tank)
	