def doWheatWork(length, x, y):
	if can_harvest():
		harvest()
		
	if get_ground_type() != Grounds.Turf:
		till()
	
	return False
		
		
		