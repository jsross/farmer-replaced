from __builtins__ import *
from Utility import *

def create_graph(size):
    matrix = create_matrix(size, 2)

    def get_size():
         return size

    def initialize_nodes():
        for index_x in range(size):
            for index_y in range(size):
                coords = (index_x, index_y)
                matrix[index_x][index_y] = create_node(coords)
    
    def get_node(coord):
        return matrix[coord[0]][coord[1]]
    
    def reset_connections():
        for index_x in range(size):
            for index_y in range(size):
                node = matrix[index_x][index_y]

                if index_y + 1 < size:
                    node["neighbors"][North] = get_node((index_x, index_y + 1))

                if index_x + 1 < size:
                    node["neighbors"][East] = get_node((index_x + 1, index_y))

                if index_y - 1 >= 0:
                    node["neighbors"][South] = get_node((index_x, index_y - 1))

                if index_x - 1 >= 0:
                    node["neighbors"][West] = get_node((index_x - 1, index_y))

    def remove_connection(coord, direction):
        node = get_node(coord)
		
        if not direction in node["neighbors"]:
            return
        
        neighbor = node["neighbors"][direction]

        node["neighbors"].pop(direction)

        if direction == North:
            neighbor["neighbors"].pop(South)
        elif direction == East:
            neighbor["neighbors"].pop(West)
        elif direction == South:
            neighbor["neighbors"].pop(North)
        elif direction == West:
            neighbor["neighbors"].pop(East)
	    
    initialize_nodes()
    reset_connections()
    
    graph = {
        "reset_connections": reset_connections,
        "get_node": get_node,
        "get_size": get_size,
        "remove_connection": remove_connection
    }

    return graph

def create_node(coord):
    new_node = {
        "coord": coord,
        "neighbors" : {
        }
    }
    
    return new_node