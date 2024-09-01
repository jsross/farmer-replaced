def doWoodWork(length, x, y):
	if can_harvest():
		harvest()
	
	if (x + (y % 2)) % 2 == 0:
		plant(Entities.Tree)

	use_item(Items.Water_Tank)