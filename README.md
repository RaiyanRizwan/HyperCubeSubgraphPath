# HyperCubeDFS

***
NOTE: After taking a course on data structures and algorithms (CS61B @ Berkeley), I have realized that this shortest path algorithm is not depth first search. While it began as DFS, it is a much more efficient, specialized shortest path algorithm that doesn't follow a route to its deepest extent (DFS) but rather, systematically pursuses the target node based on hamming weight, backtracking only when necessary... Full refactor coming soon.
***

I was presented with finding the best way to construct and represent data for an n-dimensional HyperCube/graph, and to later write an efficient DFS (depth first search) algorithm for navigating any subgraph of the cube. 

### Initial Approach
You can peek into how my brain works in the comments at the bottom of [V1](DFS_Hamming_Cube_V1.py), which describe in detail how I systematically built up the data structures.

My initial approach was to tree recursively create permutations of bitstrings in n-dimensional space. For example, for a 3d hypercube, nodes are bitstrings of size 3 (i.e. 000), and there are 8 (2^n) of them. Each 'adjacent' node is connected by an edge, where adjacency is defined by a single bit flip. Thus, you can begin with the '0' and '1' bitstrings, and then pop on a '0' or '1' to each of those, and so on until you are n-levels deep. This procedure is described in graph_hax_initial_approach_.py.

### Problems & OOP Solution

However, there is a real need to treat these nodes as objects in order to be able to easily manipulate and reference them for DFS. The **main issue with meshing OOP and my previous methodology** of building up the nodes is that every node object needs to have a list of its neighbors (reachable nodes) as an instance attribute. However, when intializing the first couple of nodes there is limited information available about the rest of the cube. Think of localization and mapping; how does a node know where it is before it's space is defined? I solved this issue by creatively adapting the very procedure via which I build up the graph. 

### HyperCube/Node Initialization Algorithm Pseudocode:

Graph class
- nodes list
- dfs method

Node class
- bitstring
- neighbor nodes list

1. create the all-zero bitstring node, add it to the graph object, compute_neighbors()
2. compute_neighbors() --> create a new_node object by flipping each bit of the previous_node (all-zero in this case) and check whether new_node is in the graph: {loop code below for each bit flip}
    * if new_node is not in the graph, add it. then call new_node.compute_neighbors()
    * if new_node is in the graph (avoid double creation), add new_node to previous_node's neighbors list, and previous_node to new_node's neighbors list 
3. eventually expand out to the full cube!

This method systematically builds up the graph while simultaneously assigning neighbors to nodes as they're created (and via recursion, goes back to complete previously unfinished neighbor lists with minimal computation). This is a much more efficient approach to first creating the entire graph and then cycling and filtering through the nodes in order to fill neighbor lists and define edges. You can think of the process as starting at an arbitrary corner of the theoretical hypercube and building out exhausistively in one direction and then the next (each time storing node objects in neighbors lists without any kind of searching or excess recursion).

### DFS Algo

The idea behind the **DFS algorithm** is relatively simple, though it took me a while to write from scratch based on some graph theory YT videos and the concept of hamming weight. Pseudocode:

variables:
start_node - current location
target_node - target location
path - list of nodes traversed so far, initialized to [start_node]
black_list - list of nodes that can't lead to target_node, initialized to []

1. IF the end_goal_node is within the neighbors list of the start_node, return that path. ELSE 2.
2. IF all of the neighbors of the start_node are on black_list, return 'no path'. ELSE 3.
3. IF start_node has reachable neighbors that are not all on path + black_list, 4. ELSE 6.
4. Calculate the hamming weights of each neighbor_node in the start_node's neighbors list, and visit the optimal_node (closest hamming weight to end_goal_node) IF it has not been visited already (path) and it's not on black_list. ELSE, visit the next most optimal_node, and so on. IF all possible neighbor nodes have been visited or are black listed and there is no path to the end goal, return 'no path'. ELSE 5.
5. Perform the same procedure as 2. where start_node is set to the optimal_node we just traversed to and appended to path. 
6. Blacklist start_node and set start_node = the last visited node. This way, start_node will never be visited again and we can begin traversal from where we were before. Also pop blacklisted node from path (doesn't lead to target), and loop back to perform 2. 

In this way, the search algorithm returns the most efficient possible path to the end goal, without recursive processing. 

## Conclusions:
This project took me about 5-7 hours. I was very, very surprised that the algorithms worked! I've never written a DFS algorithm before or had any exposure to translating hypercube theory to code. The purpose of this project was to establish a classical, prerequisite example of the HyperCube Path problem before approaching it in the quantum space with hybrid Grover's algorithm optimization, as outlined in a research paper I'm co-debreifing for a QC DeCal at Berkeley. The classical DFS is pretty fast, though perhaps slower for randomly generated subgraph simulations- which I'll be working on next! However, classical hardware and exponential (or perhaps higher) time complexity limits us to testing the program on 9 or 10 dimensional hypercubes (which is still mind-blowing to me). A quantum approach to NP complete problems should change that, with any luck.

## Random Subgraph Update
Added subgraph function to Graph class that randomly eliminates the given number of edges from the graph, notably making clever use of the iterator-nature of for loops. Pleased to see that DFS and all other functionality still works as intended.

## DFS for Random Subgraph Update
The old DFS function (who's algo has been copy-pasted below and replaced above) didn't quite work in the more complex cases of the random subgraph update. In particular, the implementation of DFS backtracking after exhaustively searching a route wasn't working. Acknowledging the introduction of intermediate island nodes and non-hamming cycles within the cube were key realizations in updating the function, which now uses a blacklist system to reroute until all possible routes are either blacklisted or recently visited (at which point no path exists) or the target node is reached. Note: the new algo is described above in the DFS algo section, and is still not recursive.

Old pseudocode for DFS:
1. If the end_goal_node is within the neighbors list of the start_node, return that path. 
2. Otherwise, calculate the hamming weights of each neighbor_node in the start_node's neighbors list, and visit the optimal_node (closest hamming weight to end_goal_node) if it has not been visited already. If it has been visited, visit the next most optimal_node, and so on, unless all possible neighbor nodes have been visited and there is no path to the end goal. 
3. Then, perform the same procedure as ii. starting @ the optimal node we just traversed to, and keeping track of the path so far. 

The old material can still be accessed via V1.
