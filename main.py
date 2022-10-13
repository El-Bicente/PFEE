from function_to_csv import function_to_csv
from format import csv_to_vtp
from reord.graph_structure import Graph
from reord.reord import parse_csv, set_minimas, reord_algorithm
from reord.mst_algo import kruskal_mst

function_to_csv.main(step=1, size=9, function=function_to_csv.wave_function)

csv_paths = {
    "points" : "function_to_csv/generated_csv/points.csv",
    "lines" : "function_to_csv/generated_csv/lines.csv",
    "triangles" : "function_to_csv/generated_csv/triangles.csv",
    "output": "format/generated_vtp/output_graph.vtu"
}

csv_dual_paths = {
    "points" : "function_to_csv/generated_csv/points_dual.csv",
    "lines" : "function_to_csv/generated_csv/lines_dual.csv",
    "output": "format/generated_vtp/output_dual_graph.vtu"
}
### Revaluation
graph = Graph(2)
graph = parse_csv(graph, csv_paths)
#graph = set_minimas(graph)
#graph = reord_algorithm(graph)
graph.convert_to_csv(csv_paths)
#Graphe avant revaluation
dual_non_rev, dual_non_rev_union_form = graph.create_dual(graph)
dual_non_rev.convert_to_csv(csv_dual_paths)
kruskal_mst(dual_non_rev, dual_non_rev_union_form)
### Generate vtu file
csv_to_vtp.main(csv_paths)
csv_to_vtp.main(csv_dual_paths)
