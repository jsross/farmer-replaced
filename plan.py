def create_plan_matrix():

	planMatrix = create_matrix(get_world_size(),2)
	
	#build_pumpkin_farm(planMatrix, 0, 0, get_world_size(), get_world_size())
	
	# build_carrot_farm(planMatrix, 0, 0, get_world_size(), get_world_size())
	# build_tree_farm(planMatrix, 0, 0, get_world_size(), get_world_size())
	
	build_hay_farm(planMatrix, 0, 0, get_world_size(), get_world_size())
	#build_sunflower_farm(planMatrix, get_world_size()-1, get_world_size()-1, get_world_size(), get_world_size())
	# build_pumpkin_farm(planMatrix, 0, 0, get_world_size() - 2, get_world_size() - 2)
	build_maze_plan(planMatrix, 0, 0, 1, 1)
	
	return planMatrix
	
def build_hay_farm(matrix, x1, y1, x2, y2):
	apply_plan(matrix, x1, y1, x2, y2, create_wheat_plan)

def build_tree_farm(matrix, x1, y1, x2, y2):
	for xIndex in range(x1, x2):
		for yIndex in range(y1,y2):
			if (xIndex + (yIndex % 2)) % 2 == 0:
				matrix[xIndex][yIndex] = create_tree_plan()

def apply_plan(matrix, x1, y1, x2, y2, create_plan):
	x_range = range(x1, x2)
	x_range_len = len(x_range)
	y_range = range(y1, y2)
	y_range_len = len(y_range)
	plot_count = x_range_len * y_range_len
	
	plan_count = 0
	
	for xIndex in range(x1, x2):
		for yIndex in range(y1,y2):
			is_last = True
			
			if plan_count < plot_count - 1:
				is_last = False
			
			matrix[xIndex][yIndex] = [create_plan(), is_last]
			
			plan_count += 1

def build_maze_plan(matrix, x1, y1, x2, y2):
	apply_plan(matrix, x1, y1, x2, y2, create_maze_plan)
				
def build_sunflower_farm(matrix, x1, y1, x2, y2):
	apply_plan(matrix, x1, y1, x2, y2, create_sunflower_plan)

def build_bush_farm(matrix, x1, y1, x2, y2):
	apply_plan(matrix, x1, y1, x2, y2, create_bush_plan)

def build_carrot_farm(matrix, x1, y1, x2, y2):
	apply_plan(matrix, x1, y1, x2, y2, create_carrot_plan)
		
def build_pumpkin_farm(matrix, x1, y1, x2, y2):
	return apply_plan(matrix, x1, y1, x2, y2, create_pumpkin_plan)
			




			