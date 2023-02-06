import numpy as np

from graph_structure import Coordinates
from enum import Enum

class Side(Enum):
    FRONT = 1
    LEFT = 2
    TOP = 3
    FRONT_TOP = 4
    LEFT_TOP = 5
    FRONT_LEFT = 6

def check_input(size: dict) -> bool:
    if size['x'] > 0 and size['y'] > 0 and size['z'] > 0:
        return {'x': size['x'] + 1, 'y': size['y'] + 1, 'z': size['z'] + 1}

    print('There is an error in input parameter. One of them is under zero. You can not get less than one cube.')
    raise
    

def build_matrix_ids(size: dict, step: int, function):
    current_id = 0
    matrix = []
    vertices = []

    # one cube can't be composed of one vertex on each side 
    for z in range(size['z']):
        current_floor = []
        for y in range(size['y']):
            current_row = []
            for x in range(size['x']):
                vertices += [(current_id, x * step, y * step, z * step, function(Coordinates((x, y, z))))]
                current_row.append(current_id)
                current_id += 1
            current_floor.append(current_row)
        matrix.append(current_floor)

    return np.array(matrix), vertices

def get_centroid(coords):
    mean_degree = (len(coords) + 1)
    centroid = Coordinates((0, 0, 0))
    for vertex_coords in coords:
        centroid.x += vertex_coords[0]
        centroid.y += vertex_coords[1]
        centroid.z += vertex_coords[2]

    centroid.x /= mean_degree
    centroid.y /= mean_degree
    centroid.z /= mean_degree

    return centroid

def get_simplex_with_weight(ids, coords, function):
    centroid = get_centroid(coords)

    return tuple(ids[z, y, x] for z, y, x in coords) + (function(centroid),)

def get_last_egdes(ids: np.array, pos: Coordinates, reversed: bool, side: Side, function):
    """
        description:
            complete the missing edges on the last line, column, floor or the volume
        params:
            ids: 3D numpy array of vertex's id. Coordinates of a vertex in the matrix 
            represents the coordinates of a vertex in the final space
            pos: current position of the cube it is building
            reversed : does it need to create edges for a reverse cube or not ?
            side: enum about position of the vertex
                - FRONT : last x pos
                - LEFT : last y pos
                - TOP : last z pos
                ...
            function: function to get the weight of each simplex
        return:
            missing edges
    """
    last_local_edges = []
    if side == Side.FRONT:
        last_local_edges += [
                get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z + 1, pos.y, pos.x)], function), # A, E
                get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y + 1, pos.x)], function), # A, C
        ]
        if not reversed:
            return last_local_edges + [get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z + 1, pos.y + 1, pos.x)], function)] # A, G
        return last_local_edges + [get_simplex_with_weight(ids, [(pos.z, pos.y + 1, pos.x), (pos.z + 1, pos.y, pos.x)], function)] # C, E

    elif side == Side.LEFT:
        last_local_edges += [
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y, pos.x + 1)], function), # A, B
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z + 1, pos.y, pos.x)], function), # A, E
        ]
        if not reversed:
            return last_local_edges + [get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z + 1, pos.y, pos.x + 1)], function)] # A, F
        return last_local_edges + [get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x + 1), (pos.z + 1, pos.y, pos.x)], function)] # B, E

    elif side == Side.TOP:
        last_local_edges += [
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y, pos.x + 1)], function), # A, B
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y + 1, pos.x)], function), # A, C
        ]
        if not reversed:
            return last_local_edges + [get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y + 1, pos.x + 1)], function)] # A, D
        return last_local_edges + [get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x + 1), (pos.z, pos.y + 1, pos.x)], function)] # B, C

    elif side == Side.FRONT_TOP:
        return [get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y + 1, pos.x)], function)] # A, C
    elif side == Side.LEFT_TOP:
        return [get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y, pos.x + 1)], function)] # A, B
    elif side == Side.FRONT_LEFT:
        return [get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z + 1, pos.y, pos.x)], function)] # A, E

