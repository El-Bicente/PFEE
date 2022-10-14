from reord.graph_structure import Graph, Coordinates

def kruskal_mst(G):
    result = Graph(G.order)
    comp = Graph(G.order)
    edges = sorted(G.simplexes[1], key = lambda x: x.weight)
    sets = {}

    for edge in edges:
        neighboors = [G.simplexes_id[point_id] for point_id in G.adj[edge.ID]]
        u = neighboors[0]
        v = neighboors[1]
        w = edge.weight

        node1_ID = result.add_simplex([u.coords[0].copy()], u.weight)
        node2_ID = result.add_simplex([v.coords[0].copy()], v.weight)
        if node1_ID not in sets:
            sets[node1_ID] = {node1_ID}
        if node2_ID not in sets:
            sets[node2_ID] ={node2_ID}

        if (node2_ID not in sets[node1_ID] and node1_ID not in sets[node2_ID]):
            result.add_simplex([u.coords[0].copy(), v.coords[0].copy()], weight = w)
            sets[node1_ID] = sets[node1_ID].union(sets[node2_ID])
            for elm in sets[node1_ID]:
                sets[elm] = sets[elm].union(sets[node1_ID])
                sets[node1_ID] = sets[node1_ID].union(sets[elm])

            sets[node2_ID] = sets[node2_ID].union(sets[node1_ID])
            for elm in sets[node2_ID]:
                sets[elm] = sets[elm].union(sets[node2_ID])
                sets[node2_ID] = sets[node1_ID].union(sets[elm])
        else:
            comp.add_simplex([u.coords[0].copy()], u.weight)
            comp.add_simplex([v.coords[0].copy()], v.weight)
            comp.add_simplex([u.coords[0].copy(), v.coords[0].copy()], weight = w)
    return result, comp
