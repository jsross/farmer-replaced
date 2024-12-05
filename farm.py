from __builtins__ import *
from Utility import *

def create_farm(size):
    matrix = create_matrix(size, create_node)

    regions = []

    def create_region(type, anchor_coords, width, height, fill_strategy):
        end_coords = (anchor_coords[0] + width, anchor_coords[1] + height)
        plots = select_from_matrix(matrix, anchor_coords, end_coords, fill_strategy)

        region = {
            "type": type,
            "plots": plots,
            "anchor_coords": anchor_coords,
            "end_coords": end_coords,
            "width": width,
            "height": height
        }

        regions.append(region)

    def get_regions():
        return regions
    
    def apply_property_value(coord_1, coord_2, property_name, property_value, fill_test):
        x1 = coord_1[0]
        y1 = coord_1[1]
        x2 = coord_2[0]
        y2 = coord_2[1]

        for x_index in range(x1, x2):
            for y_index in range(y1, y2):
                if fill_test(x_index, y_index):
                    plot = get_plot(x_index, y_index)
                    plot[property_name] = property_value

    def get_plot(x, y):
        return matrix[x][y]
    
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
        
        if coords_2 == None:
            print("oops")

        distance = calculate_dist(coords_1[0], coords_1[1], coords_2[0],coords_2[1])

        quick_print("get_distance: ", get_op_count() - start_op_count)

        return distance
    
    def get_distance_map(x, y):
        result = {}

        for x_index in range(size):
            for y_index in range(size):
                result[(x_index, y_index)] = calculate_dist(x_index, y_index, x, y)
        
        return result

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
    
    def get_neighbors(x, y):
        neighbors = [
            (x, (y + 1) % size), # North
            ((x + 1) % size, y), # East
            (x, (y - 1) % size), # South
            ((x - 1) % size, y)  # West
        ]

        return neighbors
    
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

    def select_coords(properties):

        def test_func(item, _x, _y):
            for property_key in properties:
                if not item[property_key] == properties[property_key]:
                    return False
            
            return True

        return select_prop_from_matrix(matrix, "coords", test_func)

    new_farm = {
        "add_connections": add_connections,
        "apply_property_value": apply_property_value,
        "create_region": create_region,
        "get_plot": get_plot,
        "get_neighbor": get_neighbor,
        "get_neighbors": get_neighbors,
        "get_direction": get_direction,
        "get_distance": get_distance,
        "get_distance_map": get_distance_map,
        "get_regions": get_regions,
        "select_coords": select_coords
    }

    return new_farm
                     
def create_node(x, y):
    new_node = {
        "coords": (x,y),
        "action": no_op,
        "entity_type": None,
        "ground_type": None,
        "measure": 0,
        "can_harvest": False,
        "priority": 0,
        "water": 0,
        "timestamp": 0
    }

    return new_node

def no_op(_):
    return

def translate_coords(coords, x_offset, y_offset):
    return (coords[0] + x_offset, coords[1] + y_offset)

def calculate_dist(x_1, y_1, x_2, y_2):
    return abs(x_1 - x_2) + abs(y_1 - y_2)

def fill_strategy_checkerd(_, x, y):
	rem = y % 2
	fill = (x - rem ) % 2 == 0
	return fill

def fill_strategy_checkerd_alt(_, x, y):
	rem = y % 2
	fill = (x - rem ) % 2 == 1
	
	return fill

def fill_strategy_solid(_, x, y):
	return True