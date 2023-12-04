import random
from Fringe import Fringe
from Node import Node

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

    def __init__(self, n, seed=0):
        self.nodes_adjacency = {} # Node : neighbors[Node]
        self.decimal_Node_dict = {} # decimal value : Node
        self.rand = random.Random(seed)
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
            self.nodes_adjacency[node] = node_neighbors # update graph
                 
    def path(self, start_bitstr, end_bitstr):
        """
        Finds a path from start node to end node. Robust against missing edges.
        """

        current_node = self.decimal_Node_dict[int(start_bitstr, 2)]
        end_node = self.decimal_Node_dict[int(end_bitstr, 2)]

        ordered_path = [current_node]
        unordered_path = set(ordered_path) # use to check contains
        dead_ends = set()
        
        while not current_node == end_node: # until we reach our target
            neighbors = self.nodes_adjacency[current_node] # neighbors list
            if len(ordered_path) == 1 and all(neighbor in dead_ends for neighbor in neighbors) or not neighbors: # @ start with nowhere to go
                return 'no path'
            
            # find optimal node to traverse to
            best_valid_node = None
            best_valid_node_difference = 1e100
            for neighbor_node in neighbors:
                better_distance = abs(end_node.hamming_weight - neighbor_node.hamming_weight) < best_valid_node_difference
                valid = neighbor_node not in dead_ends and neighbor_node not in unordered_path
                if better_distance and valid:
                    best_valid_node = neighbor_node
                    best_valid_node_difference = abs(end_node.hamming_weight - neighbor_node.hamming_weight)

            if best_valid_node: # traverse
                ordered_path.append(best_valid_node)
                unordered_path.add(best_valid_node)
                current_node = best_valid_node
            else: # back up
                dead_ends.add(current_node)
                unordered_path.remove(current_node)
                ordered_path.pop()
                current_node = ordered_path[-1]
            
        return f'edges: {len(ordered_path)-1}, path: {list(map(lambda node: node.bitstr, ordered_path))}' # return bit strings along the path

    def subgraph(self, num_edges):
        """
        Generates a subgraph of this graph with num_edges number of edges removed. Randomly picks nodes from which to remove edges.
        If a node has no edges, moves onto the next node (taking advantage of for loop generator properties) until all edges are gone.
        """
        
        if num_edges > len([node for neighbors in self.nodes_adjacency.values() for node in neighbors]) // 2:
            return 'not enough edges'

        num_removed = 0
        while num_removed < num_edges:
            random_node = self.decimal_Node_dict[self.rand.randint(0, 2**self.n - 1)]
            neighbors = self.nodes_adjacency[random_node]
            if neighbors:
                node_to_remove = neighbors[self.rand.randint(0, len(neighbors) - 1)]
                self.nodes_adjacency[random_node].remove(node_to_remove)
                self.nodes_adjacency[node_to_remove].remove(random_node)
                num_removed += 1

    def shortest_path(self, start_bitstr, target_bitstr):
        """A* algorithm. Heuristic := hamming distance from current_bitstr to target_bitstr. Any path from
        current to target is greater than or equal in length to the hamming distance. Thus, the heuristic is admissible.
        The heuristic is also consistent by the property that to get to a 'further' target, more bits must be flipped, and
        thus the hamming distance between an intermediate node and the target will never be less than that of a closer node."""
        
        s_d = c_d = int(start_bitstr, 2) # decimal value of start bitstring
        fringe = Fringe(self.decimal_Node_dict.keys()) # Fringe PQ [decimal_key : distance]
        distTo = {v : float('inf') for v in self.decimal_Node_dict.keys()} # initialize distances to each node as infinity
        fringe.remove(s_d) # remove start node from fringe
        distTo[s_d] = 0 # set distance to start node = 0
        edgeTo = {v: None for v in self.nodes_adjacency.keys()}
        EDGE_LENGTH = 1 # all edges are a hamming distance of 1 in a hypercube
        while fringe:
            c_node = self.decimal_Node_dict[c_d] 
            # relax neighbors
            for neighbor in self.nodes_adjacency[c_node]: 
                g = distTo[c_d] # distance to current node
                h = c_node.hamming_distance(neighbor) # estimated distance from current node to target
                n_d = neighbor.value
                if g + EDGE_LENGTH + h < distTo[n_d]:
                    fringe.push(n_d, g + EDGE_LENGTH + h)
                    distTo[n_d] = g + EDGE_LENGTH
                    edgeTo[neighbor] = c_node
            # dequeue shortest distance vertex
            c_d = fringe.pop().vertex
            if c_d == int(target_bitstr, 2):
                break
        target_node = self.decimal_Node_dict[int(target_bitstr, 2)]
        if not edgeTo[target_node]:
            return "No path found."
        # Gather path from edgeTo list
        start_node = self.decimal_Node_dict[s_d]
        path = [target_node]
        while target_node != start_node:
            path = [edgeTo[target_node]] + path
            target_node = edgeTo[target_node]
        return f'edges: {len(path)-1}, path: {path}'

    def __repr__(self):
        out = []
        for node in self.nodes_adjacency.keys():
            out.append(f'{node.bitstr}: {", ".join([neighbor.bitstr for neighbor in self.nodes_adjacency[node]])}')
        return '\n'.join(out)
