# Hyper Cube Subgraph Path

11/19/23 Update

I implemented A*. To see the difference between the previous path algo and the current shortest path, run simpleDemo.py. Honestly, it was a lot of fun! I more practically, post CS61B, understand admissibility and consistency for heuristics. I chose hamming distance as a heuristic, since the actual path (in a subgraph) is always equal to or longer than the hamming distance between the current and target node (a similar argument can be made for consistency). Also, notably, there were some cheeky tricks I had to implement in order to update the priority queue in Python when relaxing edges (to not kill the runtime). 

11/05/23 Update

I decided to revist this code, which I wrote during the fall semester of my freshman year at Berkeley. Most of it is rewritten using concepts I learned in CS61B (hash maps, adjacency lists) and CS61C (binary). Whereas before I could only generate 10 dimensional hypercubes, I can now generate a 15 dimensional hypercube in 5 seconds. I can also find a path (if it exists) in any subgraph of the hyper cube from any bitstring to another. 

Graph generation: O(n2^n)

# Next Steps
Implement dynamic programming algorithm (path in subgraph O(2^n)). I read about this approach when I was reading _Quantum Speedups for Exponential-Time Dynamic Programming Algorithms_, as the best classical solve. After I take CS170 (next sem), I will update this repo yet again (or perhaps sooner). 
