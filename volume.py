from function_to_csv import three_dim_function_to_csv
from format import csv_to_vtp

csv_paths = {
    "points" : "function_to_csv/csv_files/3D/vertices.csv",
    "lines" : "function_to_csv/csv_files/3D/edges.csv",
    "triangles" : "function_to_csv/csv_files/3D/faces.csv",
    "tetras" : "function_to_csv/csv_files/3D/tetras.csv"
}

three_dim_function_to_csv.main()
csv_to_vtp.main(csv_paths, generateTetras=True)