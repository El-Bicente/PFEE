from function_to_csv import function_to_csv
from format import csv_to_vtp
from reord.graph_structure import Graph
from reord.reord import parse_csv, set_minimas, reord_algorithm
from reord.mst_algo import kruskal_mst
from gradient_field.gradient_field import gradient_field_builder, watershed_gvf
import argparse
import math
import time

csv_paths = {
    "points" : "function_to_csv/generated_csv/points.csv",
    "lines" : "function_to_csv/generated_csv/lines.csv",
    "triangles" : "function_to_csv/generated_csv/triangles.csv",
    "output": "format/generated_vtp/output_graph.vtu"
}

csv_reord_path = {
    "points" : "function_to_csv/generated_csv/reord_points.csv",
    "lines" : "function_to_csv/generated_csv/reord_lines.csv",
    "triangles" : "function_to_csv/generated_csv/reord_triangles.csv",
    "output": "format/generated_vtp/reord_output_graph.vtu"
}

csv_dual_paths = {
    "points" : "function_to_csv/generated_csv/points_dual.csv",
    "lines" : "function_to_csv/generated_csv/lines_dual.csv",
    "output": "format/generated_vtp/output_dual_graph.vtu"
}

csv_mst_dual_paths = {
    "points" : "function_to_csv/generated_csv/points_dual_mst.csv",
    "lines" : "function_to_csv/generated_csv/lines_dual_mst.csv",
    "output": "format/generated_vtp/output_dual_graph_mst.vtu"
}

ws_gvf_dual_paths = {
    "points" : "function_to_csv/generated_csv/points_gvf_dual_ws.csv",
    "lines" : "function_to_csv/generated_csv/lines_gvf_dual_ws.csv",
    "triangles" : "function_to_csv/generated_csv/triangles_gvf_dual_ws.csv",
    "output": "format/generated_vtp/output_gvf_dual_ws.vtu"
}

csv_comp_dual_paths = {
    "points" : "function_to_csv/generated_csv/points_dual_comp.csv",
    "lines" : "function_to_csv/generated_csv/lines_dual_comp.csv",
    "output": "format/generated_vtp/output_dual_graph_comp.vtu"
}

vector_paths = {
    "vectors" : "function_to_csv/generated_csv/vectors.csv",
    "vectors_dir" : "function_to_csv/generated_csv/vectors_dir.csv",
    "output": "format/generated_vtp/output_gvf.vtp"
}

def wave_function(x, y):
    return math.sin(math.sqrt(x*x + y*y))

def time_exec(func, name, *arg):
    start_time = time.time()
    res = func(*arg)
    print(f"{name} in seconds: {(time.time() - start_time)}")
    return res

def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="PFEE"
    )
    parser.add_argument(
        "-m", "--minimas", required=True,
        help="Minima modes: - 0: inférieur strict - 1: inférieur ou égal - 2: minima isolés forcés avec inférieur strict - 3: minima isolés forcés avec inférieur ou égal",
        type=int
    )

    return parser

def main():

    parser = get_parser()
    args = parser.parse_args()

    function_to_csv.main(step=1, size=9, function=wave_function)

    ### Graph creation
    start_time = time.time()

    graph = Graph(2)
    graph = parse_csv(graph, csv_paths)
    csv_to_vtp.build_graph_mesh(csv_paths)

    print(f"Graph Creation in seconds: {(time.time() - start_time)}")

    ### Revaluation
    start_time = time.time()

    graph = set_minimas(graph, mode=args.minimas, map=True)
    graph = reord_algorithm(graph, video=False)
    print(graph.get_map())
    graph.convert_to_csv(csv_reord_path)

    print(f"Revaluation in seconds: {(time.time() - start_time)}")

    #Graph after revaluation
    start_time = time.time()

    dual_rev = graph.create_dual()
    dual_rev.convert_to_csv(csv_dual_paths)

    print(f"Dual graph Creation in seconds: {(time.time() - start_time)}")

    #Gradient field creation
    start_time = time.time()

    seen_edges_pts = gradient_field_builder(dual_rev, vector_paths)
    ws_gvf_graph = watershed_gvf(graph, seen_edges_pts)
    ws_gvf_graph.convert_to_csv(ws_gvf_dual_paths)

    print(f"GVF in seconds: {(time.time() - start_time)}")

    #Application of mst
    start_time = time.time()

    dual_mst, dual_mst_comp = kruskal_mst(dual_rev)
    dual_mst.convert_to_csv(csv_mst_dual_paths)
    dual_mst_comp.convert_to_csv(csv_comp_dual_paths)

    print(f"MST in seconds: {(time.time() - start_time)}")

    ### Generate vtu file
    csv_to_vtp.build_vector_glyph(vector_paths)
    csv_to_vtp.build_graph_mesh(csv_reord_path)
    csv_to_vtp.build_graph_mesh(csv_dual_paths)
    csv_to_vtp.build_graph_mesh(csv_mst_dual_paths)
    csv_to_vtp.build_graph_mesh(ws_gvf_dual_paths)
    csv_to_vtp.build_graph_mesh(csv_comp_dual_paths)

    """
    ### Test

    graph = Graph(2)
    graph = parse_csv(graph, csv_paths)
    csv_to_vtp.build_graph_mesh(csv_paths)

    graph = set_minimas(graph, args.minimas, map=True)
    graph = reord_algorithm(graph, video=False)
    graph.convert_to_csv(csv_reord_path)
    csv_to_vtp.build_graph_mesh(csv_reord_path)
    """
if __name__ == "__main__":
    main()
