from format import csv_to_vtp
from gradient_field.generate_csv import build_paper_example
from gradient_field.gradient_field import gradient_field_builder

csv_paths = {
    "points" : "format/csv_files/points.csv",
    "lines" : "format/csv_files/lines.csv",
    "triangles" : "format/csv_files/triangles.csv",
    "vectors" : "format/csv_files/vectors_pts.csv",
    "vectors_dir" : "format/csv_files/vectors_dir.csv"
}

# build graph
graph = build_paper_example()

# save it
graph.convert_to_csv(csv_paths)

# build vectors
gradient_field_builder(graph)

### Generate vtu file
csv_to_vtp.main(csv_paths, generateVectors=True)