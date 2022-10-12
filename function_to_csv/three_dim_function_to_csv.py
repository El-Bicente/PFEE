from reord.graph_structure import Coordinates
import math
import pandas as pd


def wave_function(coords: Coordinates):
    return math.sin(math.sqrt((coords.x ** 2) + (coords.y ** 2) + (coords.z ** 2)))

class DataCSV:
    def __init__(self) -> None:
        self.vertices: str = "Node Number,X,Y,Z,Weight\n"
        self.edges: str = "P1,P2,Weight\n"
        self.faces: str = "S1,S2,S3,Weight\n"
        self.tetras: str = "S1,S2,S3,S4,Weight\n"

class VolumeData:
    def __init__(self, function, cube_size = 1) -> None:
        self.vertices: pd.DataFrame = pd.DataFrame(columns=["x", "y", "z"])
        self.edges: set = set()
        self.faces: set = set()
        self.tetras: set = set()
        self.last_index = -1
        self.csv: DataCSV = DataCSV()
        self.function = function
        self.cube_size = 1 if cube_size < 0 else cube_size
        self.units = {
            'u' : Coordinates((self.cube_size, 0, 0)),
            'v' : Coordinates((0, self.cube_size, 0)),
            'w' : Coordinates((0, 0, self.cube_size))
        }

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

    def add_simplex(self, ids: list[int], weight: float):
        simplex_dim = len(ids) - 1
        smp_info = tuple(ids) + (weight,)
        if simplex_dim == 1:
            self.edges.add(smp_info)
        elif simplex_dim == 2:
            self.faces.add(smp_info)
        elif simplex_dim == 3:
            self.tetras.add(smp_info)

    def save_csv(self, path: str):
        with open(path + "vertices.csv", "w") as csv_vertices_file:
            csv_vertices_file.write(self.csv.vertices)

        for body_filename in ["edges", "faces", "tetras"]:
            csv_simplexes = getattr(self.csv, body_filename)
            for smp_info in getattr(self, body_filename):
                csv_simplexes += f'{",".join([str(x) for x in smp_info])}\n'
                
            with open(path + body_filename + ".csv", "w") as csv_file:
                csv_file.write(csv_simplexes)

def create_cube_vertices(volume_data: VolumeData, starting_pos: Coordinates, is_reversed: bool):
    """
    volume_data: VolumeData => main structure that contains important information
    starting_pos: Coordinates => starting position of the cube

    Return: dict of vertices ids
    """
    u, v, w = volume_data.units['u'], volume_data.units['v'], volume_data.units['w']
    if not is_reversed:
        cube_vertices = {                    # Example:
            'A': starting_pos,               # A (0, 0, 0)
            'B': starting_pos + u,           # B (1, 0, 0)
            'C': starting_pos + v,           # C (0, 1, 0)
            'D': starting_pos + (u + v),     # D (1, 1, 0)
            'E': starting_pos + w,           # E (0, 0, 1)
            'F': starting_pos + (u + w),     # F (1, 0, 1)
            'G': starting_pos + (v + w),     # G (0, 1, 1)
            'H': starting_pos + (u + v + w), # H (1, 1, 1)
        }
    else:
        cube_vertices = {
            'A': starting_pos + v,
            'B': starting_pos + (u + v),
            'C': starting_pos,
            'D': starting_pos + u,
            'E': starting_pos + (v + w),
            'F': starting_pos + (u + v + w),
            'G': starting_pos + w,
            'H': starting_pos + (u + w),
        }

    cube_vertivces_ids = {}
    for key, current_vertex in cube_vertices.items():
        cube_vertivces_ids[key] = volume_data.add_vertex(current_vertex)

    return cube_vertivces_ids

def create_weighted_simplex(volume_data: VolumeData, ids: list[int]):
    mean_degree = len(ids)
    centroid = Coordinates((0, 0, 0))
    for current_id in ids:
        coords_vertex_row = volume_data.vertices.loc[current_id]
        centroid.x += coords_vertex_row.x
        centroid.y += coords_vertex_row.y
        centroid.z += coords_vertex_row.z

    centroid.x /= mean_degree
    centroid.y /= mean_degree
    centroid.z /= mean_degree

    volume_data.add_simplex(sorted(ids), volume_data.function(centroid))

