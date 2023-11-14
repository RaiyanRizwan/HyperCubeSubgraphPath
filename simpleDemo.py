from HyperCubeSearch import Graph

# --- DIM 4 ---
g = Graph(4)
print(f'4D Hypercube Adjacency List:\n{g}\n')
print(f'Path from 0000 to 1111 in 4D Hypercube:\n{g.path("0000", "1111")}\n')
g.subgraph(12)
print(f'4D Hypercube subgraph Adjacency List:\n{g}\n')
print(f'Path from 0000 to 1111 in 4D Hypercube subgraph:\n{g.path("0000", "1111")}\n')

# --- DIM 15 --- 
g = Graph(15, seed=5)
print(f'Path from {"0"*15} to {"1"*15} in 15D Hypercube:\n{g.path("0"*15, "1"*15)}\n')
g.subgraph(2e5)
print(f'Path from {"0"*15} to {"1"*15} in 15D Hypercube subgraph:\n{g.path("0"*15, "1"*15)}')
