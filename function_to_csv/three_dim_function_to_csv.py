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
        self.last_index = -1
        self.csv: DataCSV = DataCSV()
        self.function = function
        self.cube_size = 1 if cube_size < 0 else cube_size

    def add_vertex(self, vertex: Coordinates):
        new_vertex = pd.DataFrame.from_records([{'x': vertex.x, 'y': vertex.y, 'z': vertex.z}])
        self.vertices = pd.concat([self.vertices, new_vertex], ignore_index=True)
        self.last_index += 1
        self.csv.vertices += f"{self.last_index}, {vertex.x}, {vertex.y}, {vertex.z}, {self.function(vertex)}\n"
        
        return self.last_index

    def get_vertex_id(vertices: pd.DataFrame, coordinates: Coordinates):
        row = vertices[(vertices.x == coordinates.x) & (vertices.y == coordinates.y) & (vertices.z == coordinates.z)]
        # row = [] si rien n'est trouvé
        if row:
            # row.index renvoie Int64Index([5], dtype='int64')
            return row.index[0]
        return None

    def save_csv(self, path: str):
        for body_filename in ["vertices", "edges", "faces", "tetras"]:
            with open(path + body_filename + ".csv", "w") as csv_file:
                csv_file.write(getattr(self.csv, body_filename))


def create_cube_vertices(volume_data: VolumeData, starting_pos: Coordinates):
    """
    volume_data: VolumeData => main structure that contains important information
    starting_pos: Coordinates => starting position of the cube

    Return: dict of vertices ids
    """
    u = Coordinates((volume_data.cube_size, 0, 0))
    v = Coordinates((0, volume_data.cube_size, 0))
    w = Coordinates((0, 0, volume_data.cube_size))

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

    cube_vertivces_ids = {}
    for key, current_vertex in cube_vertices.items():
        cube_vertivces_ids[key] = volume_data.add_vertex(current_vertex)

    return cube_vertivces_ids

# FIXME Think to init the correct weights
def create_cube_edges(volume_data: VolumeData, cube_vertices_ids: dict):
    edges = f"{cube_vertices_ids['A']}, {cube_vertices_ids['B']}, 0\n"
    edges += f"{cube_vertices_ids['A']}, {cube_vertices_ids['C']}, 0\n"
    edges += f"{cube_vertices_ids['A']}, {cube_vertices_ids['E']}, 0\n"
    edges += f"{cube_vertices_ids['B']}, {cube_vertices_ids['C']}, 0\n"
    edges += f"{cube_vertices_ids['B']}, {cube_vertices_ids['E']}, 0\n"
    edges += f"{cube_vertices_ids['C']}, {cube_vertices_ids['E']}, 0\n"

    edges += f"{cube_vertices_ids['B']}, {cube_vertices_ids['H']}, 0\n"
    edges += f"{cube_vertices_ids['C']}, {cube_vertices_ids['H']}, 0\n"
    edges += f"{cube_vertices_ids['E']}, {cube_vertices_ids['H']}, 0\n"

    edges += f"{cube_vertices_ids['B']}, {cube_vertices_ids['F']}, 0\n"
    edges += f"{cube_vertices_ids['E']}, {cube_vertices_ids['F']}, 0\n"
    edges += f"{cube_vertices_ids['F']}, {cube_vertices_ids['H']}, 0\n"

    edges += f"{cube_vertices_ids['C']}, {cube_vertices_ids['G']}, 0\n"
    edges += f"{cube_vertices_ids['E']}, {cube_vertices_ids['G']}, 0\n"
    edges += f"{cube_vertices_ids['G']}, {cube_vertices_ids['H']}, 0\n"

    edges += f"{cube_vertices_ids['B']}, {cube_vertices_ids['D']}, 0\n"
    edges += f"{cube_vertices_ids['C']}, {cube_vertices_ids['D']}, 0\n"
    edges += f"{cube_vertices_ids['D']}, {cube_vertices_ids['H']}, 0\n"

    volume_data.csv.edges += edges