def create_cube_edges(volume_data: VolumeData, cube_vertices_ids: dict):
    create_weighted_simplex(volume_data, [cube_vertices_ids['A'], cube_vertices_ids['B']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['A'], cube_vertices_ids['C']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['A'], cube_vertices_ids['E']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['B'], cube_vertices_ids['C']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['B'], cube_vertices_ids['E']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['C'], cube_vertices_ids['E']])

    create_weighted_simplex(volume_data, [cube_vertices_ids['B'], cube_vertices_ids['H']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['C'], cube_vertices_ids['H']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['E'], cube_vertices_ids['H']])

    create_weighted_simplex(volume_data, [cube_vertices_ids['B'], cube_vertices_ids['F']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['E'], cube_vertices_ids['F']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['F'], cube_vertices_ids['H']])

    create_weighted_simplex(volume_data, [cube_vertices_ids['C'], cube_vertices_ids['G']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['E'], cube_vertices_ids['G']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['G'], cube_vertices_ids['H']])

    create_weighted_simplex(volume_data, [cube_vertices_ids['B'], cube_vertices_ids['D']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['C'], cube_vertices_ids['D']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['D'], cube_vertices_ids['H']])

def create_cube_faces(volume_data: VolumeData, cube_vertices_ids: dict):
    # MIDDLE TETRAHEDRON
    create_weighted_simplex(volume_data, [cube_vertices_ids['B'], cube_vertices_ids['C'], cube_vertices_ids['E']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['B'], cube_vertices_ids['E'], cube_vertices_ids['H']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['B'], cube_vertices_ids['C'], cube_vertices_ids['H']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['C'], cube_vertices_ids['E'], cube_vertices_ids['H']])

    # TETRAHEDRON IN A
    create_weighted_simplex(volume_data, [cube_vertices_ids['A'], cube_vertices_ids['B'], cube_vertices_ids['E']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['A'], cube_vertices_ids['C'], cube_vertices_ids['E']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['A'], cube_vertices_ids['B'], cube_vertices_ids['C']])

    # TETRAHEDRON IN D
    create_weighted_simplex(volume_data, [cube_vertices_ids['D'], cube_vertices_ids['B'], cube_vertices_ids['C']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['D'], cube_vertices_ids['C'], cube_vertices_ids['H']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['D'], cube_vertices_ids['B'], cube_vertices_ids['H']])

    # # TETRAHEDRON IN F
    create_weighted_simplex(volume_data, [cube_vertices_ids['F'], cube_vertices_ids['E'], cube_vertices_ids['H']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['F'], cube_vertices_ids['B'], cube_vertices_ids['E']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['F'], cube_vertices_ids['B'], cube_vertices_ids['H']])

    # # TETRAHEDRON IN G
    create_weighted_simplex(volume_data, [cube_vertices_ids['G'], cube_vertices_ids['E'], cube_vertices_ids['H']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['G'], cube_vertices_ids['C'], cube_vertices_ids['E']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['G'], cube_vertices_ids['C'], cube_vertices_ids['H']])

def create_cube_tetrahedrons(volume_data: VolumeData, cube_vertices_ids: dict):
    create_weighted_simplex(volume_data, [cube_vertices_ids['A'], cube_vertices_ids['B'], cube_vertices_ids['C'], cube_vertices_ids['E']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['B'], cube_vertices_ids['C'], cube_vertices_ids['E'], cube_vertices_ids['H']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['B'], cube_vertices_ids['E'], cube_vertices_ids['F'], cube_vertices_ids['H']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['C'], cube_vertices_ids['E'], cube_vertices_ids['G'], cube_vertices_ids['H']])
    create_weighted_simplex(volume_data, [cube_vertices_ids['B'], cube_vertices_ids['C'], cube_vertices_ids['D'], cube_vertices_ids['H']])

def build_cube_with_tetrahedrons(volume_data: VolumeData, starting_pos: Coordinates, is_reversed: bool):
    cube_vertices_ids = create_cube_vertices(volume_data=volume_data, starting_pos=starting_pos, is_reversed=is_reversed)
    create_cube_edges(volume_data=volume_data, cube_vertices_ids=cube_vertices_ids)
    create_cube_faces(volume_data=volume_data, cube_vertices_ids=cube_vertices_ids)
    create_cube_tetrahedrons(volume_data=volume_data, cube_vertices_ids=cube_vertices_ids)

# FIXME Think to succession of cubes. Their faces must match
def main(cube_size: int, volume_size: dict):
    volume_data = VolumeData(function=wave_function, cube_size=cube_size)

    starting_pos = Coordinates((0, 0, 0))
    for floor in range(volume_size['z']):
        for row in range(volume_size['y']):
            for column in range(volume_size['x']):
                new_pos = starting_pos + (volume_data.units['u'] * column) + (volume_data.units['v'] * row) + (volume_data.units['w'] * floor)
                is_reversed = ((floor + row + column) % 2) == 1
                build_cube_with_tetrahedrons(volume_data=volume_data, starting_pos=new_pos, is_reversed=is_reversed)

    volume_data.save_csv("function_to_csv/csv_files/3D/")

if __name__ == "__main__":
    main(1, {'x': 2, 'y': 2, 'z': 2})