def get_last_faces(ids: np.array, pos: Coordinates, reversed: bool, side: Side, function):
    """
        description:
            complete the missing faces on the last line, column, floor or the volume
        params:
            ids: 3D numpy array of vertex's id. Coordinates of a vertex in the matrix 
            represents the coordinates of a vertex in the final space
            pos: current position of the cube it is building
            reversed : does it need to create edges for a reverse cube or not ?
            side: enum about position of the vertex
                - FRONT : last x pos
                - LEFT : last y pos
                - TOP : last z pos
                ...
            function: function to get the weight of each simplex
        return:
            missing faces
    """
    last_local_faces = []
    if side == Side.FRONT:
        if not reversed:
            last_local_faces += [
                get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z + 1, pos.y, pos.x), (pos.z + 1, pos.y + 1, pos.x)], function), # A, E, G
                get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y + 1, pos.x), (pos.z + 1, pos.y + 1, pos.x)], function), # A, C, G
            ]
        else:
            last_local_faces += [
                get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y + 1, pos.x), (pos.z + 1, pos.y, pos.x)], function), # A, C, E
                get_simplex_with_weight(ids, [(pos.z, pos.y + 1, pos.x), (pos.z + 1, pos.y + 1, pos.x), (pos.z + 1, pos.y, pos.x)], function) # C, G, E
            ]

    elif side == Side.LEFT:
        if not reversed:
            last_local_faces += [
                get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y, pos.x + 1), (pos.z + 1, pos.y, pos.x + 1)], function), # A, B, F
                get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z + 1, pos.y, pos.x), (pos.z + 1, pos.y, pos.x + 1)], function), # A, E, F
            ]
        else:
            last_local_faces += [
                get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x + 1), (pos.z + 1, pos.y, pos.x + 1), (pos.z + 1, pos.y, pos.x)], function), # B, F, E
                get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x + 1), (pos.z, pos.y, pos.x), (pos.z + 1, pos.y, pos.x)], function), # B, A, E
            ]

    elif side == Side.TOP:
        if not reversed:
            last_local_faces += [
                get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y, pos.x + 1), (pos.z, pos.y + 1, pos.x + 1)], function), # A, B, D
                get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y + 1, pos.x), (pos.z, pos.y + 1, pos.x + 1)], function), # A, C, D
            ]
        else:
            last_local_faces += [
                get_simplex_with_weight(ids, [(pos.z, pos.y + 1, pos.x), (pos.z, pos.y, pos.x), (pos.z, pos.y, pos.x + 1)], function), # C, A, B
                get_simplex_with_weight(ids, [(pos.z, pos.y + 1, pos.x), (pos.z, pos.y + 1, pos.x + 1), (pos.z, pos.y, pos.x + 1)], function), # C, D, B
            ]
    
    return last_local_faces

def get_local_edges(ids: np.array, pos: Coordinates, reversed: bool, function):
    """
        description:
            get the interlocking edges for the current cube
        params:
            ids: 3D numpy array of vertex's id. Coordinates of a vertex in the matrix 
            represents the coordinates of a vertex in the final space
            pos: current position of the cube it is building
            reversed : does it need to create edges for a reverse cube or not ?
            function: function to get the weight of each simplex
        return:
            interlocking edges
    """
    local_edges = [
        get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y, pos.x + 1)], function), # A, B
        get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y + 1, pos.x)], function), # A, C
        get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z + 1, pos.y, pos.x)], function)  # A, E
    ]

    if not reversed:
        local_edges += [
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x + 1), (pos.z + 1, pos.y, pos.x)], function), # B, E
            get_simplex_with_weight(ids, [(pos.z, pos.y + 1, pos.x), (pos.z + 1, pos.y, pos.x)], function), # C, E
            get_simplex_with_weight(ids, [(pos.z, pos.y + 1, pos.x), (pos.z, pos.y, pos.x + 1)], function)  # C, B
        ]

    else:
        local_edges += [
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z + 1, pos.y, pos.x + 1)], function), # A, F
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z + 1, pos.y + 1, pos.x)], function), # A, G
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y + 1, pos.x + 1)], function)  # A, D
        ]

    return local_edges

