import math

class Graph:
    def __init__(self):
        self._vertices = []
        self._adjacencies = {}

    def add_node(self, node):
        if not node in self._vertices:
            self._vertices.append(node)
            self._adjacencies[node] = {}
            
    def add_edge(self, left, right, weight=1, directed=False):
        for node in [left, right]:
            self.add_node(node)
                
        self._adjacencies[left][right] = weight
        if not directed:
            self._adjacencies[right][left] = weight
            
    def remove_edges(self, left):
        if left in self._adjacencies:
            self._adjacencies[left] = {}

    def vertices(self):
        return self._vertices[:]

    def adjacencies(self, node):
        return self._adjacencies[node] if node in self._adjacencies else None

    def weight(self, left, right):
        if left in self._adjacencies and right in self._adjacencies[left]:
            return self._adjacencies[left][right]

        return float('inf')

    def areAdjacencies(self, left, right):
        return (left in self._adjacencies and
                right in self._adjacencies[left] and
                math.isfinite(self._adjacencies[left][right]))
        
    def __repr__(self) -> str:
        return str(self._adjacencies)
