# how can we represent a hypercube?
"""
2D cube:

00 01

10 11

3D cube:

		001			011
000			010


		101			111
100			110			

now systematically: start w/ 0, then 1. take each and attach a 0 or 1 to it. take each of those and so on. classic tree

0

01
	010
	011

00
	001
	000

1

11
	110
	111

10
	100
	101

# make a node class that stores bitstring & list of adjacent nodes
# create nodes for graph by flipping one bit at a time & looking in the heap for existing nodes to connect
"""

from functools import reduce

def hamming_weight(btstr):
	return sum([eval(e) for e in btstr])

def graph(n):
	"""
	Return list of bitstring nodes.

	>>> graph(4)
	[node: 010, reachable nodes: ['110', '000', '011'], lowest_hamming_edge: {0, '000'}, 
	node: 011, reachable nodes: ['111', '001', '010'], lowest_hamming_edge: {'001', 1}, 
	node: 001, reachable nodes: ['101', '011', '000'], lowest_hamming_edge: {0, '000'}, 
	node: 000, reachable nodes: ['100', '010', '001'], lowest_hamming_edge: {'100', 1}, 
	node: 101, reachable nodes: ['001', '111', '100'], lowest_hamming_edge: {'001', 1}, 
	node: 100, reachable nodes: ['000', '110', '101'], lowest_hamming_edge: {0, '000'}, 
	node: 110, reachable nodes: ['010', '100', '111'], lowest_hamming_edge: {1, '010'}, 
	node: 111, reachable nodes: ['011', '101', '110'], lowest_hamming_edge: {'011', 2}]

	"""

	def helper(start, dimension):

		if dimension == 1:
			return [Node(start)]

		if eval(start[len(start)-1]) == 0:
			return helper(start + '1', dimension-1) + helper(start + '0', dimension-1)
		return helper(start + '0', dimension-1) + helper(start + '1', dimension-1)

	return helper('0', n) + helper('1', n)

def dfs(g, start_node, end_node):

	visited = []

	while not start_node == end_node:
		visited.append(start_node.lowest_hamming_edge[0])


class Node:

	def __init__(self, bitstr):
		self.bitstr = bitstr
		self.adjacent = self.adjacents() # maybe there is a way to set adjacents in graph function (alternating pattern...isolate single flips?)
		self.lowest_hamming_edge = {min(self.adjacent, key=hamming_weight), hamming_weight(min(self.adjacent, key=hamming_weight))}

	def adjacents(self):
		adjacents = []
		for i in range(len(self.bitstr)):
			flipped = 1 if eval(self.bitstr[i]) == 0 else 0
			adjacents.append(self.bitstr[:i] + str(flipped) + self.bitstr[i+1:])

		return adjacents

	def __repr__(self):
		return f'node: {self.bitstr}, reachable nodes: {self.adjacent}, lowest_hamming_edge: {self.lowest_hamming_edge}'














