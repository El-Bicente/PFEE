from function_to_csv import three_dim_function_to_csv
from format import csv_to_vtp
import time

csv_paths = {
    "points" : "function_to_csv/csv_files/3D/vertices.csv",
    "lines" : "function_to_csv/csv_files/3D/edges.csv",
    "triangles" : "function_to_csv/csv_files/3D/faces.csv",
    "tetras" : "function_to_csv/csv_files/3D/tetras.csv"
}

start_time = time.time()
three_dim_function_to_csv.main(1, {'x': 10, 'y': 10, 'z': 10})
print("--- %s seconds ---" % (time.time() - start_time))
csv_to_vtp.main(csv_paths, generateTetras=True)