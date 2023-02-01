from graph_structure import Graph, Coordinates
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

def networkx_mst(G, dual_minima):
    Gnet = nx.Graph()

    for edge in G.simplexes[1]:
        neighboors = [G.simplexes_id[point_id] for point_id in G.adj[edge.ID]]
        u = neighboors[0]
        v = neighboors[1]
        w = edge.weight
        Gnet.add_edge(u.ID, v.ID, weight = w)

    inf_node_id = len(G.simplexes_id)
    for m in dual_minima:
        Gnet.add_edge(m, inf_node_id, weight = -1)

    mst_net = nx.minimum_spanning_tree(Gnet, algorithm="prim")

    result = Graph(G.order)
    comp = Graph(G.order)
    for u, v in Gnet.edges:
        if u == inf_node_id or v == inf_node_id:
            continue
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

def watershed_msf(primal: Graph, msf_cut: Graph):
    # Initialization of a set containing all centroids of the edges
    # They are used to find the corresponding primal edges
    edges_centroid = set(edge.get_centroid() for edge in msf_cut.simplexes[1])

    # The watershed is the closure of all critical n-1 faces
    watershed = Graph(primal.order - 1)

    # Adding all simplexes included in the closure
    # TODO Check if they are wrong matches of centroids
    for edge_primal in primal.simplexes[primal.order - 1]:
        if edge_primal.get_centroid() not in edges_centroid:
            continue

        for neighbor_id in primal.adj[edge_primal.ID]:
            neighbor = primal.simplexes_id[neighbor_id]
            if neighbor.order >= (primal.order - 1):
                continue
            coords = neighbor.coords[0].copy()
            watershed.add_simplex([coords], neighbor.weight)

        edge_closure = primal.simplexes_id[edge_primal.ID]
        watershed.add_simplex([edge_closure.coords[0].copy(), edge_closure.coords[1].copy()], edge_closure.weight)

    return watershed
