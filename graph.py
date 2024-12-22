from __builtins__ import *
from Utility import *

def create_graph(get_weight):
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
    
    def in_cycle(edge):
        if not edge in edges:
            return False
        
        remove_edge(edge)

        vertices = []

        for vertex in edge:
            vertices.append(vertex)

        vertex_1 = vertices[0]
        vertex_2 = vertices[1]

        path = get_a_star_path(vertex_1, vertex_2)

        add_edge(edge)

        return path != None

    def get_a_star_path(coord_start, coord_end):
        start_tick = get_tick_count()
        
        distances_from_start = {}
                
        # The set of discovered nodes that may need to be (re-)expanded.
        # Initially, only the start node is known.
        # This is usually implemented as a min-heap or priority queue rather than a hash-set.
        set_open_coords = {coord_start}
        distances_from_start[coord_start] = 0
        weights = {
            coord_start: get_weight(coord_start, coord_end)
        }

        # For node n, came_from[n] is the node immediately preceding it on the cheapest path from the start
        # to n currently known.
        came_from = {}
        result_path = None
    
        while len(set_open_coords) > 0:
            # This operation can occur in O(Log(N)) time if openSet is a min-heap or a priority queue
            
            coord_current = find_lightest_node(set_open_coords, weights)

            if coord_current == coord_end:
                result_path = reconstruct_path(coord_current, came_from)

                break

            set_open_coords.remove(coord_current)

            neighbors = get_connected(coord_current)

            for neighbor in neighbors:
                #if this is the first time visiting this node, set some defaults
                if not neighbor in distances_from_start:
                    distances_from_start[neighbor] = 9999999999999

                if not neighbor in weights:
                    weights[neighbor] = 9999999999999

                # d(current,neighbor) is the weight of the edge from current to neighbor
                # tentative_gScore is the distance from start to the neighbor through current
                tenative_distance_from_start = distances_from_start[coord_current]  + 1

                if tenative_distance_from_start < distances_from_start[neighbor]:
                    # This path to neighbor is better than any previous one. Record it!
                    came_from[neighbor] = coord_current
                    distances_from_start[neighbor] = tenative_distance_from_start
                                    
                    # For node n, weight := distance_from_start + get_weight. Weight represents our current best guess as to
                    # how cheap a path could be from start to finish if it goes through n.
                    weights[neighbor]  = tenative_distance_from_start + get_weight(coord_end, neighbor)

                    set_open_coords.add(neighbor)

        quick_print("a_star: ", get_tick_count() - start_tick)
        
        return result_path
    
    def get_connected(coord):
        if not coord in neighbor_map:
            return set()
        
        neighbors = neighbor_map[coord]
        
        return neighbors
    
    def get_edge_count():
        return len(edges)
    
    new_graph = {
        "add_edge": add_edge,
        "get_connected": get_connected,
        "get_edge_count": get_edge_count,
        "get_path": get_a_star_path,
        "in_cycle": in_cycle,
        "remove_edge": remove_edge
    }

    return new_graph

def reconstruct_path(current, came_from):
    total_path = []

    while current in came_from:
        total_path.insert(0, current)
        
        current = came_from[current]
    
    if len(total_path) > 0:
        return total_path
    
    return None

def find_lightest_node(coords, weights):
    lightest = None
    lightest_weight = 9999999999999

    for current_coords in coords:
        current_weight = weights[current_coords]

        if current_weight < lightest_weight:
            lightest = current_coords
            lightest_weight = current_weight

    return lightest