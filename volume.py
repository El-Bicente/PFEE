from function_to_csv import three_dim_function_to_csv2
from format import csv_to_vtp
from reord.graph_structure import Coordinates
import time
import math

csv_paths = {
    "points" : "function_to_csv/csv_files/3D/vertices.csv",
    "lines" : "function_to_csv/csv_files/3D/edges.csv",
    "triangles" : "function_to_csv/csv_files/3D/faces.csv",
    "tetras" : "function_to_csv/csv_files/3D/tetras.csv"
}

def wave_function(coords: Coordinates):
    return math.sin(math.sqrt((coords.x ** 2) + (coords.y ** 2) + (coords.z ** 2)))

start_time = time.time()
three_dim_function_to_csv2.main(step=1, size={'x': 10, 'y': 10, 'z': 10}, function=wave_function)
print("--- %s seconds ---" % (time.time() - start_time))
csv_to_vtp.main(csv_paths, generateTetras=True)