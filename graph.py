def create_graph(size):
    matrix = create_matrix(size, 2)

    def get_size():
         return size

    def initialize_nodes():
        for index_x in range(size):
            for index_y in range(size):
                coords = (index_x, index_y)
                matrix[index_x][index_y] = create_node(coords)
    
    def translate(coord):
         if coord < 0:
              return size + coord
         elif coord >= size:
              return coord % size
         else:
              return coord

    def get_node(coord):
        translated_x = translate(coord[0])
        translated_y = translate(coord[1])

        return matrix[translated_x][translated_y]
    
    def reset_connections():
        for index_x in range(size):
            for index_y in range(size):
                node = matrix[index_x][index_y]

                node["neighbors"][North] = get_node((index_x,index_y + 1))
                node["neighbors"][East] = get_node((index_x + 1,index_y))
                node["neighbors"][South] = get_node((index_x,index_y - 1))
                node["neighbors"][West] = get_node((index_x,index_y + 1))
    
    initialize_nodes()
	reset_connections()
    
    graph = {
        "reset_connections": reset_connections,
        "get_node": get_node,
        "get_size": get_size
    }

    return graph

def create_matrix(size, num_dims):		
	matrix = []
	
	for _ in range(size):
		if num_dims <= 1:
			matrix.append(None)
		else:
			matrix.append(create_matrix(size, num_dims - 1))
	
	return matrix

def create_node(coord):
    new_node = {
        "coord": coord,
        "neighbors" : {
            North: None,
            East: None,
            South: None,
            West: None
        }    
    }
    
    return new_node   