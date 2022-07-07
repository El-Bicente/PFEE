

class Graph:
    def __init__(self, vertices):
        self.V = len(vertices)
        self.vertices_weight = vertices
        self.adjlist = [[] for i in range(self.V)]

    def add_edge(self, u, v, w):
        if (v,w) not in self.adjlist[u]:
            self.adjlist[u].append((v, w))

        if (u,w) not in self.adjlist[v]:
            self.adjlist[v].append((u, w))

    # def revaluation(self):
    #     G = dual(K)
    #     F_prime = F
    #     deja_vu = minima(F) #union of all minima
    #     G_past = subgraph(G)

    #     for l in N

def pairing(u, v):
    return round(0.5 * (u + v) * (u + v + 1) + v)

def dual(graph):
    new_adjlist = []
    labels = []
    weights = []

    adjlist = graph.adjlist.copy()
    for u, neighbors in enumerate(adjlist):
        for v, weight in neighbors:
            for w, weight2 in graph.adjlist[v]:
                if not pairing(u, v) in labels:
                    labels.append(pairing(u, v))
                    weights.append(weight)

                if not pairing(v, w) in labels:
                    labels.append(pairing(v, w))
                    weights.append(weight2)

                new_adjlist.append((labels.index(pairing(u, v)), labels.index(pairing(v, w)), graph.vertices_weight[v]))

    dual_graph = Graph(weights)
    for u, v, w in new_adjlist:
        dual_graph.add_edge(u, v, w)

    return dual_graph

g = Graph([6, 4, 5])
g.add_edge(0, 2, 4)
g.add_edge(1, 0, 8)

print(dual(g).adjlist)
#print(g.adjlist)