from __builtins__ import *
from Utility import *

def create_graph():
    edges = []
    neighbor_map = {}

    def add_neighbors(coord_1, coord_2):
        if not coord_1 in neighbor_map:
            neighbor_map[coord_1] = []

        if not coord_2 in neighbor_map:
            neighbor_map[coord_2] = []
        
        neighbor_map[coord_1].append(coord_2)
        neighbor_map[coord_2].append(coord_1)
    
    def remove_neighbors(coord_1, coord_2):
        if coord_1 in neighbor_map:
            neighbor_map[coord_1].remove(coord_2)

        if coord_2 in neighbor_map:
            neighbor_map[coord_2].remove(coord_1)

    def add_edge(edge):
        start_tick = get_tick_count()

        if edge in edges:
            quick_print("add_edge: ", get_tick_count() - start_tick)

            return False
        
        edges.append(edge)

        for coord_1 in edge:
            for coord_2 in edge:
                if coord_1 != coord_2:
                    add_neighbors(coord_1, coord_2)

        quick_print("add_edge: ", get_tick_count() - start_tick)
        
        return True
    
    def remove_edge(edge):
        start_tick = get_tick_count()

        if not edge in edges:
            quick_print("add_edge: ", get_tick_count() - start_tick)

            return False
        
        edges.remove(edge)

        for coord_1 in edge:
            for coord_2 in edge:
                if coord_1 != coord_2:
                    remove_neighbors(coord_1, coord_2)

        quick_print("remove_edge: ", get_tick_count() - start_tick)

        return True
    
    def get_connected(coord):
        if not coord in neighbor_map:
            return set()
        
        neighbors = neighbor_map[coord]
        
        return neighbors
    
    def get_edge_count():
        return len(edges)
    
    new_graph = {
        "add_edge": add_edge,
        "remove_edge": remove_edge,
        "get_edge_count": get_edge_count,
        "get_connected": get_connected,
        "get_edge_count": get_edge_count
    }

    return new_graph