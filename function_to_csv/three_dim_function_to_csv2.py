import numpy as np
import time

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

def get_local_edges(ids: dict, pos: tuple[int, int, int], reversed: bool):
    local_edges = [
        (ids[pos[2], pos[1], pos[0]], ids[pos[2], pos[1], pos[0] + 1]),
        (ids[pos[2], pos[1], pos[0]], ids[pos[2], pos[1] + 1, pos[0]]),
        (ids[pos[2], pos[1], pos[0]], ids[pos[2] + 1, pos[1], pos[0]])
    ]

    if not reversed:
        local_edges.append((ids[pos[2], pos[1], pos[0] + 1], ids[pos[2] + 1, pos[1], pos[0]]))
        local_edges.append((ids[pos[2], pos[1] + 1, pos[0]], ids[pos[2] + 1, pos[1], pos[0]]))
        local_edges.append((ids[pos[2], pos[1] + 1, pos[0]], ids[pos[2], pos[1], pos[0] + 1]))

    else:
        local_edges.append((ids[pos[2], pos[1], pos[0]], ids[pos[2] + 1, pos[1], pos[0] + 1]))
        local_edges.append((ids[pos[2], pos[1], pos[0]], ids[pos[2] + 1, pos[1] + 1, pos[0]]))
        local_edges.append((ids[pos[2], pos[1], pos[0]], ids[pos[2], pos[1] + 1, pos[0] + 1]))

    return local_edges

def build_volume(ids: np.array):
    reversed = False
    edges = []
    for z in range(ids.shape[0] - 1):
        for y in range(ids.shape[1] - 1):
            reversed = not reversed
            for x in range(ids.shape[2] - 1):
                edges += get_local_edges(ids, (x, y, z), reversed)

    print(f"number of edges: {len(edges)}")

                


def main(size: dict):
    if (size := check_input(size)):       
        ids = build_matrix_ids(size)

        start_time = time.time()
        build_volume(ids)
        print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main(size = {'x': 10, 'y': 10, 'z': 10})