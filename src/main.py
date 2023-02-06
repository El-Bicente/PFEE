from function_2d_to_csv import main as function_2d_to_csv
from function_3d_to_csv import main as function_3d_to_csv

import csv_to_vtp
from graph_structure import Graph
from algorithms.reord import parse_csv, set_minimas, reord_algorithm
from algorithms.mst_algo import kruskal_mst, networkx_mst, watershed_msf
from algorithms.gradient_field import gradient_field_builder, watershed_gvf
import argparse
import math
import time

csv_paths = {
    "points" : "src/outputs/generated_csv/{dim}/points.csv",
    "lines" : "src/outputs/generated_csv/{dim}/lines.csv",
    "triangles" : "src/outputs/generated_csv/{dim}/triangles.csv",
    # "tetras" : "src/outputs/generated_csv/{dim}/tetras.csv",
    "output": "src/outputs/generated_vtp/{dim}/output_graph.vtu"
}

csv_reord_path = {
    "points" : "src/outputs/generated_csv/{dim}/reord_points.csv",
    "lines" : "src/outputs/generated_csv/{dim}/reord_lines.csv",
    "triangles" : "src/outputs/generated_csv/{dim}/reord_triangles.csv",
    # "tetras" : "src/outputs/generated_csv/{dim}/reord_tetras.csv",
    "output": "src/outputs/generated_vtp/{dim}/reord_output_graph.vtu"
}

csv_dual_paths = {
    "points" : "src/outputs/generated_csv/{dim}/points_dual.csv",
    "lines" : "src/outputs/generated_csv/{dim}/lines_dual.csv",
    "output": "src/outputs/generated_vtp/{dim}/output_dual_graph.vtu"
}

csv_mst_dual_paths = {
    "points" : "src/outputs/generated_csv/{dim}/points_dual_mst.csv",
    "lines" : "src/outputs/generated_csv/{dim}/lines_dual_mst.csv",
    "output": "src/outputs/generated_vtp/{dim}/output_dual_graph_mst.vtu"
}

ws_gvf_dual_paths = {
    "points" : "src/outputs/generated_csv/{dim}/points_gvf_dual_ws.csv",
    "lines" : "src/outputs/generated_csv/{dim}/lines_gvf_dual_ws.csv",
    "triangles" : "src/outputs/generated_csv/{dim}/triangles_gvf_dual_ws.csv",
    "output": "src/outputs/generated_vtp/{dim}/output_gvf_dual_ws.vtu"
}

ws_msf_dual_paths = {
    "points" : "src/outputs/generated_csv/{dim}/points_msf_dual_ws.csv",
    "lines" : "src/outputs/generated_csv/{dim}/lines_msf_dual_ws.csv",
    "output": "src/outputs/generated_vtp/{dim}/output_msf_dual_ws.vtu"
}

vector_paths = {
    "vectors" : "src/outputs/generated_csv/{dim}/vectors.csv",
    "vectors_dir" : "src/outputs/generated_csv/{dim}/vectors_dir.csv",
    "output": "src/outputs/generated_vtp/{dim}/output_gvf.vtp"
}

def wave_function_2d(x, y):
    return math.sin(math.sqrt(x*x + y*y))

def wave_function_3d(x, y, z):
    return math.sin(math.sqrt(x*x + y*y + z*z))

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
        "-m", "--minimas", required=False, default = 1,
        help="Minima modes: - 0: inférieur strict - 1: inférieur ou égal - 2: minima isolés forcés avec inférieur strict - 3: minima isolés forcés avec inférieur ou égal",
        type=int
    )

    parser.add_argument(
        "-d", "--dimension", required=False, default = None,
        help="Dimension modes: - without arg: 2D plan - with arg: 3D volume",
    )

    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.dimension is None:
        dim = "2d"
        function_2d_to_csv(
            step=args.resolution,
            size=args.size,
            function=wave_function_2d,
            paths=csv_paths,
            dim=dim
        )
    else:
        dim = "3d"
        step = 1
        start_time = time.time()
        function_3d_to_csv.main(
            step=step,
            size={'x': args.size, 'y': args.size, 'z': args.size},
            paths=csv_paths,
            function=wave_function_3d
        )
        print("Volume creation: %s seconds" % (time.time() - start_time))
        

    # Graph creation
    start_time = time.time()

    graph = Graph(2 if dim == "2d" else 3)
    graph = parse_csv(graph, csv_paths, dim)
    csv_to_vtp.build_graph_mesh(csv_paths, dim)

    print(f"Graph Creation in seconds: {(time.time() - start_time)}")

    # Revaluation
    start_time = time.time()

    graph = set_minimas(graph, size=args.size, step=step, mode=args.minimas, dim=dim, map=True)
    graph, dual_minima = reord_algorithm(graph, dim, video=False)
    graph.convert_to_csv(csv_reord_path, dim)

    print(f"Revaluation in seconds: {(time.time() - start_time)}")

    # Graph after revaluation
    start_time = time.time()

    dual_rev = graph.create_dual()
    dual_rev.convert_to_csv(csv_dual_paths, dim)

    print(f"Dual graph Creation in seconds: {(time.time() - start_time)}")

    # Gradient field creation
    start_time = time.time()

    seen_edges_pts = gradient_field_builder(dual_rev, vector_paths, dim)
    # Ultimate collapse
    ws_gvf_graph = watershed_gvf(graph, seen_edges_pts)
    ws_gvf_graph.convert_to_csv(ws_gvf_dual_paths, dim)

    print(f"GVF in seconds: {(time.time() - start_time)}")

    # Application of MST
    start_time = time.time()

    # Prim's MST Algorithm
    dual_mst, dual_mst_comp = networkx_mst(dual_rev, dual_minima)
    dual_mst.convert_to_csv(csv_mst_dual_paths, dim)
    # Watershed
    watershed = watershed_msf(graph, dual_mst_comp)
    watershed.convert_to_csv(ws_msf_dual_paths, dim)

    print(f"MST in seconds: {(time.time() - start_time)}")

    # Generate vtu file
    csv_to_vtp.build_vector_glyph(vector_paths, dim)
    csv_to_vtp.build_graph_mesh(csv_reord_path, dim)
    csv_to_vtp.build_graph_mesh(csv_dual_paths, dim)
    csv_to_vtp.build_graph_mesh(csv_mst_dual_paths, dim)
    csv_to_vtp.build_graph_mesh(ws_gvf_dual_paths, dim)
    csv_to_vtp.build_graph_mesh(ws_msf_dual_paths, dim)

if __name__ == "__main__":
    main()
