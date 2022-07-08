from graph import Graph

def pairing(u, v):
    return round(0.5 * (u + v) * (u + v + 1) + v)

# custom .index (see explanations below)
def get_position(list, searched_value):
    pos = 0
    for elt in list:
        if elt == searched_value:
            return (True, pos)
        pos += 1
    return (False, pos)

# => remove redundancy
def get_vertex_pos(vertices_pair, weight, ids, weights):
    # sort the pair of vertices and unpack it
    # => we don't want to create 2 vertices for the same edge (ex : (u, v) == (v, u))
    vertex_id = pairing(*sorted([vertices_pair[0], vertices_pair[1]]))

    # when the element is not found, I wanted to have the size of 
    # the list without calling len() => avoid operations
    # .index can not do that :/
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
                # we don't want to see the same edge from opposite side
                if u == w:
                    continue

                first_vertex_pos = get_vertex_pos((u, v), weight1, ids, weights)
                second_vertex_pos = get_vertex_pos((v, w), weight2, ids, weights)

                new_edges.append((first_vertex_pos, second_vertex_pos, graph.vertex_weights[v]))

    # I add the possibility to add new edges directly in the constructor
    # It's cleaner in my opinion
    dual_graph = Graph(weights, new_edges)

    return dual_graph

graph = Graph([6, 4, 5])
graph.add_edge(0, 2, 4)
graph.add_edge(1, 0, 8)

dual_graph = get_edge_weighted_dual_graph(graph)

print("============ DUAL GRAPH VERTIX WEIGHTS ============")
for vertex, value in enumerate(dual_graph.vertex_weights):
    # f-strings are cool if you don't know it, adopt it !
    # only available in latest versions of python
    print(f"{vertex}: {value}")

print("============ DUAL GRAPH ADJACENT LIST ============")
for vertex, list in enumerate(dual_graph.adjlist):
    print(f"{vertex}: {list}")