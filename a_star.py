from __builtins__ import *
from __test_harness__ import *
from Utility import *

def a_star(graph, coord_start, coord_end):
    weights = {}
    distances_from_start = {}
    approx_distance_to_end = {}

    get_connected = graph["get_connected"]

    def reconstruct_path(current):
        total_path = [current]

        while current in cameFrom:
            current = cameFrom[current]
            total_path.insert(0, current)

        return total_path

    def find_lightest_node(set_coords):
        lightest = None

        for current_coord in set_coords:
            if lightest == None:
                lightest = current_coord
            else:
                if weights[current_coord] < weights[lightest]:
                    lightest = current_coord

        return lightest
            
    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    # This is usually implemented as a min-heap or priority queue rather than a hash-set.
    set_open_coords = {coord_start}

    distances_from_start[coord_start] = 0
    approx_distance_to_end[coord_end] = 0

    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from the start
    # to n currently known.
    cameFrom = {}
   
    while len(set_open_coords) > 0:
        # This operation can occur in O(Log(N)) time if openSet is a min-heap or a priority queue
        
        coord_current = find_lightest_node(set_open_coords)

        if coord_current == coord_end:
            return reconstruct_path(coord_current)

        set_open_coords.remove(coord_current)

        neighbors = get_connected(coord_current)

        for neighbor in neighbors:

            #if this is the first time visiting this node, set some defaults
            if not neighbor in distances_from_start:
                distances_from_start[neighbor] = Infinity

            if not neighbor in approx_distance_to_end:
                approx_distance_to_end[neighbor] = get_distance(neighbor, coord_end)

            if not neighbor in weights:
                weights[neighbor] = Infinity

            # d(current,neighbor) is the weight of the edge from current to neighbor
            # tentative_gScore is the distance from start to the neighbor through current
            tenative_distance_from_start = distances_from_start[coord_current]  + 1

            if tenative_distance_from_start < distances_from_start[neighbor]:
                # This path to neighbor is better than any previous one. Record it!
                cameFrom[neighbor] = coord_current
                distances_from_start[neighbor] = tenative_distance_from_start
                                
                # For node n, weight := distance_from_start + approx_distance_to_end. Weight represents our current best guess as to
                # how cheap a path could be from start to finish if it goes through n.
                weights[neighbor]  = tenative_distance_from_start + approx_distance_to_end[neighbor]

                set_open_coords.add(neighbor)

    # Open set is empty but goal was never reached
    return None

