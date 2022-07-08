from graph import Graph

def get_minimas(graph: Graph):
    minimas = []
    visited_edges = []

    # browse vertex
    for vertex, vertex_weight in enumerate(graph.vertex_weights):
        # check neighbor values (edges)
        is_vertex_minima = True
        for neighbor, edge_weight in graph.adjlist[vertex]:
            # see with Boutry/article if we want <= or < for minimas
            if is_vertex_minima and vertex_weight > edge_weight:
                is_vertex_minima = False

            if (checked_edge := tuple(sorted([vertex, neighbor]))) not in visited_edges:
                visited_edges.append(checked_edge)
                if (
                    edge_weight <= vertex_weight
                    and edge_weight <= graph.vertex_weights[neighbor]
                ):
                    minimas.append((*checked_edge, edge_weight))
                    if edge_weight < vertex_weight:
                        break

        if is_vertex_minima:
            minimas.append((vertex, vertex_weight))

    return minimas

### TEST 1
graph1 = Graph([0, 10, 5])
graph1.add_edge(0, 2, 4)
graph1.add_edge(1, 0, 8)

minimas1 = get_minimas(graph1)

assert len(minimas1) == 1
assert minimas1[0] == (0, 0)

### TEST 2
graph2 = Graph([0, 10, 5])
graph2.add_edge(0, 2, 4)
graph2.add_edge(1, 0, 8)
graph2.add_edge(1, 2, 1)

minimas2 = get_minimas(graph2)

assert len(minimas2) == 2
assert minimas2[0] == (0, 0)
assert minimas2[1] == (1, 2, 1)