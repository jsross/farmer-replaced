def create_wheat_plan():

	def do_harvest(is_last):
		if can_harvest():
			harvest()

	def do_prepare(is_last):
		if get_ground_type() != Grounds.Turf:
			till()
			
	return [do_harvest, do_prepare]