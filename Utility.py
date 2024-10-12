def create_matrix(size, create_item):
	matrix = []

	for x_index in range(size):
		matrix.append([])
		for y_index in range(size):
			matrix[x_index].append(create_item(x_index, y_index))
	
	return matrix