# FIXME Think to init the correct weight
def create_cube_faces(volume_data: VolumeData, cube_vertices_ids: dict):
    # MIDDLE TETRAHEDRON
    faces = f"{cube_vertices_ids['B']}, {cube_vertices_ids['C']}, {cube_vertices_ids['E']}, 0\n"
    faces += f"{cube_vertices_ids['B']}, {cube_vertices_ids['E']}, {cube_vertices_ids['H']}, 0\n"
    faces += f"{cube_vertices_ids['B']}, {cube_vertices_ids['C']}, {cube_vertices_ids['H']}, 0\n"
    faces += f"{cube_vertices_ids['C']}, {cube_vertices_ids['E']}, {cube_vertices_ids['H']}, 0\n"

    # TETRAHEDRON IN A
    faces += f"{cube_vertices_ids['A']}, {cube_vertices_ids['B']}, {cube_vertices_ids['E']}, 0\n"
    faces += f"{cube_vertices_ids['A']}, {cube_vertices_ids['C']}, {cube_vertices_ids['E']}, 0\n"
    faces += f"{cube_vertices_ids['A']}, {cube_vertices_ids['B']}, {cube_vertices_ids['C']}, 0\n"

    # TETRAHEDRON IN D
    faces += f"{cube_vertices_ids['D']}, {cube_vertices_ids['B']}, {cube_vertices_ids['C']}, 0\n"
    faces += f"{cube_vertices_ids['D']}, {cube_vertices_ids['C']}, {cube_vertices_ids['H']}, 0\n"
    faces += f"{cube_vertices_ids['D']}, {cube_vertices_ids['B']}, {cube_vertices_ids['H']}, 0\n"

    # TETRAHEDRON IN F
    faces += f"{cube_vertices_ids['F']}, {cube_vertices_ids['E']}, {cube_vertices_ids['H']}, 0\n"
    faces += f"{cube_vertices_ids['F']}, {cube_vertices_ids['B']}, {cube_vertices_ids['E']}, 0\n"
    faces += f"{cube_vertices_ids['F']}, {cube_vertices_ids['B']}, {cube_vertices_ids['H']}, 0\n"

    # TETRAHEDRON IN G
    faces += f"{cube_vertices_ids['G']}, {cube_vertices_ids['E']}, {cube_vertices_ids['H']}, 0\n"
    faces += f"{cube_vertices_ids['G']}, {cube_vertices_ids['C']}, {cube_vertices_ids['E']}, 0\n"
    faces += f"{cube_vertices_ids['G']}, {cube_vertices_ids['C']}, {cube_vertices_ids['H']}, 0\n"

    volume_data.csv.faces += faces

# FIXME Think to init the correct weight
def create_cube_tetrahedrons(volume_data: VolumeData, cube_vertivces_ids: dict):
    tetras = f"{cube_vertivces_ids['A']}, {cube_vertivces_ids['B']}, {cube_vertivces_ids['C']}, {cube_vertivces_ids['E']}, 0\n"
    tetras += f"{cube_vertivces_ids['B']}, {cube_vertivces_ids['C']}, {cube_vertivces_ids['E']}, {cube_vertivces_ids['H']}, 0\n"
    tetras += f"{cube_vertivces_ids['B']}, {cube_vertivces_ids['E']}, {cube_vertivces_ids['F']}, {cube_vertivces_ids['H']}, 0\n"
    tetras += f"{cube_vertivces_ids['C']}, {cube_vertivces_ids['E']}, {cube_vertivces_ids['G']}, {cube_vertivces_ids['H']}, 0\n"
    tetras += f"{cube_vertivces_ids['B']}, {cube_vertivces_ids['C']}, {cube_vertivces_ids['D']}, {cube_vertivces_ids['H']}, 0\n"

    volume_data.csv.tetras += tetras


# FIXME Think to common face => we musn't create edge, vertex and face once again
def build_cube_with_tetrahedrons(volume_data: VolumeData, starting_pos: Coordinates):
    cube_vertices_ids = create_cube_vertices(volume_data=volume_data, starting_pos=starting_pos)
    create_cube_edges(volume_data=volume_data, cube_vertices_ids=cube_vertices_ids)
    create_cube_faces(volume_data=volume_data, cube_vertices_ids=cube_vertices_ids)
    create_cube_tetrahedrons(volume_data=volume_data, cube_vertivces_ids=cube_vertices_ids)

    
# FIXME Think to succession of cubes. Their faces must match
def main():
    volume_data = VolumeData(function=wave_function)
    build_cube_with_tetrahedrons(volume_data=volume_data, starting_pos=Coordinates((0, 0, 0)))
    volume_data.save_csv("function_to_csv/csv_files/3D/")
    
if __name__ == "__main__":
    main()