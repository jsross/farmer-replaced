from __builtins__ import *
from Utility import *

def create_game_board(size):
    matrix = create_matrix(size, create_node)

    def apply_property_value(coord_1, coord_2, property_name, property_value, fill_test):
        x1 = coord_1[0]
        y1 = coord_1[1]
        x2 = coord_2[0]
        y2 = coord_2[1]

        for x_index in range(x1, x2):
            for y_index in range(y1, y2):
                if fill_test(x_index, y_index):
                    plot = get_plot((x_index, y_index))
                    plot[property_name] = property_value

    def get_plot(coord):
        return matrix[coord[0]][coord[1]]
    
    def get_plots(expected_entity_type):

        def plot_test(plot, x_index, y_index):
            return plot["Expected_Entity_Type"] == expected_entity_type

        plots = find_in_matrix(matrix, plot_test)

        return plots
    
    def get_direction(src_coords, dest_coords):
        src_x = src_coords[0]
        src_y = src_coords[1]
        dest_x = dest_coords[0]
        dest_y = dest_coords[1]

        if dest_x > src_x:
            return East
        elif dest_x < src_x:
            return West
        elif dest_y > src_y:
            return North
        elif dest_y < src_y:
            return South
        
    def get_distance(coords_1, coords_2):
        start_op_count = get_op_count()

        distance = calculate_dist(coords_1[0], coords_1[1], coords_2[0],coords_2[1])

        quick_print("get_distance: ", get_op_count() - start_op_count)

        return distance
    
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

        neighbor_coords = (neighbor_x % size, neighbor_y % size)
        
        quick_print("get_neighbor: ", get_op_count() - start_op_count)

        return neighbor_coords
    
    def add_connections(graph):
        start_op_count = get_op_count()

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

        quick_print("add_connections: ", get_op_count() - start_op_count)

    new_game_board = {
        "get_plot": get_plot,
        "get_plots": get_plots,
        "get_neighbor": get_neighbor,
        "get_direction": get_direction,
        "get_distance": get_distance,
        "add_connections": add_connections,
        "apply_property_value": apply_property_value
    }

    return new_game_board
                     
def create_node(x, y):
    new_node = {
        "coords": (x,y)
    }

    return new_node

def translate_coords(coords, x_offset, y_offset):
    return (coords[0] + x_offset, coords[1] + y_offset)

def calculate_dist(x_1, y_1, x_2, y_2):
    return abs(x_1 - x_2) + abs(y_1 - y_2)


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