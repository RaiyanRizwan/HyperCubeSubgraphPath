import heapq

class Fringe:
    
    def __init__(self, nodes_decimal: list):
        self.heap = [FringeTuple(node_decimal, float('inf')) for node_decimal in nodes_decimal]
        self.fringe_tuple_dict = {fringe_tuple.vertex : fringe_tuple for fringe_tuple in self.heap}
        
    def __bool__(self):
        return bool(self.heap)
        
    def push(self, v, d):
        if v in self.fringe_tuple_dict:
            self.fringe_tuple_dict[v].outdated = True
        heapq.heappush(self.heap, FringeTuple(v, d))
        
    def pop(self):
        while self.heap:
            smallest = heapq.heappop(self.heap)
            if not smallest.outdated:
                return smallest
        return None
    
    def remove(self, v):
        self.fringe_tuple_dict[v].outdated = True
    
class FringeTuple:
        
        def __init__(self, v, dist):
            self.vertex = v
            self.distance = dist
            self.outdated = False
        
        def __lt__(self, other):
            return self.distance < other.distance
        
        def __eq__(self, other):
            return self.vertex == other.vertex
    