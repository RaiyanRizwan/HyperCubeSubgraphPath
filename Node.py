class Node:

    def __init__(self, value: int, dim: int):
        self.value = value
        self.bitstr = str(format(self.value, f'0{dim}b'))
        self.hamming_weight = sum([eval(e) for e in self.bitstr])

    def __repr__(self):
        return f'{self.bitstr}'

    def __eq__(self, other_node):
        return self.value == other_node.value
        
    def __hash__(self):
        return self.value
    
    def hamming_distance(self, other):
        return abs(self.hamming_weight - other.hamming_weight)