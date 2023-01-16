from reord.graph_structure import Graph


def watershed_gvf(primal: Graph, seen_edges_pts):
    ws_graph = Graph(primal.order)
    for pos, smp in enumerate(primal.simplexes_id):
        if (smp.order == 0):
            ws_graph.add_simplex([smp.coords[0].copy()], smp.weight)
        elif (smp.order == 1 and smp.get_centroid() not in seen_edges_pts):

            ws_graph.add_simplex([smp.coords[0].copy(), smp.coords[1].copy()], smp.weight)
        elif ((smp.get_centroid() not in seen_edges_pts) and (smp.weight != 0)):
            ws_graph.add_simplex([smp.coords[0].copy(), smp.coords[1].copy(), smp.coords[2].copy()], smp.weight)

    return ws_graph

"""for pos, smp in enumerate(graph.simplexes_id):
    if (smp.order != 1):
        continue

    smp_id = smp.ID
    if  smp_id not in seen_edges:
        start_pt, end_pt = graph.adj[smp_id]
        start_pt, end_pt = graph.simplexes_id[start_pt], graph.simplexes_id[end_pt]
        ws_graph.add_simplex([start_pt.coords[0].copy()], start_pt.weight)
        ws_graph.add_simplex([end_pt.coords[0].copy()], end_pt.weight)
        ws_graph.add_simplex([start_pt.coords[0].copy(), end_pt.coords[0].copy()], weight = smp.weight)
    seen_edges.add(smp_id)
"""

def gradient_field_builder(dual_graph: Graph, paths):
    csv_vector_file = ",X,Y,Z\n"
    csv_vector_dir_file = ",X,Y,Z\n"
    vector_id = 0
    seen_edges_pts = set([])

    for pos, smp in enumerate(dual_graph.simplexes_id):
        if (smp.order != 1):
            continue
        
        p1 = dual_graph.simplexes_id[dual_graph.adj[pos][0]]
        p2 = dual_graph.simplexes_id[dual_graph.adj[pos][1]]

        start_point, end_point = None, None

        if p1.weight == smp.weight:
            start_point, end_point = p2.coords[0], p1.coords[0]
        
        elif p2.weight == smp.weight:
            start_point, end_point = p1.coords[0], p2.coords[0]
        
        if start_point:
            csv_vector_file += f"{vector_id}, {start_point.x}, {start_point.y}, {start_point.z}\n"
            csv_vector_dir_file += f"{vector_id}, {end_point.x - start_point.x}, {end_point.y - start_point.y}, {end_point.z - start_point.z}\n"
            seen_edges_pts.add(start_point)
            seen_edges_pts.add(end_point)
            seen_edges_pts.add(smp.get_centroid())
            vector_id += 1

    with open(paths["vectors"], "w") as vectors_file:
        vectors_file.write(csv_vector_file)

    with open(paths["vectors_dir"], "w") as vectors_dir_file:
        vectors_dir_file.write(csv_vector_dir_file)
    
    return seen_edges_pts
