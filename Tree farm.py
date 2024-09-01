def doTreeWork():
	if can_harvest():
		harvest()
	
	plant(Entities.Tree)

	use_item(Items.Water_Tank)