def get_local_faces(ids: np.array, pos: Coordinates, reversed: bool, function):
    """
        description:
            get the interlocking faces for the current cube
        params:
            ids: 3D numpy array of vertex's id. Coordinates of a vertex in the matrix 
            represents the coordinates of a vertex in the final space
            pos: current position of the cube it is building
            reversed : does it need to create edges for a reverse cube or not ?
            function: function to get the weight of each simplex
        return:
            interlocking faces
    """
    if not reversed:
        local_faces = [
            # right face
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y, pos.x + 1), (pos.z + 1, pos.y, pos.x)], function), # A, B, E
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x + 1), (pos.z + 1, pos.y, pos.x), (pos.z + 1, pos.y, pos.x + 1)], function), # B, E, F

            # back face
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y + 1, pos.x), (pos.z + 1, pos.y, pos.x)], function), # A, C, E
            get_simplex_with_weight(ids, [(pos.z, pos.y + 1, pos.x), (pos.z + 1, pos.y, pos.x), (pos.z + 1, pos.y + 1, pos.x)], function), # C, E, G

            # botton face
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y, pos.x + 1), (pos.z, pos.y + 1, pos.x)], function), # A, B, C
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x + 1), (pos.z, pos.y + 1, pos.x), (pos.z, pos.y + 1, pos.x + 1)], function) # B, C, D
        ]
    else:
        local_faces = [
            # right face
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z + 1, pos.y, pos.x), (pos.z + 1, pos.y, pos.x + 1)], function), # A, E, F
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y, pos.x + 1), (pos.z + 1, pos.y, pos.x + 1)], function), # A, B, F

            # back face
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y + 1, pos.x), (pos.z + 1, pos.y + 1, pos.x)], function), # A, C, G
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z + 1, pos.y, pos.x), (pos.z + 1, pos.y + 1, pos.x)], function), # A, E, G

            # botton face
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y, pos.x + 1), (pos.z, pos.y + 1, pos.x + 1)], function), # A, B, D
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y + 1, pos.x), (pos.z, pos.y + 1, pos.x + 1)], function)  # A, C, D
        ]

    return local_faces

def get_local_tetras(ids: np.array, pos: Coordinates, reversed: bool, function):
    """
        description:
            get the interlocking tetrahedras for the current cube
        params:
            ids: 3D numpy array of vertex's id. Coordinates of a vertex in the matrix 
            represents the coordinates of a vertex in the final space
            pos: current position of the cube it is building
            reversed : does it need to create edges for a reverse cube or not ?
            function: function to get the weight of each simplex
        return:
            interlocking tetrahedras
    """
    if not reversed:
        local_tetras = [
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y, pos.x + 1), (pos.z, pos.y + 1, pos.x), (pos.z + 1, pos.y, pos.x)], function), # A, B, C, E
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x + 1), (pos.z, pos.y + 1, pos.x), (pos.z, pos.y + 1, pos.x + 1), (pos.z + 1, pos.y + 1, pos.x + 1)], function), # B, C, D, H
            get_simplex_with_weight(ids, [(pos.z, pos.y + 1, pos.x), (pos.z + 1, pos.y, pos.x), (pos.z + 1, pos.y + 1, pos.x), (pos.z + 1, pos.y + 1, pos.x + 1)], function), # C, E, G, H
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x + 1), (pos.z + 1, pos.y, pos.x), (pos.z + 1, pos.y, pos.x + 1), (pos.z + 1, pos.y + 1, pos.x + 1)], function), # B, E, F, H
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x + 1), (pos.z, pos.y + 1, pos.x), (pos.z + 1, pos.y, pos.x), (pos.z + 1, pos.y + 1, pos.x + 1)], function), # B, C, E, H
        ]
    else:
        local_tetras = [
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z + 1, pos.y, pos.x), (pos.z + 1, pos.y, pos.x + 1), (pos.z + 1, pos.y + 1, pos.x)], function), # A, E, F, G
            get_simplex_with_weight(ids, [(pos.z, pos.y + 1, pos.x + 1), (pos.z + 1, pos.y, pos.x + 1), (pos.z + 1, pos.y + 1, pos.x), (pos.z + 1, pos.y + 1, pos.x + 1)], function), # D, F, G, H
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y, pos.x + 1), (pos.z, pos.y + 1, pos.x + 1), (pos.z + 1, pos.y, pos.x + 1)], function), # A, B, D, F
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y + 1, pos.x), (pos.z, pos.y + 1, pos.x + 1), (pos.z + 1, pos.y + 1, pos.x)], function), # A, C, D, G
            get_simplex_with_weight(ids, [(pos.z, pos.y, pos.x), (pos.z, pos.y + 1, pos.x + 1), (pos.z + 1, pos.y, pos.x + 1), (pos.z + 1, pos.y + 1, pos.x)], function), # A, D, F, G
        ]

    return local_tetras

def save_volume_as_csv(paths: dict, vertices: list, edges: list, faces: list, tetras: list):
    """
        description:
            save the volume as csv
        params:
            vertices : list of vertices (id, x, y, z, weight)
            edges : list of edges (id1, id2, weight)
            faces : list of faces (id1, id2,, id3, weight)
            tetras : list of tetrahedras (id1, id2,, id3, id4, weight)
        return:
           nothing
    """
    np.savetxt(paths["points"], np.asarray(vertices), delimiter=",", header="Node Number,X,Y,Z,Weight")
    np.savetxt(paths["lines"], np.asarray(edges), delimiter=",", header="P1,P2,Weight")
    np.savetxt(paths["triangles"], np.asarray(faces), delimiter=",", header="S1,S2,S3,Weight")
    np.savetxt(paths["tetras"], np.asarray(tetras), delimiter=",", header="S1,S2,S3,S4,Weight")

