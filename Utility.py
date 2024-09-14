def create_matrix(size, num_dims):		
	matrix = []
	
	for _ in range(size):
		if num_dims <= 1:
			matrix.append(None)
		else:
			matrix.append(create_matrix(size, num_dims - 1))
	
	return matrix

def create_plot(entity_type):
    plot = {
        "entity_type": entity_type
    }

    return plot

def apply_entity_type(board, x1, y1, x2, y2, entity_type, fill_test):
	for xIndex in range(x1, x2):
		for yIndex in range(y1,y2):
			if fill_test(xIndex, yIndex):
				board[xIndex][yIndex] = entity_type

def hash_edge(edge):
	hash_coord(edge)

def hash_coord(coord):
	return hash_cantor(coord[0], coord[1])

def hash_cantor(x, y):
	n = ((x + y) * (x + y + 1) / 2) + y

	return n

def get_distance(coord1, coord2):
	x1 = coord1[0]
	x2 = coord2[0]
	y1 = coord1[1]
	y2 = coord2[1]

	distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

	return distance