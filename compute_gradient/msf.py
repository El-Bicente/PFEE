

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

    # def revaluation(self):
    #     G = dual(K)
    #     F_prime = F
    #     deja_vu = minima(F) #union of all minima
    #     G_past = subgraph(G)

    #     for l in N

def pairing(u, v):
    return round(0.5 * (u + v) * (u + v + 1) + v)

def get_position(list, searched_value):
    pos = 0
    for elt in list:
        if elt == searched_value:
            return (True, pos)
        pos += 1
    return (False, pos)

def get_vertex_pos(vertices_pair, weight, ids, weights):
    vertex_id = pairing(*sorted([vertices_pair[0], vertices_pair[1]]))
    (is_found, vertex_pos) = get_position(ids, vertex_id)
    if not is_found:
        ids.append(vertex_id)
        weights.append(weight)

    return vertex_pos

def get_edge_weighted_dual_graph(graph):
    new_edges = []
    ids = []
    weights = []

    adjlist = graph.adjlist.copy()
    for u, neighbors in enumerate(adjlist):
        for v, weight1 in neighbors:
            for w, weight2 in graph.adjlist[v]:
                if u == w:
                    continue

                first_vertex_pos = get_vertex_pos((u, v), weight1, ids, weights)
                second_vertex_pos = get_vertex_pos((v, w), weight2, ids, weights)

                new_edges.append((first_vertex_pos, second_vertex_pos, graph.vertex_weights[v]))

    dual_graph = Graph(weights, new_edges)

    return dual_graph

graph = Graph([6, 4, 5])
graph.add_edge(0, 2, 4)
graph.add_edge(1, 0, 8)

dual_graph = get_edge_weighted_dual_graph(graph)

print("============ DUAL GRAPH VERTIX WEIGHTS ============")
for vertex, value in enumerate(dual_graph.vertex_weights):
    print(f"{vertex}: {value}")

print("============ DUAL GRAPH ADJACENT LIST ============")
for vertex, list in enumerate(dual_graph.adjlist):
    print(f"{vertex}: {list}")