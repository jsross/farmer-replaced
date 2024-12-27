from __builtins__ import *

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

def select_coords_with_properties(matrix, properties):
    def test_func(item, _x, _y):
        for property_key in properties:
            if not item[property_key] == properties[property_key]:
                return False
        
        return True

    return select_coords_from_matrix(matrix, test_func)

def calculate_dist(x_1, y_1, x_2, y_2):
    return abs(x_1 - x_2) + abs(y_1 - y_2)

def get_neighbor(x, y, direction):
    start_op_count = get_tick_count()
    size = get_world_size()

    neighbor_x = 0
    neighbor_y = 0

    if direction == North:
        neighbor_x = x
        neighbor_y = y + 1
    elif direction == East:
        neighbor_x = x + 1
        neighbor_y = y
    elif direction == South:
        neighbor_x = x
        neighbor_y = y - 1
    elif direction == West:
        neighbor_x = x - 1
        neighbor_y = y
		
    if neighbor_x < 0 or neighbor_x >= size:
        return None
	
    if neighbor_y < 0 or neighbor_y >= size:
        return None

    neighbor_coords = (neighbor_x, neighbor_y)
    
    quick_print("get_neighbor: ", get_tick_count() - start_op_count)

    return neighbor_coords

def get_neighbors(x, y):
    size = get_world_size()
    
    neighbors = [
        (x, (y + 1) % size), # North
        ((x + 1) % size, y), # East
        (x, (y - 1) % size), # South
        ((x - 1) % size, y)  # West
    ]

    return neighbors

def get_distance(coords_1, coords_2):
    # start_op_count = get_tick_count()
    
    if coords_1 == None or coords_2 == None:
        quick_print("Bad Arguments: coords_1 and coords_2 are both required")

        exit()

    distance = calculate_dist(coords_1[0], coords_1[1], coords_2[0],coords_2[1])

    # quick_print("get_distance: ", get_tick_count() - start_op_count)

    return distance

def swap_entries(matrix, coord_1, coord_2):
	value_1 = matrix[coord_1[0]][coord_1[1]]
	value_2 = matrix[coord_2[0]][coord_2[1]]
	
    matrix[coord_1[0]][coord_1[1]] = value_2
    matrix[coord_2[0]][coord_2[1]] = value_1