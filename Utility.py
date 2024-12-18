def create_array(length, default):
	array = []

	for _ in range(length):
		array.append(default)
	
	return array

def create_matrix(width, height, create_item):
	matrix = []

	for x_index in range(width):
		matrix.append([])
		for y_index in range(height):
			matrix[x_index].append(create_item(x_index, y_index))
	
	return matrix

def create_matrix_with_default(width, height, default):
	matrix = []

	for x_index in range(width):
		matrix.append([])
		for _ in range(height):
			matrix[x_index].append(default)
	
	return matrix

def create_matrix_with_default_object(width, height, default):
	matrix = []

	for x_index in range(width):
		matrix.append([])
		for _ in range(height):
			matrix[x_index].append(dict(default))
	
	return matrix

def copy_array(src_array, dest_array):
	count = len(src_array)

	for index in range(count):
		dest_array[index] = src_array[index]

def find_in_matrix(matrix, test_func):
	items = []
	width = len(matrix)
	for x_index in range(width):
		height = len(x_index[x_index])
		for y_index in range(height):
			item = matrix[x_index][y_index]

			if test_func(item, x_index, y_index):
				items.append(item)

	return items

def find_first_value_in_matrix(matrix, value):
	width = len(matrix)

	for x_index in range(width):
		height = len(matrix[x_index])

		for y_index in range(height):
			item = matrix[x_index][y_index]

			if item == value:
				return (x_index, y_index)
	
	return None

def select_coords_from_matrix(matrix, test_func):
	coords = []
	width = len(matrix)

	for x_index in range(width):
		height = len(matrix[x_index])
		for y_index in range(height):
			item = matrix[x_index][y_index]

			if test_func(item, x_index,y_index):
				coords.append((x_index, y_index))
	
	return coords

def select_coords_from_matrix_with_value(matrix, value):
	coords = []
	width = len(matrix)

	for x_index in range(width):
		height = len(matrix[x_index])
		for y_index in range(height):
			item = matrix[x_index][y_index]

			if item == value:
				coords.append((x_index, y_index))
	
	return coords

def find_in_array(array, test_func):
	items = []

	for index in range(len(array)):
		item = array[index]

		if test_func(item, index):
			items.append(item)
	
	return items

def select_object_from_array(array, properties):
	def test_func(item, _):
		for key in properties:
			if key not in item:
				return False
			if item[key] != properties[key]:
				return False
			
			continue

		return True
	
	return find_in_array(array, test_func)

def select_prop_from_matrix(matrix, prop_key, test_func):
	results = []
	size = len(matrix)

	for x_index in range(size):
		for y_index in range(size):
			item = matrix[x_index][y_index]

			if test_func(item, x_index, y_index):
				results.append(item[prop_key])
				
	return results

def select_from_matrix(matrix, coords_1, coords_2):
	items = []

	for x_index in range(coords_1[0], coords_2[0]):
		for y_index in range(coords_1[1], coords_2[1]):
			items.append(matrix[x_index][y_index])
				
	return items

def select_coords_with_properties(matrix, properties):
        def test_func(item, _x, _y):
            for property_key in properties:
                if not item[property_key] == properties[property_key]:
                    return False
            
            return True

        return select_coords_from_matrix(matrix, test_func)

def merge(target, source):
	for key in source:
		target[key] = source[key]

def wait_till(timestamp):
	while True:
		current_timestamp = get_time()

		if current_timestamp > timestamp:
			break
