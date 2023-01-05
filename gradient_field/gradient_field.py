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

def gradient_field_builder(graph: Graph, paths):
    csv_vector_file = ",X,Y,Z\n"
    csv_vector_dir_file = ",X,Y,Z\n"
    vector_id = 0
    seen_edges_pts = set([])

    for pos, smp in enumerate(graph.simplexes_id):
        if (smp.order != 0):
            continue
        for adj_smp_id in graph.adj[pos]:
            adj_smp = graph.simplexes_id[adj_smp_id]
            if smp.weight == adj_smp.weight:
                smp_centroid = smp.coords[0]
                adj_spm_centroid = adj_smp.get_centroid()

                csv_vector_file += f"{vector_id}, {smp_centroid.x}, {smp_centroid.y}, {smp_centroid.z}\n"
                csv_vector_dir_file += f"{vector_id}, {adj_spm_centroid.x - smp_centroid.x}, {adj_spm_centroid.y - smp_centroid.y}, {adj_spm_centroid.z - smp_centroid.z}\n"
                vector_id += 1

                start_pt, end_pt = graph.adj[adj_smp_id]
                start_pt, end_pt = graph.simplexes_id[start_pt], graph.simplexes_id[end_pt]

                if (start_pt.weight != end_pt.weight):
                    seen_edges_pts.add(adj_spm_centroid)
                    seen_edges_pts.add(start_pt.coords[0])
                    seen_edges_pts.add(end_pt.coords[0])

    with open(paths["vectors"], "w") as vectors_file:
        vectors_file.write(csv_vector_file)

    with open(paths["vectors_dir"], "w") as vectors_dir_file:
        vectors_dir_file.write(csv_vector_dir_file)

    return seen_edges_pts
