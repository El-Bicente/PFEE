from reord.graph_structure import Graph, Coordinates
import networkx as nx

def graph_to_tup(G, is_weight = False):
    res = []
    for edge in G.simplexes[1]:
        neighboors = [G.simplexes_id[point_id] for point_id in G.adj[edge.ID]]
        u = neighboors[0]
        v = neighboors[1]
        if is_weight:
            res.append((u.ID, v.ID, edge.weight))
        else:
            res.append((u.ID, v.ID))
    return res

def networkx_mst(G):
    Gnet = nx.Graph()
    for edge in G.simplexes[1]:
        neighboors = [G.simplexes_id[point_id] for point_id in G.adj[edge.ID]]
        u = neighboors[0]
        v = neighboors[1]
        w = edge.weight
        Gnet.add_edge(u.ID, v.ID, weight = w)
    mst_net = nx.minimum_spanning_tree(Gnet)

    result = Graph(G.order)
    comp = Graph(G.order)
    for u, v in Gnet.edges:
        node1 = G.simplexes_id[u]
        node2 = G.simplexes_id[v]

        if ((u, v) in mst_net.edges):
            result.add_simplex([node1.coords[0].copy()], node1.weight)
            result.add_simplex([node2.coords[0].copy()], node2.weight)
            result.add_simplex([node1.coords[0].copy(),
                                node2.coords[0].copy()], weight = Gnet[u][v]["weight"])
        else:
            comp.add_simplex([node1.coords[0].copy()], node1.weight)
            comp.add_simplex([node2.coords[0].copy()], node2.weight)
            comp.add_simplex([node1.coords[0].copy(),
                                node2.coords[0].copy()], weight = Gnet[u][v]["weight"])

    return result, comp



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
