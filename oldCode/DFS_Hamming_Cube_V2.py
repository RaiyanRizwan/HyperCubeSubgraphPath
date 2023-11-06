import random

def hamming_weight(btstr):
	return sum([eval(e) for e in btstr])

def cheapest_hamming(nodes):
	if nodes:
		cheapest_adj = min(nodes, key=lambda node: hamming_weight(node.bitstr))
		return cheapest_adj.bitstr
	else:
		return 'isolated'

def hammings(nodes):
	"""
	Returns a list of hamming weights for each node sorted from smallest to largest
	"""
	return sorted(list(zip(nodes, map(lambda node: hamming_weight(node.bitstr), nodes))), key=lambda pair: pair[1])

class Graph:
	"""
	A graph that contains node objects related to each other via common edges.

	>>> Graph(3).nodes
	[node: 000, neighbors: ['100', '010', '001'], 
	node: 100, neighbors: ['000', '110', '101'], 
	node: 110, neighbors: ['010', '100', '111'], 
	node: 010, neighbors: ['110', '000', '011'], 
	node: 011, neighbors: ['111', '001', '010'], 
	node: 111, neighbors: ['011', '101', '110'], 
	node: 101, neighbors: ['001', '111', '100'], 
	node: 001, neighbors: ['101', '011', '000']]

	"""

	def __init__(self, n):
		self.nodes = []
		self.graph(n)

	def graph(self, n):
		self.nodes.append(Node('0'*n))
		self.nodes[-1].adjacents(self)
	
	def dfs(self, sn_i, en_i):
		"""
		Finds shortest possible path from start node to end node. 

		>>> g = Graph(8) # 8th dimension hypercube
		>>> g
		['00000000', '10000000', '11000000', '01000000', '01100000', '11100000', '10100000', '00100000', '00110000', '10110000', '11110000', '01110000', '01010000', '11010000', '10010000', '00010000', '00011000', '10011000', '11011000', '01011000', '01111000', '11111000', '10111000', '00111000', '00101000', '10101000', '11101000', '01101000', '01001000', '11001000', '10001000', '00001000', '00001100', '10001100', '11001100', '01001100', '01101100', '11101100', '10101100', '00101100', '00111100', '10111100', '11111100', '01111100', '01011100', '11011100', '10011100', '00011100', '00010100', '10010100', '11010100', '01010100', '01110100', '11110100', '10110100', '00110100', '00100100', '10100100', '11100100', '01100100', '01000100', '11000100', '10000100', '00000100', '00000110', '10000110', '11000110', '01000110', '01100110', '11100110', '10100110', '00100110', '00110110', '10110110', '11110110', '01110110', '01010110', '11010110', '10010110', '00010110', '00011110', '10011110', '11011110', '01011110', '01111110', '11111110', '10111110', '00111110', '00101110', '10101110', '11101110', '01101110', '01001110', '11001110', '10001110', '00001110', '00001010', '10001010', '11001010', '01001010', '01101010', '11101010', '10101010', '00101010', '00111010', '10111010', '11111010', '01111010', '01011010', '11011010', '10011010', '00011010', '00010010', '10010010', '11010010', '01010010', '01110010', '11110010', '10110010', '00110010', '00100010', '10100010', '11100010', '01100010', '01000010', '11000010', '10000010', '00000010', '00000011', '10000011', '11000011', '01000011', '01100011', '11100011', '10100011', '00100011', '00110011', '10110011', '11110011', '01110011', '01010011', '11010011', '10010011', '00010011', '00011011', '10011011', '11011011', '01011011', '01111011', '11111011', '10111011', '00111011', '00101011', '10101011', '11101011', '01101011', '01001011', '11001011', '10001011', '00001011', '00001111', '10001111', '11001111', '01001111', '01101111', '11101111', '10101111', '00101111', '00111111', '10111111', '11111111', '01111111', '01011111', '11011111', '10011111', '00011111', '00010111', '10010111', '11010111', '01010111', '01110111', '11110111', '10110111', '00110111', '00100111', '10100111', '11100111', '01100111', '01000111', '11000111', '10000111', '00000111', '00000101', '10000101', '11000101', '01000101', '01100101', '11100101', '10100101', '00100101', '00110101', '10110101', '11110101', '01110101', '01010101', '11010101', '10010101', '00010101', '00011101', '10011101', '11011101', '01011101', '01111101', '11111101', '10111101', '00111101', '00101101', '10101101', '11101101', '01101101', '01001101', '11001101', '10001101', '00001101', '00001001', '10001001', '11001001', '01001001', '01101001', '11101001', '10101001', '00101001', '00111001', '10111001', '11111001', '01111001', '01011001', '11011001', '10011001', '00011001', '00010001', '10010001', '11010001', '01010001', '01110001', '11110001', '10110001', '00110001', '00100001', '10100001', '11100001', '01100001', '01000001', '11000001', '10000001', '00000001']
		>>> g.dfs(0, 170) # all zero to all one bitstring
		"edges: 8, path: ['00000000', '10000000', '11000000', '11100000', '11110000', '11111000', '11111100', '11111110', '11111111']"

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

			en_h = hamming_weight(end_node.bitstr)

			while not start_node == end_node:
				
				#print("start:", start_node.bitstr)
				#print("blacklisted:", black_listed)
				#print("path", [n.bitstr for n in path])

				if black_listed and all(e in black_listed for e in start_node.adjacent):
					return 'no path' # exhausted all path possibilities

				if start_node.adjacent and not all(e in path + black_listed for e in start_node.adjacent):

					sn_neighbors_h = hammings(start_node.adjacent) # sorted hamming weights of all neighbors
					optimal = min(sn_neighbors_h, key= lambda pair: abs(en_h - hamming_weight(pair[0].bitstr)))
					o_n = optimal[0] # optimal node to go to

					while o_n in path or o_n in black_listed:

						if not sn_neighbors_h:
							return "no path" 

						sn_neighbors_h.remove(optimal)
						optimal = min(sn_neighbors_h, key= lambda pair: abs(en_h - hamming_weight(pair[0].bitstr)))
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

		>>> g = Graph(3)
		>>> g.subgraph(self, 3)
		[node: 000, neighbors: ['100', '010', '001'], cheapest_hamming: 100, 
		node: 100, neighbors: ['000', '110'], cheapest_hamming: 000, 
		node: 110, neighbors: ['010', '100', '111'], cheapest_hamming: 010, 
		node: 010, neighbors: ['110'], cheapest_hamming: 110, 
		node: 011, neighbors: ['111', '001', '010'], cheapest_hamming: 001, 
		node: 111, neighbors: ['011', '101', '110'], cheapest_hamming: 011, 
		node: 101, neighbors: ['001', '111', '100'], cheapest_hamming: 001, 
		node: 001, neighbors: ['101', '011', '000'], cheapest_hamming: 000]
		
		>>> Graph(3).subgraph(30) # we'd expect 24 edges (3 per node, 8 nodes) to be removed
		not enough edges
		not enough edges
		not enough edges
		not enough edges
		not enough edges
		not enough edges
		[node: 000, neighbors: [], cheapest_hamming: isolated, 
		node: 100, neighbors: [], cheapest_hamming: isolated, 
		node: 110, neighbors: [], cheapest_hamming: isolated, 
		node: 010, neighbors: [], cheapest_hamming: isolated, 
		node: 011, neighbors: [], cheapest_hamming: isolated, 
		node: 111, neighbors: [], cheapest_hamming: isolated, 
		node: 101, neighbors: [], cheapest_hamming: isolated, 
		node: 001, neighbors: [], cheapest_hamming: isolated]
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

class Node:

	def __init__(self, bitstr):
		self.bitstr = bitstr

	def adjacents(self, g):
		adjacents = []

		for i in range(len(self.bitstr)):

			flipped = 1 if eval(self.bitstr[i]) == 0 else 0
			adj_bitsr = self.bitstr[:i] + str(flipped) + self.bitstr[i+1:]
			
			if adj_bitsr in map(lambda node: node.bitstr, g.nodes):
				adjacents.extend([node for node in g.nodes if node.bitstr == adj_bitsr])
			else:
				new_node = Node(adj_bitsr)
				g.nodes.append(new_node)
				adjacents.append(new_node) 
				new_node.adjacents(g)

		self.adjacent = adjacents

	def __repr__(self):
		return f'node: {self.bitstr}, neighbors: {list(map(lambda node: node.bitstr, self.adjacent))}, cheapest_hamming: {cheapest_hamming(self.adjacent)}'
	
