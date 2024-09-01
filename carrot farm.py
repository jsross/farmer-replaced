		
def doCarrotWork(length, x, y):
	plantable = False
	
	if can_harvest():
		harvest()
		plantable = True
	
	if get_ground_type() != Grounds.Soil:
		till()
		plantable = True
		
	plant(Entities.Carrots)
	use_item(Items.Water_Tank)
	
	return plantable
		
		