import numpy as np

from reord.graph_structure import Coordinates
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
    

def build_matrix_ids(size: dict):
    current_id = 0
    matrix = []

    # one cube can't be composed of one vertex on each side 
    for _ in range(size['z']):
        current_floor = []
        for _ in range(size['y']):
            current_row = []
            for _ in range(size['x']):
                current_row.append(current_id)
                current_id += 1
            current_floor.append(current_row)
        matrix.append(current_floor)

    return np.array(matrix)

def get_last_egdes(ids: dict, pos: Coordinates, reversed: bool, side: Side):
    last_local_edges = []
    if side == Side.FRONT:
        last_local_edges += [
                (ids[pos.z, pos.y, pos.x], ids[pos.z + 1, pos.y, pos.x]),
                (ids[pos.z, pos.y, pos.x], ids[pos.z, pos.y + 1, pos.x]),
        ]
        if not reversed:
            return last_local_edges + [(ids[pos.z, pos.y, pos.x], ids[pos.z + 1, pos.y + 1, pos.x])]
        return last_local_edges + [(ids[pos.z, pos.y + 1, pos.x], ids[pos.z + 1, pos.y, pos.x])]

    elif side == Side.LEFT:
        last_local_edges += [
            (ids[pos.z, pos.y, pos.x], ids[pos.z, pos.y, pos.x + 1]),
            (ids[pos.z, pos.y, pos.x], ids[pos.z + 1, pos.y, pos.x]),
        ]
        if not reversed:
            return last_local_edges + [(ids[pos.z, pos.y, pos.x], ids[pos.z + 1, pos.y, pos.x + 1])]
        return last_local_edges + [(ids[pos.z, pos.y, pos.x + 1], ids[pos.z + 1, pos.y, pos.x])]

    elif side == Side.TOP:
        last_local_edges += [
            (ids[pos.z, pos.y, pos.x], ids[pos.z, pos.y, pos.x + 1]),
            (ids[pos.z, pos.y, pos.x], ids[pos.z, pos.y + 1, pos.x]),
        ]
        if not reversed:
            return last_local_edges + [(ids[pos.z, pos.y, pos.x], ids[pos.z, pos.y + 1, pos.x + 1])]
        return last_local_edges + [(ids[pos.z, pos.y, pos.x + 1], ids[pos.z, pos.y + 1, pos.x])]

    elif side == Side.FRONT_TOP:
        return [(ids[pos.z, pos.y, pos.x], ids[pos.z, pos.y + 1, pos.x])]
    elif side == Side.LEFT_TOP:
        return [(ids[pos.z, pos.y, pos.x], ids[pos.z, pos.y, pos.x + 1])]
    elif side == Side.FRONT_LEFT:
        return [(ids[pos.z, pos.y, pos.x], ids[pos.z + 1, pos.y, pos.x])]
        

def get_local_edges(ids: dict, pos: Coordinates, reversed: bool):
    local_edges = [
        (ids[pos.z, pos.y, pos.x], ids[pos.z, pos.y, pos.x + 1]),
        (ids[pos.z, pos.y, pos.x], ids[pos.z, pos.y + 1, pos.x]),
        (ids[pos.z, pos.y, pos.x], ids[pos.z + 1, pos.y, pos.x])
    ]

    if not reversed:
        local_edges += [
            (ids[pos.z, pos.y, pos.x + 1], ids[pos.z + 1, pos.y, pos.x]),
            (ids[pos.z, pos.y + 1, pos.x], ids[pos.z + 1, pos.y, pos.x]),
            (ids[pos.z, pos.y + 1, pos.x], ids[pos.z, pos.y, pos.x + 1])
        ]

    else:
        local_edges += [
            (ids[pos.z, pos.y, pos.x], ids[pos.z + 1, pos.y, pos.x + 1]),
            (ids[pos.z, pos.y, pos.x], ids[pos.z + 1, pos.y + 1, pos.x]),
            (ids[pos.z, pos.y, pos.x], ids[pos.z, pos.y + 1, pos.x + 1])
        ]

    return local_edges

def get_local_faces(ids: dict, pos: Coordinates, reversed: bool):
    if not reversed:
        local_faces = [
            # right face
            (ids[pos.z, pos.y, pos.x], ids[pos.z, pos.y, pos.x + 1], ids[pos.z + 1, pos.y, pos.x]),
            (ids[pos.z, pos.y, pos.x + 1], ids[pos.z + 1, pos.y, pos.x], ids[pos.z + 1, pos.y, pos.x + 1]),

            # back face
            (ids[pos.z, pos.y, pos.x], ids[pos.z, pos.y + 1, pos.x], ids[pos.z + 1, pos.y, pos.x]),
            (ids[pos.z, pos.y + 1, pos.x], ids[pos.z + 1, pos.y, pos.x], ids[pos.z + 1, pos.y + 1, pos.x]),

            # botton face
            (ids[pos.z, pos.y, pos.x], ids[pos.z, pos.y, pos.x + 1], ids[pos.z, pos.y + 1, pos.x]),
            (ids[pos.z, pos.y, pos.x + 1], ids[pos.z, pos.y + 1, pos.x], ids[pos.z, pos.y + 1, pos.x + 1])
        ]
    else:
        local_faces = [
            # right face
            (ids[pos.z, pos.y, pos.x], ids[pos.z + 1, pos.y, pos.x], ids[pos.z + 1, pos.y, pos.x + 1]),
            (ids[pos.z, pos.y, pos.x], ids[pos.z, pos.y, pos.x + 1], ids[pos.z + 1, pos.y, pos.x + 1]),

            # back face
            (ids[pos.z, pos.y, pos.x], ids[pos.z + 1, pos.y, pos.x], ids[pos.z, pos.y + 1, pos.x]),
            (ids[pos.z, pos.y + 1, pos.x], ids[pos.z, pos.y + 1, pos.x], ids[pos.z + 1, pos.y + 1, pos.x]),

            # botton face
            (ids[pos.z, pos.y, pos.x], ids[pos.z, pos.y, pos.x + 1], ids[pos.z, pos.y + 1, pos.x + 1]),
            (ids[pos.z, pos.y, pos.x], ids[pos.z, pos.y + 1, pos.x], ids[pos.z, pos.y + 1, pos.x + 1])
        ]

    return local_faces

