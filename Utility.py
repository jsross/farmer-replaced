def create_matrix(size, create_item):
	matrix = []

	for x_index in range(size):
		matrix.append([])
		for y_index in range(size):
			matrix[x_index].append(create_item(x_index, y_index))
	
	return matrix

def create_matrix_with_default(size, default):
	matrix = []

	for x_index in range(size):
		matrix.append([])
		for _ in range(size):
			matrix[x_index].append(default)
	
	return matrix

def find_in_matrix(matrix, test_func):
	items = []
	size = len(matrix)
	for x_index in range(size):
		for y_index in range(size):
			item = matrix[x_index][y_index]

			if test_func(item, x_index, y_index):
				items.append(item)
				
	return items

def find_in_array(array, test_func):
	items = []

	for index in range(len(array)):
		item = array[index]

		if test_func(item, index):
			items.append(item)
	
	return items