def build_matrix_ids(size: dict):
    current_id = 0
    matrix = []
    for _ in range(size['z']):
        current_floor = []
        for _ in range(size['y']):
            current_row = []
            for _ in range(size['x']):
                current_row.append(current_id)
                current_id += 1
            current_floor.append(current_row)
        matrix.append(current_floor)

    print(current_id)
    return matrix

def main(size: dict):
    ids = build_matrix_ids(size)

if __name__ == "__main__":
    main(size = {'x': 100, 'y': 100, 'z': 100})