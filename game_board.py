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
    
    def get_neighbor(coord, direction):
        neighbor_x = 0
        neighbor_y = 0

        if direction == North:
            neighbor_x = coord[0]
            neighbor_y = coord[1] + 1
        elif direction == East:
            neighbor_x = coord[0] + 1
            neighbor_y = coord[1]
        elif direction == South:
            neighbor_x = coord[0]
            neighbor_y = coord[1] - 1
        elif direction == West:
            neighbor_x = coord[0] - 1
            neighbor_y = coord[1]

        if neighbor_x < 0 or neighbor_x >= size:
            return None

        if neighbor_y < 0 or neighbor_y >= size:
            return None
        
        return (neighbor_x, neighbor_y)
    
    initialize_nodes()

    new_game_board = {
        "get_node": get_node,
        "get_neighbor": get_neighbor
    }

    return new_game_board
                     
def create_node(coord):
    new_node = {
        "coord": coord,
    }
    
    return new_node