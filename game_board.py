from __builtins__ import *
from Utility import *

def create_game_board(size):
    matrix = create_matrix(size, 2)

    def initialize_nodes():
        for index_x in range(size):
            for index_y in range(size):
                coords = (index_x, index_y)
                matrix[index_x][index_y] = create_node(coords)
    
    def get_node(coord):
        return matrix[coord[0]][coord[1]]
    
    def get_neighbor(x, y, direction):
        start_op_count = get_op_count()

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

        if (neighbor_x < 0 or neighbor_x >= size) or (neighbor_y < 0 or neighbor_y >= size):
            quick_print("get_neighbor: ", get_op_count() - start_op_count)
            return None
        
        quick_print("get_neighbor: ", get_op_count() - start_op_count)

        return (neighbor_x, neighbor_y)
    
    def add_connections(graph):
        graph_add_edge = graph["add_edge"]

        for x_index in range(size):
            for y_index in range(size):
                current_coords = (x_index, y_index)

                #Add East Neighbor
                if x_index < size - 1:
                    graph_add_edge(current_coords, (x_index + 1, y_index))

                #Add West Neighbor
                if x_index > 0:
                    graph_add_edge(current_coords, (x_index - 1, y_index))
                
                #Add North Neighbor
                if y_index < size - 1:
                    graph_add_edge(current_coords, (x_index, y_index+1))

                #Add South Neighbor
                if y_index > 0:
                    graph_add_edge(current_coords, (x_index, y_index-1))
                
                
    initialize_nodes()



    new_game_board = {
        "get_node": get_node,
        "get_neighbor": get_neighbor,
        "add_connections": add_connections
    }

    return new_game_board
                     
def create_node(coord):
    new_node = {
        "coord": coord,
    }
    
    return new_node