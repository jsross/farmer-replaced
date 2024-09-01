		
def doPumpkinWork(length, x, y):
	planted = False
	
	if can_harvest():
		harvest()
	
	if get_ground_type() != Grounds.Soil:
		till()
		
	planted = plant(Entities.Pumpkin)
	use_item(Items.Water_Tank)
	
	return planted