def get_local_tetras(ids: dict, pos: Coordinates, reversed: bool):
    if not reversed:
        local_tetras = [
            (ids[pos.z, pos.y, pos.x], ids[pos.z, pos.y, pos.x + 1], ids[pos.z, pos.y + 1, pos.x], ids[pos.z + 1, pos.y, pos.x]),
            (ids[pos.z, pos.y, pos.x + 1], ids[pos.z, pos.y + 1, pos.x], ids[pos.z, pos.y + 1, pos.x + 1], ids[pos.z + 1, pos.y + 1, pos.x + 1]),
            (ids[pos.z, pos.y + 1, pos.x], ids[pos.z + 1, pos.y, pos.x], ids[pos.z + 1, pos.y + 1, pos.x], ids[pos.z + 1, pos.y + 1, pos.x + 1]),
            (ids[pos.z, pos.y, pos.x + 1], ids[pos.z + 1, pos.y, pos.x], ids[pos.z + 1, pos.y, pos.x + 1], ids[pos.z + 1, pos.y + 1, pos.x + 1]),
            (ids[pos.z, pos.y, pos.x + 1], ids[pos.z, pos.y + 1, pos.x], ids[pos.z + 1, pos.y, pos.x], ids[pos.z + 1, pos.y + 1, pos.x + 1]),
        ]
    else:
        local_tetras = [
            (ids[pos.z, pos.y, pos.x], ids[pos.z + 1, pos.y, pos.x], ids[pos.z + 1, pos.y, pos.x + 1], ids[pos.z + 1, pos.y + 1, pos.x]),
            (ids[pos.z, pos.y + 1, pos.x + 1], ids[pos.z + 1, pos.y, pos.x + 1], ids[pos.z + 1, pos.y + 1, pos.x], ids[pos.z + 1, pos.y + 1, pos.x + 1]),
            (ids[pos.z, pos.y, pos.x], ids[pos.z, pos.y, pos.x + 1], ids[pos.z, pos.y + 1, pos.x + 1], ids[pos.z + 1, pos.y, pos.x + 1]),
            (ids[pos.z, pos.y, pos.x], ids[pos.z, pos.y + 1, pos.x], ids[pos.z, pos.y + 1, pos.x + 1], ids[pos.z + 1, pos.y + 1, pos.x]),
            (ids[pos.z, pos.y, pos.x], ids[pos.z, pos.y + 1, pos.x + 1], ids[pos.z + 1, pos.y, pos.x + 1], ids[pos.z + 1, pos.y + 1, pos.x]),
        ]

    return local_tetras


def build_volume(ids: np.array):
    reversed = False
    edges = []
    faces = []
    tetras = []
    for z in range(ids.shape[0]):
        for y in range(ids.shape[1]):
            reversed = not reversed
            for x in range(ids.shape[2]):
                current_pos = Coordinates((x, y, z))

                if (x == (ids.shape[2] - 1)):
                    edges += get_last_egdes(ids, current_pos, reversed, Side.FRONT)
                    faces += get_last_faces(ids, current_pos, reversed, Side.FRONT)
                    continue
                if (y == (ids.shape[1] - 1)):
                    edges += get_last_egdes(ids, current_pos, reversed, Side.LEFT)
                    faces += get_last_faces(ids, current_pos, reversed, Side.LEFT)
                    continue
                if (z == (ids.shape[0] - 1)):
                    edges += get_last_egdes(ids, current_pos, reversed, Side.TOP)
                    faces += get_last_faces(ids, current_pos, reversed, Side.TOP)
                    continue
                if (x == (ids.shape[2] - 1)) and (z == (ids.shape[0] - 1)):
                    edges += get_last_egdes(ids, current_pos, reversed, Side.FRONT_TOP)
                    faces += get_last_faces(ids, current_pos, reversed, Side.FRONT_TOP)
                    continue
                if (y == (ids.shape[1] - 1)) and (z == (ids.shape[0] - 1)):
                    edges += get_last_egdes(ids, current_pos, reversed, Side.LEFT_TOP)
                    faces += get_last_faces(ids, current_pos, reversed, Side.LEFT_TOP)
                    continue
                if (x == (ids.shape[2] - 1)) and (y == (ids.shape[1] - 1)):
                    edges += get_last_egdes(ids, current_pos, reversed, Side.FRONT_LEFT)
                    faces += get_last_faces(ids, current_pos, reversed, Side.FRONT_LEFT)
                    continue

                edges += get_local_edges(ids, current_pos, reversed)
                faces += get_local_faces(ids, current_pos, reversed)
                tetras += get_local_tetras(ids, current_pos, reversed)


    print(f"number of edges: {len(edges)}")
    print(f"number of faces: {len(faces)}")
    print(f"number of tetras: {len(tetras)}")

def main(size: dict):
    if (size := check_input(size)):
        ids = build_matrix_ids(size)
        build_volume(ids)

if __name__ == "__main__":
    main(size = {'x': 10, 'y': 10, 'z': 10})