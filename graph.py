from __builtins__ import *
from Utility import *

def create_graph(get_weight):
    edges = []
    neighbor_map = {}

    def add_neighbors(vertex_1, vertex_2):
        if not vertex_1 in neighbor_map:
            neighbor_map[vertex_1] = set()

        if not vertex_2 in neighbor_map:
            neighbor_map[vertex_2] = set()
        
        neighbor_map[vertex_1].add(vertex_2)
        neighbor_map[vertex_2].add(vertex_1)
    
    def remove_neighbors(vertex_1, vertex_2):
        if vertex_1 in neighbor_map and vertex_2 in neighbor_map[vertex_1]:
            neighbor_map[vertex_1].remove(vertex_2)

        if vertex_2 in neighbor_map and vertex_1 in neighbor_map[vertex_2]:
            neighbor_map[vertex_2].remove(vertex_1)

    def add_edge(edge):
        start_tick = get_tick_count()

        if edge in edges:
            # quick_print("add_edge: ", get_tick_count() - start_tick)

            return False
        
        edges.append(edge)

        for vertex_1 in edge:
            for vertex_2 in edge:
                if vertex_1 != vertex_2:
                    add_neighbors(vertex_1, vertex_2)

        # quick_print("add_edge: ", get_tick_count() - start_tick)
        
        return True
    
    def remove_edge(edge):
        start_tick = get_tick_count()

        if not edge in edges:
            quick_print("add_edge: ", get_tick_count() - start_tick)

            return False
        
        edges.remove(edge)

        for vertex_1 in edge:
            for vertex_2 in edge:
                if vertex_1 != vertex_2:
                    remove_neighbors(vertex_1, vertex_2)

        quick_print("remove_edge: ", get_tick_count() - start_tick)

        return True
    
    def in_cycle(edge):
        start_tick = get_tick_count()

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

        is_in_cycle = path != None

        if is_in_cycle:
            quick_print("Contains Cycle: ", path)

        quick_print("in_cycle: ", get_tick_count() - start_tick)

        return is_in_cycle

    def get_a_star_path(vertex_start, vertex_end):
        start_tick = get_tick_count()
        
        distances_from_start = {}
                
        # The set of discovered nodes that may need to be (re-)expanded.
        # Initially, only the start node is known.
        # This is usually implemented as a min-heap or priority queue rather than a hash-set.
        set_open_vertex = {vertex_start}
        distances_from_start[vertex_start] = 0

        weights = {
            vertex_start: get_weight(vertex_start, vertex_end)
        }

        # For node n, came_from[n] is the node immediately preceding it on the cheapest path from the start
        # to n currently known.
        came_from = {}
        result_path = None
    
        while len(set_open_vertex) > 0:
            # This operation can occur in O(Log(N)) time if openSet is a min-heap or a priority queue
            
            current_vertex = find_lightest_node(set_open_vertex, weights)

            if current_vertex == vertex_end:
                result_path = reconstruct_path(current_vertex, came_from)

                break

            set_open_vertex.remove(current_vertex)
            
            neighbors = get_connected(current_vertex)

            for neighbor in neighbors:
                #if this is the first time visiting this node, set some defaults
                if not neighbor in distances_from_start:
                    distances_from_start[neighbor] = 9999999999999

                if not neighbor in weights:
                    weights[neighbor] = 9999999999999

                # d(current,neighbor) is the weight of the edge from current to neighbor
                # tentative_gScore is the distance from start to the neighbor through current
                tenative_distance_from_start = distances_from_start[current_vertex]  + 1

                if tenative_distance_from_start < distances_from_start[neighbor]:
                    # This path to neighbor is better than any previous one. Record it!
                    came_from[neighbor] = current_vertex
                    distances_from_start[neighbor] = tenative_distance_from_start
                                    
                    # For node n, weight := distance_from_start + get_weight. Weight represents our current best guess as to
                    # how cheap a path could be from start to finish if it goes through n.
                    weights[neighbor]  = tenative_distance_from_start + get_weight(vertex_end, neighbor)

                    set_open_vertex.add(neighbor)

        quick_print("a_star: ", get_tick_count() - start_tick)
        
        return result_path
    
    def get_connected(vertex):
        if not vertex in neighbor_map:
            return set()
        
        neighbors = neighbor_map[vertex]
        
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

def find_lightest_node(vertices, weights):
    lightest = None
    lightest_weight = 9999999999999

    for vertex in vertices:
        current_weight = weights[vertex]

        if current_weight < lightest_weight:
            lightest = vertex
            lightest_weight = current_weight

    return lightest