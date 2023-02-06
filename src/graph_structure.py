import math
import numpy as np
import pandas as pd


class Coordinates:
    def __init__(self, coord):
        self.x, self.y, self.z = coord

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def calculate_equality(self, nb1, nb2):
        return abs(nb1 - nb2) <= 0.000000001

    def __eq__(self, other):
        return  self.calculate_equality(self.x, other.x)     \
                and self.calculate_equality(self.y, other.y) \
                and self.calculate_equality(self.z, other.z) \

    def copy(self):
        return Coordinates((self.x, self.y, self.z))

    def to_string(self):
        return f'(x: {self.x}, y: {self.y}, z:{self.z})'

    def get_distance(self, other):
        return math.sqrt((self.x - other.x)**2 +
                         (self.y - other.y)**2 +
                         (self.z - other.z)**2)

    def get_middle_coord(self, other):
        xm = self.x + (other.x - self.x) / 2
        ym = self.y + (other.y - self.y) / 2
        zm = self.z + (other.z - self.z) / 2
        return Coordinates((self.x, self.y, self.z))

    def get_vector(self, other):
        return (other.x - self.x, other.y - self.y, other.z - self.z)

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
    res = pd.DataFrame(df, columns = columns)
    res.to_csv(filename, index=False)


class Graph:
    def __init__(self, order):
        #List where each position represents the ID and each value represents
        #the simplex
        self.simplexes_id = []
        self.order = order
        self.simplexes = [[] for i in range (self.order + 1)]
        #Adjency list of the graph
        self.adj = []


    def convert_to_csv(self, paths, dim):
        df_points = []
        df_lines = []
        df_triangle = []
        pts_ids = {}

        for i in range (len(self.simplexes[0])):
            smp = self.simplexes[0][i]
            df_points.append((i, smp.coords[0].x, smp.coords[0].y, smp.coords[0].z, smp.weight))
            pts_ids[smp.coords[0]] = i

        create_csv(df_points, ["Node Number", "X", "Y", "Z", "Weight"], paths["points"].format(dim=dim))

        if ("lines" in paths):
            for i in range (len(self.simplexes[1])):
                smp = self.simplexes[1][i]
                df_lines.append((pts_ids[smp.coords[0]], pts_ids[smp.coords[1]], smp.weight))
            create_csv(df_lines, ["P1", "P2", "Weight"], paths["lines"].format(dim=dim))

        if ("triangles" in paths):
            for i in range (len(self.simplexes[2])):
                smp = self.simplexes[2][i]
                df_triangle.append((pts_ids[smp.coords[0]], pts_ids[smp.coords[1]], pts_ids[smp.coords[2]], smp.weight))
            create_csv(df_triangle, ["S1", "S2", "S3", "Weight"], paths["triangles"].format(dim=dim))

    def create_dual(self):
        res = Graph(1)
        for edge in self.simplexes[self.order - 1]:
            neighboors = []
            for neigh in self.adj[edge.ID]:
                neigh = self.simplexes_id[neigh]
                if neigh.order == self.order:
                    neighboors.append(neigh)

            if (len(neighboors) != 2):
                continue

            u = neighboors[0]
            u_coords = u.get_centroid()
            v = neighboors[1]
            v_coords = v.get_centroid()
            w = edge.weight

            res.add_simplex([u_coords], weight = u.weight)
            res.add_simplex([v_coords], weight = v.weight)
            res.add_simplex([u_coords, v_coords], weight = w)
        return res

    def add_simplex(self, coord, weight=0.0):
        new_id = len(self.simplexes_id)
        simplex = Simplex(coord, new_id, weight)

        #Verify if a simplex with the same coordinates already exists
        for smp_orders in self.simplexes[simplex.order]:
            if (smp_orders.coords == coord):
                return smp_orders.ID

        self.simplexes_id.append(simplex)
        self.simplexes[simplex.order].append(simplex)

        self.adj.append([])

        for smp_orders in self.simplexes:
            if smp_orders != simplex.order:
                for smp in smp_orders:
                    #ADD 0_faces:
                    if (simplex.order == 0) and (smp.order == 1 or smp.order == 2) and simplex.coords[0] in smp.coords:
                        self.adj[simplex.ID].append(smp.ID)
                        self.adj[smp.ID].append(simplex.ID)

                    #ADD 1_faces:
                    elif (simplex.order == 1) and (
                            (smp.order == 2 and (simplex.coords[0] in smp.coords and simplex.coords[1] in smp.coords))
                        or  (smp.order == 0 and (simplex.coords[0] in smp.coords or simplex.coords[1] in smp.coords))):
                        self.adj[simplex.ID].append(smp.ID)
                        self.adj[smp.ID].append(simplex.ID)

                    #ADD 2_faces:
                    elif (simplex.order == 2):
                        if  ((smp.order == 0 and (smp.coords[0] in simplex.coords))
                            or  (smp.order == 1 and (smp.coords[0] in simplex.coords and smp.coords[1] in simplex.coords))):
                            self.adj[simplex.ID].append(smp.ID)
                            self.adj[smp.ID].append(simplex.ID)

        return simplex.ID



    def get_neighboors(self, ID):
        return self.adj[ID]

    def to_string(self):
        strs = [elm.to_string() for elm in self.simplexes]
        return "\n".join(strs)

    def get_map(self):
        map_faces = dict()
        for simp in self.simplexes_id:
            if map_faces.get(simp.weight):
                map_faces[simp.weight].add(simp.ID)
            else:
                map_faces[simp.weight] = {simp.ID}
        return map_faces
