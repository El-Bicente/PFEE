from typing import Callable
from reord.graph_structure import Coordinates
from enum import IntEnum
import math
import pandas as pd

class Side(IntEnum):
    FRONT = 1
    LEFT = 2
    TOP = 3

def wave_function(coords: Coordinates):
    return math.sin(math.sqrt((coords.x ** 2) + (coords.y ** 2) + (coords.z ** 2)))

class DataCSV:
    def __init__(self) -> None:
        self.vertices: str = "Node Number,X,Y,Z,Weight\n"
        self.edges: str = "P1,P2,Weight\n"
        self.faces: str = "S1,S2,S3,Weight\n"
        self.tetras: str = "S1,S2,S3,S4,Weight\n"

class VolumeData:
    def __init__(self, function: Callable, cube_size: int = 1) -> None:
        self.vertices: pd.DataFrame = pd.DataFrame(columns=["x", "y", "z"])
        self.simplexes: set = set() # of order 2 or more
        self.last_index = -1
        self.csv: DataCSV = DataCSV()
        self.function = function
        self.cube_size = 1 if cube_size < 0 else cube_size
        self.units = {
            'u' : Coordinates((self.cube_size, 0, 0)),
            'v' : Coordinates((0, self.cube_size, 0)),
            'w' : Coordinates((0, 0, self.cube_size))
        }
        self.current_cube_sides = {}

    def add_vertex(self, vertex: Coordinates):
        if not (index := self.get_vertex_id(vertex)):
            new_vertex = pd.DataFrame.from_records([{'x': vertex.x, 'y': vertex.y, 'z': vertex.z}])
            self.vertices = pd.concat([self.vertices, new_vertex], ignore_index=True)
            self.last_index += 1
            self.csv.vertices += f"{self.last_index}, {vertex.x}, {vertex.y}, {vertex.z}, {self.function(vertex)}\n"
            return self.last_index

        return index

    def get_vertex_id(self, coordinates: Coordinates):
        row = self.vertices[(self.vertices.x == coordinates.x) & (self.vertices.y == coordinates.y) & (self.vertices.z == coordinates.z)]
        # row = [] si rien n'est trouvé
        if not row.empty:
            # row.index renvoie Int64Index([5], dtype='int64')
            return row.index[0]
        return None

    def has_simplex(self, ids: set[int]):
        return ids in self.simplexes

    def add_simplex(self, ids: set[int]):
        if not (res := self.has_simplex(ids)):
            self.simplexes.add(frozenset(ids))
        return res

    def save_csv(self, path: str):
        for body_filename in ["vertices", "edges", "faces", "tetras"]:
            with open(path + body_filename + ".csv", "w") as csv_file:
                csv_file.write(getattr(self.csv, body_filename))


def create_cube_vertices(volume_data: VolumeData, starting_pos: Coordinates, is_reversed: bool):
    """
    volume_data: VolumeData => main structure that contains important information
    starting_pos: Coordinates => starting position of the cube

    Return: dict of vertices ids
    """

    u, v, w = volume_data.units['u'], volume_data.units['v'], volume_data.units['w']
    if not is_reversed:
        cube_vertices = {                                               # Example:
            'A': (starting_pos, {Side.FRONT.value, Side.LEFT.value, Side.TOP.value}),     # A (0, 0, 0)
            'B': (starting_pos + u, {Side.LEFT.value, Side.TOP.value}),             # B (1, 0, 0)
            'C': (starting_pos + v, {Side.FRONT.value, Side.TOP.value}),            # C (0, 1, 0)
            'D': (starting_pos + (u + v), {Side.TOP.value}),                  # D (1, 1, 0)
            'E': (starting_pos + w, {Side.FRONT.value, Side.LEFT.value}),           # E (0, 0, 1)
            'F': (starting_pos + (u + w), {Side.LEFT.value}),                 # F (1, 0, 1)
            'G': (starting_pos + (v + w), {Side.FRONT.value}),                # G (0, 1, 1)
            'H': (starting_pos + (u + v + w), {}),                      # H (1, 1, 1)
        }
    else:
        cube_vertices = {
            'A': (starting_pos + v, {Side.FRONT.value, Side.TOP.value}),
            'B': (starting_pos + (u + v), {Side.TOP.value}),
            'C': (starting_pos, {Side.FRONT.value, Side.LEFT.value, Side.TOP.value}),
            'D': (starting_pos + u, {Side.LEFT.value, Side.TOP.value}),
            'E': (starting_pos + (v + w), {Side.FRONT.value}),
            'F': (starting_pos + (u + v + w), {}),
            'G': (starting_pos + w, {Side.FRONT.value, Side.LEFT.value}),
            'H': (starting_pos + (u + w), {Side.LEFT.value}),
        }

    cube_vertices_ids = {}
    for key, (current_vertex, sides) in cube_vertices.items():
        cube_vertices_ids[key] = (volume_data.add_vertex(current_vertex), sides)

    return cube_vertices_ids

