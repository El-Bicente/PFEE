import numpy as np
import pandas as pd

class Coordinates:
    def __init__(self, coord):
        self.x, self.y, self.z = coord

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def to_string(self):
        return f'(x: {self.x}, y: {self.y}, z:{self.z})'

class Simplex:
    def __init__(self, coords, ID, weight):
        self.order = len(coords) - 1
        self.coords = coords
        self.weight = weight
        self.ID = ID

    def to_string(self):
        strs = [elm.to_string() for elm in self.coords]
        return "[" + ", ".join(strs) + "]"

    def get_centroid(self):
        div_degree = (self.order + 1)
        centroid = Coordinates((0, 0, 0))
        for point_coords in self.coords:
            centroid.x += point_coords.x
            centroid.y += point_coords.y
            centroid.z += point_coords.z

        centroid.x /= div_degree
        centroid.y /= div_degree
        centroid.z /= div_degree

        return centroid

def create_csv(df, columns, filename):
    res = pd.DataFrame(df)
    res.columns = columns
    res.to_csv(filename, index=False)

class Graph:
    def __init__(self):
        self.simplexes_id = []
        self.simplexes = [[], [], []]
        self.adj = []
        self.dual_adj = []

    def convert_to_csv(self, paths):
        df_points = []
        df_lines = []
        df_triangle = []
        pts_ids = {}

        for i in range (len(self.simplexes[0])):
            smp = self.simplexes[0][i]
            df_points.append((i, smp.coords[0].x, smp.coords[0].y, smp.coords[0].z, smp.weight))
            pts_ids[smp.coords[0]] = i

        for i in range (len(self.simplexes[1])):
            smp = self.simplexes[1][i]
            df_lines.append((pts_ids[smp.coords[0]], pts_ids[smp.coords[1]], smp.weight))

        for i in range (len(self.simplexes[2])):
            smp = self.simplexes[2][i]
            df_triangle.append((pts_ids[smp.coords[0]], pts_ids[smp.coords[1]], pts_ids[smp.coords[2]], smp.weight))

        create_csv(df_points, ["Node Number", "X", "Y", "Z", "Weight"], paths["points"])
        create_csv(df_lines, ["P1", "P2", "Weight"], paths["lines"])
        create_csv(df_triangle, ["S1", "S2", "S3", "Weight"], paths["triangles"])

        return

    
    def add_simplex(self, coord, weight=0):
        simplex = Simplex(coord, len(self.simplexes_id), weight)
        self.simplexes_id.append(simplex)
        self.simplexes[simplex.order].append(simplex)

        self.adj.append([])
        self.dual_adj.append([])

        #ADD 0_faces:
        if (simplex.order == 0):
            for i in [1, 2]:
                ord_list = self.simplexes[i]
                for smp in ord_list:
                    if (smp.ID != simplex.ID) and simplex.coords[0] in smp.coords:
                        self.adj[simplex.ID].append(smp.ID)
                        self.adj[smp.ID].append(simplex.ID)

        #ADD 1_faces:
        if (simplex.order == 1):
            for i in [0, 2]:
                ord_list = self.simplexes[i]
                for smp in ord_list:
                    if (smp.ID != simplex.ID) and smp.order == 2 and (simplex.coords[0] in smp.coords and simplex.coords[1] in smp.coords):
                        self.adj[simplex.ID].append(smp.ID)
                        self.adj[smp.ID].append(simplex.ID)
                    if (smp.ID != simplex.ID) and smp.order == 0 and (simplex.coords[0] in smp.coords or simplex.coords[1] in smp.coords):
                        self.adj[simplex.ID].append(smp.ID)
                        self.adj[smp.ID].append(simplex.ID)

        #ADD 2_faces:
        if (simplex.order == 2):
            for i in [0, 1, 2]:
                ord_list = self.simplexes[i]
                for smp in ord_list:
                    if (smp.ID != simplex.ID) and smp.order == 0 and (smp.coords[0] in simplex.coords):
                        self.adj[simplex.ID].append(smp.ID)
                        self.adj[smp.ID].append(simplex.ID)
                    if (smp.ID != simplex.ID) and smp.order == 1 and (smp.coords[0] in simplex.coords and smp.coords[1] in simplex.coords):
                        self.adj[simplex.ID].append(smp.ID)
                        self.adj[smp.ID].append(simplex.ID)
                    if (smp.ID != simplex.ID) and smp.order == 2 and ((smp.coords[0] in simplex.coords and smp.coords[1] in simplex.coords)
                                      or   (smp.coords[1] in simplex.coords and smp.coords[2] in simplex.coords)
                                      or   (smp.coords[0] in simplex.coords and smp.coords[2] in simplex.coords)):
                        self.dual_adj[simplex.ID].append(smp.ID)
                        self.dual_adj[smp.ID].append(simplex.ID)

        return simplex.ID

    def get_neighboors(self, ID):
        return self.adj[ID] + self.dual_adj[ID]

    def to_string(self):
        strs = [elm.to_string() for elm in self.simplexes]
        return "\n".join(strs)


"""
g = Graph()
print(g.add_simplex([Coordinates((0,0,0))]))
print(g.add_simplex([Coordinates((0,1,0))]))
print(g.add_simplex([Coordinates((0,0,1))]))
print(g.add_simplex([Coordinates((1,1,1))]))

print(g.add_simplex([Coordinates((0,0,0)), Coordinates((0,0,1))]))
print(g.add_simplex([Coordinates((0,1,0)), Coordinates((1,1,1))]))

print(g.add_simplex([Coordinates((0,0,0)), Coordinates((0,0,1)), Coordinates((0,1,0))]))
print(g.add_simplex([Coordinates((0,0,0)), Coordinates((0,0,1)), Coordinates((1,1,1))]))

print(g.adj)
print(g.dual_adj)

g.convert_to_csv()
"""