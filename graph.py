from __builtins__ import *
from Utility import *
from matrix import *

def create_graph():
    new_graph = {}

    return new_graph

def add_edge(graph, edge_to_add):
    edge_tuple = convert_edge_to_tuple(edge_to_add)
    vertex_1 = edge_tuple[0]
    vertex_2 = edge_tuple[1]

    state = {
        "connected": False
    }

    if not vertex_1 in graph:
        graph[vertex_1] = {}

    if not vertex_2 in graph[vertex_1]:
        graph[vertex_1][vertex_2] = state

    if not vertex_2 in graph:
        graph[vertex_2] = {}

    if not vertex_1 in graph[vertex_2]:
        graph[vertex_2][vertex_1] = state

    graph[vertex_1][vertex_2]["connected"] = True

def contains_edge(graph, edge):
    edge_tuple = convert_edge_to_tuple(edge)
    vertex_1 = edge_tuple[0]
    vertex_2 = edge_tuple[1]

    if vertex_1 in graph and vertex_2 in graph[vertex_1]:
        l1 = graph[vertex_1]
        l2 = l1[vertex_2]
        result = l2["connected"]

        return result
    
    return False

def remove_edge(graph, edge):
    edge_tuple = convert_edge_to_tuple(edge)
    vertex_1 = edge_tuple[0]
    vertex_2 = edge_tuple[1]

    has_edge = contains_edge(graph, edge)

    if has_edge:
        graph[vertex_1][vertex_2]["connected"] = False

def get_neighbors(graph, vertex):
    start_tick = get_tick_count()

    neighbors = []

    if not vertex in graph:
        return neighbors

    for key in graph[vertex]:
        if graph[vertex][key]["connected"]:
            neighbors.append(key)

    # quick_print("get_neighbors: ", get_tick_count() - start_tick)
    
    return neighbors

def in_cycle(graph, edge, banned_edges):
    start_tick = get_tick_count()

    if not contains_edge(graph, edge):
        return False
    
    if edge in banned_edges:
        return False
    
    remove_edge(graph, edge)

    for banned_edge in banned_edges:
        remove_edge(graph, banned_edge)

    vertices = []

    for vertex in edge:
        vertices.append(vertex)

    vertex_1 = vertices[0]
    vertex_2 = vertices[1]

    path = get_path(graph, vertex_1, vertex_2, get_distance)

    is_in_cycle = path != None

    add_edge(graph, edge)

    for banned_edge in banned_edges:
        add_edge(graph, banned_edge)

    # quick_print("in_cycle: ", get_tick_count() - start_tick)

    return is_in_cycle

def get_path(graph, vertex_start, vertex_end, get_weight):
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
        
        neighbors = get_neighbors(graph, current_vertex)

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

    #quick_print("get_path: ", get_tick_count() - start_tick)
    
    return result_path

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

def convert_edge_to_tuple(edge):
    vert_1 = None
    vert_2 = None

    for vertex in edge:
        if vert_1 == None:
            vert_1 = vertex
        else:
            vert_2 = vertex
    
    return (vert_1, vert_2)

def print_graph(graph, banned_edges):
    size = get_world_size()
    drone_coords = (get_pos_x(), get_pos_y())

    for y_index in range(size - 1, -1, -1):
        nodes_and_edges = " "
        edges_only = "  "

        for x_index in range(size):
            current_coords = (x_index, y_index)

            west_coords = (x_index + 1, y_index)
            west_edge = set([current_coords, west_coords])

            if current_coords == drone_coords:
                nodes_and_edges += "■"
            else:
                nodes_and_edges += "O"

            if contains_edge(graph, west_edge):
                if not west_edge in banned_edges:
                    nodes_and_edges += "-"
                else:
                    nodes_and_edges += "X"
            else:
                nodes_and_edges += " "

            south_coords = (x_index, y_index - 1)
            south_edge = set([current_coords, south_coords])

            if contains_edge(graph, south_edge):
                if not south_edge in banned_edges:
                    edges_only += " |"
                else:
                    edges_only += " X"
            else:
                edges_only += "  "

        quick_print(y_index, nodes_and_edges)
        
        if y_index > 1:
            quick_print(edges_only)

    bottom = []
    for index in range(size):
        bottom.append(index)
    
    quick_print(" ", bottom)

    quick_print("--------------------------------")

