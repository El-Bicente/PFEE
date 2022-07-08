from dual import get_edge_weighted_dual_graph
from minima import get_minimas, get_subgraph_from_simplices
from graph import Graph

def revaluation(graph: Graph):
    dual_graph = get_edge_weighted_dual_graph(graph)
    visited_simplices = get_minimas(dual_graph)
    dual_subgraph = get_subgraph_from_simplices(dual_subgraph.vertex_number, visited_simplices)

    ### INIT QUEUE
    queue = []
    for m in visited_simplices:
        if len(m) == 2:
            for neighbor, edge_weight in dual_graph.adjlist[m[0]]:
                cost = edge_weight - m[1] # Cost = F (h) − F (m)
                h = (*sorted([m[0], neighbor]), edge_weight)
                if h not in visited_simplices and cost >= 0:
                    queue.append(((m, h), cost))
        elif len(m) == 3:
            cost = graph.vertex_weights[m[0]] - m[2] # Cost = F (h) − F (m)
            h = (m[0], graph.vertex_weights[m[0]])
            if h not in visited_simplices and cost >= 0:
                queue.append(((m, h), cost))

            cost = graph.vertex_weights[m[1]] - m[2] # Cost = F (h) − F (m)
            h = (m[1], graph.vertex_weights[m[1]])
            if h not in visited_simplices and cost >= 0:
                queue.append(((m, h), cost))
        else:
            ValueError(f"Simplex of dim {len(m)} is not managed. See ||{m}||")

    ### Propagation until the queue is empty
    count = 1
    while queue:
        # pop values
        max_cost = max(queue, key = lambda elt: elt[1])[1]
        for index, ((a, b) , cost) in enumerate(queue):
            if max_cost == cost:
                queue.pop(index)
        
        if a not in visited_simplices or b not in visited_simplices:
            cost = b[-1] - a[-1]
            queue.append(((a, b), cost))
            visited_simplices.add(a)
            visited_simplices.add(b)

            # The three next lines are for pairing
            v = count
            count += 1
