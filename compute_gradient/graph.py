from dual import get_edge_weighted_dual_graph

class Graph:
    def __init__(self, vertices, edges = []):
        self.V = len(vertices)
        self.vertex_weights = vertices

        self.adjlist = [[] for _ in range(self.V)]
        for u, v, w in edges:
            self.add_edge(u, v, w)

    def add_edge(self, u, v, w):
        if (v,w) not in self.adjlist[u]:
            self.adjlist[u].append((v, w))

        if (u,w) not in self.adjlist[v]:
            self.adjlist[v].append((u, w))

    def revaluation(self):
        G = get_edge_weighted_dual_graph(self)