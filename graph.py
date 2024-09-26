from __builtins__ import *
from Utility import *

def create_graph():
    connections = {}

    def add_edge(coord_1, coord_2):
        start_op_count = get_op_count()

        if not coord_1 in connections:
            connections[coord_1] = set()
        
        if not coord_2 in connections:
            connections[coord_2] = set()

        connections[coord_1].add(coord_2)
        connections[coord_2].add(coord_1)

        quick_print("add_edge: ", get_op_count() - start_op_count)
        
        return True
    
    def remove_edge(coord_1, coord_2):
        start_op_count = get_op_count()

        if coord_1 in connections:
            coord_1_connections = connections[coord_1]

            if coord_2 in coord_1_connections:
                coord_1_connections.remove(coord_2)
        
        if coord_2 in connections:
            coord_2_connections = connections[coord_2]
            
            if coord_1 in coord_2_connections:
                coord_2_connections.remove(coord_1)

        quick_print("remove_edge: ", get_op_count() - start_op_count)

        return True
    
    def get_connected(coord):
        if not coord in connections:
            return set()
        
        connected_coord = connections[coord]
        
        return connected_coord
        

    new_graph = {
        "add_edge": add_edge,
        "remove_edge": remove_edge,
        "get_connected": get_connected
    }

    return new_graph