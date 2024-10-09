def create_matrix(size, create_item):
	matrix = []

	for x_index in range(size):
		matrix.append([])
		for y_index in range(size):
			matrix[x_index].append(create_item(x_index, y_index))
	
	return matrix

def create_plot(entity_type):
    plot = {
        "entity_type": entity_type
    }

    return plot

def fill_strategy_checkerd(x,y):
	rem = y % 2
	fill = (x - rem ) % 2 == 0
	return fill

def fill_strategy_checkerd_alt(x,y):
	rem = y % 2
	fill = (x - rem ) % 2 == 1
	
	return fill
	
def fill_strategy_solid(x,y):
	return True