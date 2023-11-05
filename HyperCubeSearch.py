import random

class Node:

    def __init__(self, value: int, neighbors: list, dim: int):
        self.value = value
        self.neighbors = neighbors
        self.bitstr = str(format(self.value, f'0{dim}b'))
        self.hamming_weight = sum([eval(e) for e in self.bitstr])
        
    def cheapest_hamming(self):
        if self.neighbors:
            cheapest_adj = min(self.neighbors, key=lambda node: node.hamming_weight)
            return cheapest_adj.bitstr
        else:
            return 'isolated'

    def __repr__(self):
        return f'node: {self.bitstr}, neighbors: {[neighbor.bitstr for neighbor in self.neighbors]}, cheapest_hamming: {self.cheapest_hamming()}'

    def __eq__(self, other_node):
        return self.value == other_node.value
        
    def __hash__(self):
        return self.value

def hammings(nodes):
	"""
	Returns a list of hamming weights for each node sorted from smallest to largest
	"""
	return sorted(list(zip(nodes, map(lambda node: node.hamming_weight, nodes))), key=lambda pair: pair[1])

class Graph:
    """
    A Hypercube graph.
    """

    def __init__(self, n):
        self.nodes = {}
        self.graph(n)

    def graph(self, n):
        """O(n2^n)"""
        nodes_dict = {d : Node(d, [], n) for d in range(2**n)}
        for node_val in nodes_dict: # loop through nodes
            node_neighbors = []
            for i in range(n): # loop through bits
                exponent = n - 1 - i
                node = nodes_dict[node_val] # O(1)
                neighbor_val = node_val + [1, -1][eval(node.bitstr[i])]*(2**exponent) # [-1, 1][ith bit value]: if 0, then 1 (flip 0 to 1) and if 1, then -1 (flip 1 to 0)
                neighbor_node = nodes_dict[neighbor_val] # O(1)
                node_neighbors.append(neighbor_node) # append to neighbors list
            node.neighbors = node_neighbors # update node neighbors
            self.nodes[node] = node_neighbors # update graph
                        
    def dfs(self, sn_i, en_i):
        """
        Finds shortest possible path from start node to end node. 
        """

        assert sn_i < len(self.nodes), en_i < len(self.nodes)

        start_node = self.nodes[sn_i]
        end_node = self.nodes[en_i]

        path = [start_node]
        black_listed = []

        if not start_node.adjacent:
            return 'no path found' # island nodes
        elif end_node in start_node.adjacent: 
            path.append(end_node) # end node is directly 
        else:

            en_h = end_node.hamming_weight

            while not start_node == end_node:
                
                #print("start:", start_node.bitstr)
                #print("blacklisted:", black_listed)
                #print("path", [n.bitstr for n in path])

                if black_listed and all(e in black_listed for e in start_node.adjacent):
                    return 'no path' # exhausted all path possibilities

                if start_node.adjacent and not all(e in path + black_listed for e in start_node.adjacent):

                    sn_neighbors_h = hammings(start_node.adjacent) # sorted hamming weights of all neighbors
                    optimal = min(sn_neighbors_h, key= lambda pair: abs(en_h - pair[0].hamming_weight))
                    o_n = optimal[0] # optimal node to go to

                    while o_n in path or o_n in black_listed:

                        if not sn_neighbors_h:
                            return "no path" 

                        sn_neighbors_h.remove(optimal)
                        optimal = min(sn_neighbors_h, key= lambda pair: abs(en_h - pair[0].hamming_weight))
                        o_n = optimal[0]

                    path.append(o_n)
                    start_node = path[-1]

                else:
                    black_listed.append(start_node)
                    start_node = path[-2]
                    path.pop()

        return f'edges: {len(path)-1}, path: {list(map(lambda node: node.bitstr,path))}'

    def remove_edge(self, n1_i, n2_i):
        node1, node2 = self.nodes[n1_i], self.nodes[n2_i]
        node1.adjacent.remove(node2)
        node2.adjacent.remove(node1)

    def subgraph(self, num_edges):
        """
        Generates a subgraph of this graph with num_edges number of edges removed. Randomly picks nodes from which to remove edges.
        If a node has no edges, moves onto the next node (taking advantage of for loop generator properties) until all edges are gone.
        """

        num_removed = 0
        lst_of_nodes = [self.nodes[random.randint(0, len(self.nodes)-1)] for _ in range(num_edges)]
        for node in lst_of_nodes:
            if node.adjacent:
                node.adjacent.pop()
                num_removed+=1
            else:
                ind_to_avoid = self.index_of_bitstr(node.bitstr)
                if ind_to_avoid+1 >= len(self.nodes):
                    print('not enough edges')
                else:
                    lst_of_nodes.append(self.nodes[ind_to_avoid+1])

        return self.nodes

    def index_of_bitstr(self, bitstr):
        return list(map(lambda node: node.bitstr, self.nodes)).index(bitstr)

    def __repr__(self):
        return f'{list(map(lambda node: node.bitstr, self.nodes))}'