def is_reversed(pos: tuple, cell_status_board: np.array):
    """
        description:
            get the status of a cube (if it is a reversed one or not).
        params:
            pos: current position of the cube it is building
            cell_status_board: numpy array containing status for each cube
        return:
            cube status
    """
    x, y, z = pos

    # If it is the first cell, because it will be the only one
    # already initialized
    if cell_status_board[z, y, x] is not None:
        return cell_status_board[z, y, x]
    
    # Check only cells behind or on the right or under
    # These are the only ones that could be initialized
    # related to our path
    if x > 0:
        return not cell_status_board[z, y, x - 1]
    elif y > 0:
        return not cell_status_board[z, y - 1, x]
    elif z > 0:
        return not cell_status_board[z - 1, y, x]
    
    raise Exception(f"No neighbors has been found at pos {pos}")

def build_volume(ids: np.array, function):
    """
        description:
            Build the volume with an hardcoded way. Build each cube thanks to
            the next cube in order to avoid checks at intersection to avoid to
            create duplicates (edges and faces). Complete the missing faces, 
            edges for each last cube of an axis.
        params:
            ids: Numpy array of ids for each vertices
            function: function  to apply to get the weights
        return:
            edges, faces, tetrahedras to save
    """
    reversed = False
    edges = []
    faces = []
    tetras = []

    cell_status_board = np.full(ids.shape, None)
    cell_status_board[0, 0, 0] = False

    for z in range(ids.shape[0]):
        for y in range(ids.shape[1]):
            for x in range(ids.shape[2]):
                current_pos = Coordinates((x, y, z))
                reversed = is_reversed((x, y, z), cell_status_board)
                cell_status_board[z, y, x] = reversed

                if (x == (ids.shape[2] - 1)) and (y == (ids.shape[1] - 1) and (z == (ids.shape[0] - 1))):
                    continue
                if (x == (ids.shape[2] - 1)) and (z == (ids.shape[0] - 1)):
                    edges += get_last_egdes(ids, current_pos, reversed, Side.FRONT_TOP, function)
                    faces += get_last_faces(ids, current_pos, reversed, Side.FRONT_TOP, function)
                    continue
                if (y == (ids.shape[1] - 1)) and (z == (ids.shape[0] - 1)):
                    edges += get_last_egdes(ids, current_pos, reversed, Side.LEFT_TOP, function)
                    faces += get_last_faces(ids, current_pos, reversed, Side.LEFT_TOP, function)
                    continue
                if (x == (ids.shape[2] - 1)) and (y == (ids.shape[1] - 1)):
                    edges += get_last_egdes(ids, current_pos, reversed, Side.FRONT_LEFT, function)
                    faces += get_last_faces(ids, current_pos, reversed, Side.FRONT_LEFT, function)
                    continue
                if (x == (ids.shape[2] - 1)):
                    edges += get_last_egdes(ids, current_pos, reversed, Side.FRONT, function)
                    faces += get_last_faces(ids, current_pos, reversed, Side.FRONT, function)
                    continue
                if (y == (ids.shape[1] - 1)):
                    edges += get_last_egdes(ids, current_pos, reversed, Side.LEFT, function)
                    faces += get_last_faces(ids, current_pos, reversed, Side.LEFT, function)
                    continue
                if (z == (ids.shape[0] - 1)):
                    edges += get_last_egdes(ids, current_pos, reversed, Side.TOP, function)
                    faces += get_last_faces(ids, current_pos, reversed, Side.TOP, function)
                    continue

                edges += get_local_edges(ids, current_pos, reversed, function)
                faces += get_local_faces(ids, current_pos, reversed, function)
                tetras += get_local_tetras(ids, current_pos, reversed, function)


    print(f"number of edges: {len(edges)}")
    print(f"number of faces: {len(faces)}")
    print(f"number of tetras: {len(tetras)}")

    return edges, faces, tetras
    

def main(step: int, size: dict, paths: dict, function):
    if (size := check_input(size)):
        ids, vertices = build_matrix_ids(size, step, function)
        edges, faces, tetras = build_volume(ids, function)
        save_volume_as_csv(paths, vertices, edges, faces, tetras)

if __name__ == "__main__":
    main(size = {'x': 10, 'y': 10, 'z': 10})