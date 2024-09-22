from __builtins__ import *
from Utility import *

def create_graph():
    hashes = set()
    connections = {}

    def add_edge(coord_1, coord_2):
        edge = {coord_1, coord_2}

        edge_hash = hash_edge(edge)

        if edge_hash in hashes:
            return False
        
        hashes.add(edge_hash)

        if not coord_1 in connections:
            connections[coord_1] = set()
        
        if not coord_2 in connections:
            connections[coord_2] = set()

        connections[coord_1].add(coord_2)
        connections[coord_2].add(coord_1)
        
        return True
    
    def remove_edge(coord_1, coord_2):
        edge = {coord_1, coord_2}

        edge_hash = hash_edge(edge)

        if not edge_hash in hashes:
            return False
        
        hashes.remove(edge_hash)

        coord_1_connections = connections[coord_1]
        coord_2_connections = connections[coord_2]

        coord_1_connections.remove(coord_2)
        coord_2_connections.remove(coord_1)

        return True
    
    def get_connected(coord):
        if not coord in connections:
            return {}
        
        return connections[coord]
        

    new_graph = {
        "add_edge": add_edge,
        "remove_edge": remove_edge,
        "get_connected": get_connected
    }

    return new_graph
    
def hash_edge(edge):
    start_ops = get_op_count()
     
    edge_set = set()
	
	for coord in edge:
		edge_set.add(hash_coord(coord))
		
	result = hash_set(edge_set)

    quick_print("hash_edge: ", (get_op_count() - start_ops))
		
	return result 

def hash_set(int_set):
    start_ops = get_op_count()

    MOD = 1000007
    sum1 = 0
    sum2 = 0
    sum3 = 0

    for num in int_set:
        sum1 = (sum1 + num) % MOD
        sum2 = (sum2 + num * num) % MOD
        sum3 = (sum3 + num * num * num) % MOD
        
    hash_value = (sum1 + 31 * sum2 + 961 * sum3) % MOD  # 31^2 = 961

    quick_print("hash_set: ", (get_op_count() - start_ops))
    return hash_value

def hash_coord(coord):
    start_ops = get_op_count()
    hash_value = hash_cantor(coord[0], coord[1])
    quick_print("hash_coord: ", (get_op_count() - start_ops))

    return hash_value

def hash_cantor(x, y):
    start_ops = get_op_count()

    hash_value = ((x + y) * (x + y + 1) / 2) + y

    quick_print("hash_cantor: ", (get_op_count() - start_ops))

    return hash_value

