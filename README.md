# HyperCubeDFS

I was presented with finding the best way to construct and represent data for an n-dimensional HyperCube/graph, and to later write an efficient DFS (depth first search) algorithm for navigating any subgraph of the cube. 

You can see my initial thought process in the comments at the bottom of graph_hax.py, and how I systematically built up the data structures.

My initial approach was to tree recursively create permutations of bitstrings in n-dimensional space. For example, for a 3d hypercube, nodes are bitstrings of size 3 (i.e. 000), and there are 8 (2^n) of them. Each 'adjacent' node is connected by an edge, where adjacency is defined by a single bit flip. Thus, you can begin with the '0' and '1' bitstrings, and then pop on a '0' or '1' to each of those, and so on until you are n-levels deep. This procedure is described in graph_hax_ia.py.

However, there is a real need to treat these nodes as objects in order to be able to easily manipulate and reference them for DFS. The main issue with meshing OOP and my previous methodology of building up the nodes is that every node object needs to have a list of its neighbors (reachable nodes) as an instance attribute. However, when intializing the first couple of nodes there is limited information available about the rest of the cube. Think of localization and mapping; how does a node know where it is before it's space is defined? I solved this issue by creatively adapting the very procedure via which I build up the graph. Below is the algorithm pseudocode:

Graph class
- nodes list
- dfs method

Node class
- bitstring
- neighbor nodes list

1. create the all-zero bitstring node, add it to the graph object, compute_neighbors()
2. compute_neighbors() --> create a new_node object by flipping each bit of the previous_node (all-zero in this case) and check whether new_node is in the graph: (loop for each bit flip)
   3a. if new_node is not in the graph, add it. then call new_node.compute_neighbors()
   3b. if new_node is in the graph (avoid double creation), add new_node to previous_node's neighbors list, and previous_node to new_node's neighbors list
4. eventually expand out to the full cube!

This method systematically builds up the graph while simultaneously assigning neighbors to nodes as they're created (and via recursion, goes back to complete previously unfinished neighbor lists with minimal computation. This is much more efficient than first creating the graph and then cycling through the nodes in order to add single-bitflipped node objects to their neighbor lists. You can think of the process as starting at a corner of the hypercube and building out exhausistively in one direction and then the next (each time storing node objects in neighbors list without any kind of searching or excess recursion).

The idea behind the DFS algorithm is relatively simple, though it took me a while to write from scratch based only on theory. If the end_goal_node is within the neighbors list of the start_node, return that path. Otherwise, calculate the hamming weights of each neighbor_node in the start_node's neighbors list, and visit the optimal_node (closest hamming weight to end_goal_node) if it has not been visited already; otherwise visit the next most optimal_node, etc. etc. unless all nodes have been visited and there is no path. In this way, the search algorithm returns the most efficient possible path to the end goal, without recursive processing.

Conclusions:
This project took me about 5-7 hours. I was very, very surprised that the algorithms worked! I've never written a DFS algorithm before or had any exposure to translating hypercube theory to code. The purpose of this project was to establish a classical, prerequisite example of the HyperCube Path problem before approaching it in the quantum space with Grover's algorithm optimization, as outlined in a research paper I'm debreifing for a QC DeCal at Berkeley. The DFS is extremely fast, though perhaps slower for randomly generated subgraph simulations- which I'll be working on next! However, classical hardware and exponential (or perhaps higher) time complexity limits us to testing the program on 9 or 10 dimensional hypercubes (which is still mind-blowing to me).

