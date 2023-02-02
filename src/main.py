from function_to_csv import main as function_to_csv
import csv_to_vtp
from graph_structure import Graph
from algorithms.reord import parse_csv, set_minimas, reord_algorithm
from algorithms.mst_algo import kruskal_mst, networkx_mst, watershed_msf
from algorithms.gradient_field import gradient_field_builder, watershed_gvf
import argparse
import math
import time

csv_paths = {
    "points" : "outputs/generated_csv/points.csv",
    "lines" : "outputs/generated_csv/lines.csv",
    "triangles" : "outputs/generated_csv/triangles.csv",
    "output": "outputs/generated_vtp/output_graph.vtu"
}

csv_reord_path = {
    "points" : "outputs/generated_csv/reord_points.csv",
    "lines" : "outputs/generated_csv/reord_lines.csv",
    "triangles" : "outputs/generated_csv/reord_triangles.csv",
    "output": "outputs/generated_vtp/reord_output_graph.vtu"
}

csv_dual_paths = {
    "points" : "outputs/generated_csv/points_dual.csv",
    "lines" : "outputs/generated_csv/lines_dual.csv",
    "output": "outputs/generated_vtp/output_dual_graph.vtu"
}

csv_mst_dual_paths = {
    "points" : "outputs/generated_csv/points_dual_mst.csv",
    "lines" : "outputs/generated_csv/lines_dual_mst.csv",
    "output": "outputs/generated_vtp/output_dual_graph_mst.vtu"
}

ws_gvf_dual_paths = {
    "points" : "outputs/generated_csv/points_gvf_dual_ws.csv",
    "lines" : "outputs/generated_csv/lines_gvf_dual_ws.csv",
    "triangles" : "outputs/generated_csv/triangles_gvf_dual_ws.csv",
    "output": "outputs/generated_vtp/output_gvf_dual_ws.vtu"
}

ws_msf_dual_paths = {
    "points" : "outputs/generated_csv/points_msf_dual_ws.csv",
    "lines" : "outputs/generated_csv/lines_msf_dual_ws.csv",
    "output": "outputs/generated_vtp/output_msf_dual_ws.vtu"
}

vector_paths = {
    "vectors" : "outputs/generated_csv/vectors.csv",
    "vectors_dir" : "outputs/generated_csv/vectors_dir.csv",
    "output": "outputs/generated_vtp/output_gvf.vtp"
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
        "-s", "--size", required=False, default = 9,
        help="Size of the grid. Default is 9",
        type=int
    )
    parser.add_argument(
        "-r", "--resolution", required=False, default = 1,
        help="Size of a single triangle edge. To make it higher, enter a value < 1. Default is 1.",
        type=float
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

    function_to_csv(step=args.resolution, size=args.size, function=wave_function)

    # Graph creation
    start_time = time.time()

    graph = Graph(2)
    graph = parse_csv(graph, csv_paths)
    csv_to_vtp.build_graph_mesh(csv_paths)

    print(f"Graph Creation in seconds: {(time.time() - start_time)}")

    # Revaluation
    start_time = time.time()

    graph = set_minimas(graph, mode=args.minimas, map=True)
    graph, dual_minima = reord_algorithm(graph, video=False)
    graph.convert_to_csv(csv_reord_path)

    print(f"Revaluation in seconds: {(time.time() - start_time)}")

    # Graph after revaluation
    start_time = time.time()

    dual_rev = graph.create_dual()
    dual_rev.convert_to_csv(csv_dual_paths)

    print(f"Dual graph Creation in seconds: {(time.time() - start_time)}")

    # Gradient field creation
    start_time = time.time()

    seen_edges_pts = gradient_field_builder(dual_rev, vector_paths)
    # Ultimate collapse
    ws_gvf_graph = watershed_gvf(graph, seen_edges_pts)
    ws_gvf_graph.convert_to_csv(ws_gvf_dual_paths)

    print(f"GVF in seconds: {(time.time() - start_time)}")

    # Application of MST
    start_time = time.time()

    # Prim's MST Algorithm
    dual_mst, dual_mst_comp = networkx_mst(dual_rev, dual_minima)
    dual_mst.convert_to_csv(csv_mst_dual_paths)
    # Watershed
    watershed = watershed_msf(graph, dual_mst_comp)
    watershed.convert_to_csv(ws_msf_dual_paths)

    print(f"MST in seconds: {(time.time() - start_time)}")

    # Generate vtu file
    csv_to_vtp.build_vector_glyph(vector_paths)
    csv_to_vtp.build_graph_mesh(csv_reord_path)
    csv_to_vtp.build_graph_mesh(csv_dual_paths)
    csv_to_vtp.build_graph_mesh(csv_mst_dual_paths)
    csv_to_vtp.build_graph_mesh(ws_gvf_dual_paths)
    csv_to_vtp.build_graph_mesh(ws_msf_dual_paths)

if __name__ == "__main__":
    main()
