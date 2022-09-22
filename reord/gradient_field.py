from generate_csv import build_paper_example
from graph_structure import Graph

graph = build_paper_example()

def gradient_field_builder(graph: Graph):
    csv_vector_file = ",X,Y,Z\n"
    csv_vector_dir_file = ",X,Y,Z\n"
    vector_id = 0
    for pos, smp in enumerate(graph.simplexes_id):
        if smp.order == 2:
            continue

        for adj_smp_id in graph.adj[pos]:
            adj_smp = graph.simplexes_id[adj_smp_id]
            if (smp.order + 1) == adj_smp.order and smp.weight == adj_smp.weight:
                smp_centroid = smp.get_centroid()
                adj_spm_centroid = adj_smp.get_centroid()
        
                csv_vector_file += f"{vector_id}, {smp_centroid.x}, {smp_centroid.y}, {smp_centroid.z}\n"
                csv_vector_dir_file += f"{vector_id}, {adj_spm_centroid.x - smp_centroid.x}, {adj_spm_centroid.y - smp_centroid.y}, {adj_spm_centroid.z - smp_centroid.z}\n"
                vector_id += 1

    with open("./generated_csv/vectors.csv", "w") as vectors_file:
        vectors_file.write(csv_vector_file)

    with open("./generated_csv/vectors_dir.csv", "w") as vectors_dir_file:
        vectors_dir_file.write(csv_vector_dir_file)

gradient_field_builder(graph)