def create_weighted_simplex(volume_data: VolumeData, ids: list[tuple[int, set[int]]], is_tetra: bool = False):
    # If the simplex exists, don't add this one to csv
    if not is_tetra and not set.intersection(volume_data.current_cube_sides, *[id[1] for id in ids]):
        return ""

    mean_degree = len(ids)
    centroid = Coordinates((0, 0, 0))
    for current_id, _ in ids:
        coords_vertex_row = volume_data.vertices.loc[current_id]
        centroid.x += coords_vertex_row.x
        centroid.y += coords_vertex_row.y
        centroid.z += coords_vertex_row.z

    centroid.x /= mean_degree
    centroid.y /= mean_degree
    centroid.z /= mean_degree

    return ', '.join([str(id) for id, _ in ids]) + ', ' + str(volume_data.function(centroid)) + '\n'


def create_cube_edges(volume_data: VolumeData, cube_vertices_ids: dict[str, tuple[int, set[int]]]):
    edges = create_weighted_simplex(volume_data, [cube_vertices_ids['A'], cube_vertices_ids['B']])
    edges += create_weighted_simplex(volume_data, [cube_vertices_ids['A'], cube_vertices_ids['C']])
    edges += create_weighted_simplex(volume_data, [cube_vertices_ids['A'], cube_vertices_ids['E']])
    edges += create_weighted_simplex(volume_data, [cube_vertices_ids['B'], cube_vertices_ids['C']])
    edges += create_weighted_simplex(volume_data, [cube_vertices_ids['B'], cube_vertices_ids['E']])
    edges += create_weighted_simplex(volume_data, [cube_vertices_ids['C'], cube_vertices_ids['E']])

    edges += create_weighted_simplex(volume_data, [cube_vertices_ids['B'], cube_vertices_ids['H']])
    edges += create_weighted_simplex(volume_data, [cube_vertices_ids['C'], cube_vertices_ids['H']])
    edges += create_weighted_simplex(volume_data, [cube_vertices_ids['E'], cube_vertices_ids['H']])

    edges += create_weighted_simplex(volume_data, [cube_vertices_ids['B'], cube_vertices_ids['F']])
    edges += create_weighted_simplex(volume_data, [cube_vertices_ids['E'], cube_vertices_ids['F']])
    edges += create_weighted_simplex(volume_data, [cube_vertices_ids['F'], cube_vertices_ids['H']])

    edges += create_weighted_simplex(volume_data, [cube_vertices_ids['C'], cube_vertices_ids['G']])
    edges += create_weighted_simplex(volume_data, [cube_vertices_ids['E'], cube_vertices_ids['G']])
    edges += create_weighted_simplex(volume_data, [cube_vertices_ids['G'], cube_vertices_ids['H']])

    edges += create_weighted_simplex(volume_data, [cube_vertices_ids['B'], cube_vertices_ids['D']])
    edges += create_weighted_simplex(volume_data, [cube_vertices_ids['C'], cube_vertices_ids['D']])
    edges += create_weighted_simplex(volume_data, [cube_vertices_ids['D'], cube_vertices_ids['H']])

    volume_data.csv.edges += edges

