from function_to_csv import function_to_csv
from format import csv_to_vtp
from reord.graph_structure import Graph
from reord.reord import parse_csv, set_minimas, reord_algorithm

function_to_csv.main(step=1, size=9, function=function_to_csv.wave_function)

csv_paths = {
    "points" : "function_to_csv/generated_csv/points.csv",
    "lines" : "function_to_csv/generated_csv/lines.csv",
    "triangles" : "function_to_csv/generated_csv/triangles.csv"
}

csv_dual_paths = {
    "points" : "function_to_csv/generated_csv/points_dual.csv",
    "lines" : "function_to_csv/generated_csv/lines_dual.csv",
}
### Revaluation
graph = Graph()
graph = parse_csv(graph, csv_paths)
graph = set_minimas(graph)
graph = reord_algorithm(graph)
graph.convert_to_csv(csv_paths)
#graph.convert_dual_to_csv(csv_paths)
### Generate vtu file
csv_to_vtp.main(csv_paths)
