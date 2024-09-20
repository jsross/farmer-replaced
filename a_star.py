from __builtins__ import *
from __test_harness__ import *
from Utility import *

def reconstruct_path(cameFrom, current):
    total_path = [current]

    while current in cameFrom:
        current = cameFrom[current]
        total_path.insert(0, current)

    return total_path

def find_lightest_node(set_coords, graph):
    node_lightest = None

    for current_coord in set_coords:
        current_node = graph["get_node"](current_coord)

        if node_lightest == None:
            node_lightest = current_node
        else:
            if(current_node["weight"] < node_lightest["weight"]):
                node_lightest = current_node

    return node_lightest

def a_star(graph, coord_start, coord_end):
    size = graph["get_size"]()

    for xIndex in range(size):
        for yIndex in range(size):
            coord_current = (xIndex, yIndex)
            node_current = graph["get_node"](coord_current)

            # For node n, distance_from_start is the cost of the cheapest path from start to n currently known.
            if(coord_current == coord_start):
                node_current["distance_from_start"] = 0
            else:
                node_current["distance_from_start"] = Infinity

            node_current["approx_distance_to_end"] = None
            node_current["weight"] = Infinity
            
    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    # This is usually implemented as a min-heap or priority queue rather than a hash-set.
    set_open_coords = {coord_start}

    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from the start
    # to n currently known.
    cameFrom = {}
   
    while len(set_open_coords) > 0:
        # This operation can occur in O(Log(N)) time if openSet is a min-heap or a priority queue
        
        current_node = find_lightest_node(set_open_coords, graph)
        coord_current = current_node["coord"]

        if coord_current == coord_end:
            return reconstruct_path(cameFrom, coord_current)

        set_open_coords.remove(current_node["coord"])

        neighbors = current_node["neighbors"]

        for neighbor_key in neighbors:
            neighbor = neighbors[neighbor_key]
            
            if neighbor == None:
                continue
				
            coord_neighbor = neighbor["coord"]

            # d(current,neighbor) is the weight of the edge from current to neighbor
            # tentative_gScore is the distance from start to the neighbor through current
            neighbor_distance_from_start = current_node["distance_from_start"]  + 1

            if neighbor_distance_from_start < neighbor["distance_from_start"]:
                # This path to neighbor is better than any previous one. Record it!
                cameFrom[coord_neighbor] = coord_current
                neighbor["distance_from_start"] = neighbor_distance_from_start
                                
                # For node n, weight := distance_from_start + approx_distance_to_end. Weight represents our current best guess as to
                # how cheap a path could be from start to finish if it goes through n.
                neighbor["weight"]  = neighbor_distance_from_start + get_distance(coord_neighbor, coord_end)

                set_open_coords.add(coord_neighbor)

    # Open set is empty but goal was never reached
    return None