def create_cube_faces(volume_data: VolumeData, cube_vertices_ids: dict):
    # MIDDLE TETRAHEDRON
    faces = create_weighted_simplex(volume_data, [cube_vertices_ids['B'], cube_vertices_ids['C'], cube_vertices_ids['E']])
    faces += create_weighted_simplex(volume_data, [cube_vertices_ids['B'], cube_vertices_ids['E'], cube_vertices_ids['H']])
    faces += create_weighted_simplex(volume_data, [cube_vertices_ids['B'], cube_vertices_ids['C'], cube_vertices_ids['H']])
    faces += create_weighted_simplex(volume_data, [cube_vertices_ids['C'], cube_vertices_ids['E'], cube_vertices_ids['H']])

    # TETRAHEDRON IN A
    faces += create_weighted_simplex(volume_data, [cube_vertices_ids['A'], cube_vertices_ids['B'], cube_vertices_ids['E']])
    faces += create_weighted_simplex(volume_data, [cube_vertices_ids['A'], cube_vertices_ids['C'], cube_vertices_ids['E']])
    faces += create_weighted_simplex(volume_data, [cube_vertices_ids['A'], cube_vertices_ids['B'], cube_vertices_ids['C']])

    # TETRAHEDRON IN D
    faces += create_weighted_simplex(volume_data, [cube_vertices_ids['D'], cube_vertices_ids['B'], cube_vertices_ids['C']])
    faces += create_weighted_simplex(volume_data, [cube_vertices_ids['D'], cube_vertices_ids['C'], cube_vertices_ids['H']])
    faces += create_weighted_simplex(volume_data, [cube_vertices_ids['D'], cube_vertices_ids['B'], cube_vertices_ids['H']])

    # # TETRAHEDRON IN F
    faces += create_weighted_simplex(volume_data, [cube_vertices_ids['F'], cube_vertices_ids['E'], cube_vertices_ids['H']])
    faces += create_weighted_simplex(volume_data, [cube_vertices_ids['F'], cube_vertices_ids['B'], cube_vertices_ids['E']])
    faces += create_weighted_simplex(volume_data, [cube_vertices_ids['F'], cube_vertices_ids['B'], cube_vertices_ids['H']])

    # # TETRAHEDRON IN G
    faces += create_weighted_simplex(volume_data, [cube_vertices_ids['G'], cube_vertices_ids['E'], cube_vertices_ids['H']])
    faces += create_weighted_simplex(volume_data, [cube_vertices_ids['G'], cube_vertices_ids['C'], cube_vertices_ids['E']])
    faces += create_weighted_simplex(volume_data, [cube_vertices_ids['G'], cube_vertices_ids['C'], cube_vertices_ids['H']])

    volume_data.csv.faces += faces

def create_cube_tetrahedrons(volume_data: VolumeData, cube_vertices_ids: dict):
    tetras = create_weighted_simplex(volume_data, [cube_vertices_ids['A'], cube_vertices_ids['B'], cube_vertices_ids['C'], cube_vertices_ids['E']], is_tetra = True)
    tetras += create_weighted_simplex(volume_data, [cube_vertices_ids['B'], cube_vertices_ids['C'], cube_vertices_ids['E'], cube_vertices_ids['H']], is_tetra = True)
    tetras += create_weighted_simplex(volume_data, [cube_vertices_ids['B'], cube_vertices_ids['E'], cube_vertices_ids['F'], cube_vertices_ids['H']], is_tetra = True)
    tetras += create_weighted_simplex(volume_data, [cube_vertices_ids['C'], cube_vertices_ids['E'], cube_vertices_ids['G'], cube_vertices_ids['H']], is_tetra = True)
    tetras += create_weighted_simplex(volume_data, [cube_vertices_ids['B'], cube_vertices_ids['C'], cube_vertices_ids['D'], cube_vertices_ids['H']], is_tetra = True)

    volume_data.csv.tetras += tetras

def build_cube_with_tetrahedrons(volume_data: VolumeData, starting_pos: Coordinates, is_reversed: bool):
    cube_vertices_ids = create_cube_vertices(volume_data=volume_data, starting_pos=starting_pos, is_reversed=is_reversed)
    create_cube_edges(volume_data=volume_data, cube_vertices_ids=cube_vertices_ids)
    create_cube_faces(volume_data=volume_data, cube_vertices_ids=cube_vertices_ids)
    create_cube_tetrahedrons(volume_data=volume_data, cube_vertices_ids=cube_vertices_ids)

def get_sides(x: int, y: int, z: int) -> set:
    current_sides = set()
    if x:
        current_sides.add(Side.FRONT.value)
    if y:
        current_sides.add(Side.LEFT.value)
    if z:
        current_sides.add(Side.TOP.value)

    return current_sides


# FIXME Think to succession of cubes. Their faces must match
def main(cube_size: int, volume_size: dict):
    volume_data = VolumeData(function=wave_function, cube_size=cube_size)

    starting_pos = Coordinates((0, 0, 0))
    for z in range(volume_size['z']):
        for y in range(volume_size['y']):
            for x in range(volume_size['x']):
                volume_data.current_cube_sides = get_sides(x, y, z)
                new_pos = starting_pos + (volume_data.units['u'] * x) + (volume_data.units['v'] * y) + (volume_data.units['w'] * z)
                is_reversed = ((z + y + x) % 2) == 1
                build_cube_with_tetrahedrons(volume_data=volume_data, starting_pos=new_pos, is_reversed=is_reversed)

    volume_data.save_csv("function_to_csv/csv_files/3D/")

if __name__ == "__main__":
    main(1, {'x': 2, 'y': 2, 'z': 2})