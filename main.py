clear()
seedsNeeded = [0,0,0]
plotCount = get_world_size() * get_world_size()

planMatrix = create_plan_matrix()

trade(Items.Pumpkin_Seed,plotCount)

def execute_plan(matrix):
	successCount = 0
	is_last = False
	
	for yIndex in range(get_world_size()):
		for xIndex in range(get_world_size()):
			actions = matrix[xIndex][yIndex][0]
			is_last = matrix[xIndex][yIndex][1]
			
			execute_actions(actions, is_last)
				
			move(East)			
		move(North)
	
	return successCount
	
def execute_actions(actions, is_last):
	for action in actions:
		action(is_last)

while True:
	
	if num_items(Items.Carrot_Seed) == 0:
		trade(Items.Carrot_Seed,plotCount)
		
	if num_items(Items.Sunflower_Seed) == 0:
		trade(Items.Sunflower_Seed, plotCount)

	if num_items(Items.Fertilizer) == 0:
		trade(Items.Fertilizer, plotCount)
		
	execute_plan(planMatrix)
	
	trade(Items.Pumpkin_Seed,seedsNeeded[0])
	seedsNeeded[0] = 0