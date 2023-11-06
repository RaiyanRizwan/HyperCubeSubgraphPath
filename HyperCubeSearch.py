import random

class Node:

    def __init__(self, value: int, dim: int):
        self.value = value
        self.bitstr = str(format(self.value, f'0{dim}b'))
        self.hamming_weight = sum([eval(e) for e in self.bitstr])

    def __repr__(self):
        return f'node: {self.bitstr}'

    def __eq__(self, other_node):
        return self.value == other_node.value
        
    def __hash__(self):
        return self.value

class Graph:
    """
    An undirected Hypercube graph. Generates a 15 dimensional hypercube (32768 nodes) in around 5 seconds.
    Example:
    g = Graph(15)
    g.subgraph(75000)
    g.shortest_path('000000000000000', '111111111111111')
    >>> "edges: 17, path: ['000000000000000', '100000000000000', '110000000000000', 
    '110100000000000', '110110000000000', '111110000000000', 
    '111111000000000', '111111100000000', '111111110000000', 
    '111111111000000', '111111111100000', '111111111110000', 
    '111111111111000', '111111111111100', '011111111111100', 
    '011111111111110', '111111111111110', '111111111111111']"
    """

    def __init__(self, n):
        self.nodes = {}
        self.decimal_Node_dict = {}
        self.graph(n)
        self.n = n

    def graph(self, n):
        """O(n2^n)"""
        self.decimal_Node_dict = {d : Node(d, n) for d in range(2**n)}
        for node_val in self.decimal_Node_dict: # loop through nodes
            node_neighbors = []
            for i in range(n): # loop through bits
                exponent = n - 1 - i
                node = self.decimal_Node_dict[node_val] # O(1)
                neighbor_val = node_val + [1, -1][eval(node.bitstr[i])]*(2**exponent) # [-1, 1][ith bit value]: if 0, then 1 (flip 0 to 1) and if 1, then -1 (flip 1 to 0)
                neighbor_node = self.decimal_Node_dict[neighbor_val] # O(1)
                node_neighbors.append(neighbor_node) # append to neighbors list
            self.nodes[node] = node_neighbors # update graph
                 
    def shortest_path(self, start_bitstr, end_bitstr):
        """
        Finds shortest possible path from start node to end node. 
        """

        current_node = self.decimal_Node_dict[int(start_bitstr, 2)]
        end_node = self.decimal_Node_dict[int(end_bitstr, 2)]

        path = [current_node]
        dead_ends = []
        
        while not current_node == end_node: # until we reach our target
            neighbors = self.nodes[current_node] # neighbors list
            if len(path) == 1 and all(neighbor in dead_ends for neighbor in neighbors) or not neighbors: # @ start with nowhere to go
                return 'no path'
            
            # find optimal node to traverse to
            best_valid_node = None
            best_valid_node_difference = 1e100
            for neighbor_node in neighbors:
                better_distance = abs(end_node.hamming_weight - neighbor_node.hamming_weight) < best_valid_node_difference
                valid = neighbor_node not in dead_ends and neighbor_node not in path
                if better_distance and valid:
                    best_valid_node = neighbor_node
                    best_valid_node_difference = abs(end_node.hamming_weight - neighbor_node.hamming_weight)

            if best_valid_node:
                # traverse
                path.append(best_valid_node)
                current_node = best_valid_node
            else:
                # back up
                dead_ends.append(current_node)
                path.pop()
                current_node = path[-1]
            
        return f'edges: {len(path)-1}, path: {list(map(lambda node: node.bitstr, path))}' # return bit strings along the path

    def subgraph(self, num_edges):
        """
        Generates a subgraph of this graph with num_edges number of edges removed. Randomly picks nodes from which to remove edges.
        If a node has no edges, moves onto the next node (taking advantage of for loop generator properties) until all edges are gone.
        """
        
        if num_edges > len([node for neighbors in self.nodes.values() for node in neighbors]) // 2:
            return 'not enough edges'

        num_removed = 0
        while num_removed < num_edges:
            random_node = self.decimal_Node_dict[random.randint(0, 2**self.n - 1)]
            neighbors = self.nodes[random_node]
            if neighbors:
                node_to_remove = neighbors[random.randint(0, len(neighbors) - 1)]
                self.nodes[random_node].remove(node_to_remove)
                self.nodes[node_to_remove].remove(random_node)
                num_removed += 1
        
        print(self)

    def __repr__(self):
        out = []
        for node in self.nodes.keys():
            out.append(f'{node.bitstr}: {", ".join([neighbor.bitstr for neighbor in self.nodes[node]])}')
        return '\n'.join(out)
