import math
import numpy as np
import pandas as pd


class Coordinates:
    def __init__(self, coord):
        self.x, self.y, self.z = coord

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

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

    def get_centroid(self):
        if (self.order == 2):
            c_x = (self.coords[0].x + self.coords[1].x + self.coords[2].x) / 3
            c_y = (self.coords[0].y + self.coords[1].y + self.coords[2].y) / 3
            c_z = (self.coords[0].z + self.coords[1].z + self.coords[2].z) / 3

            return Coordinates((c_x, c_y, c_z))
        return -1


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
    def __init__(self, order):
        #List where each position represents the ID and each value represents
        #the simplex
        self.simplexes_id = []
        self.order = order
        self.simplexes = [[] for i in range (self.order + 1)]
        #Adjency list of the graph
        self.adj = []


    def convert_to_csv(self, paths):
        df_points = []
        df_lines = []
        df_triangle = []
        pts_ids = {}

        for i in range (len(self.simplexes[0])):
            smp = self.simplexes[0][i]
            df_points.append((i, smp.coords[0].x, smp.coords[0].y, smp.coords[0].z, smp.weight))
            pts_ids[smp.coords[0]] = i

        create_csv(df_points, ["Node Number", "X", "Y", "Z", "Weight"], paths["points"])

        if ("lines" in paths):
            for i in range (len(self.simplexes[1])):
                smp = self.simplexes[1][i]
                df_lines.append((pts_ids[smp.coords[0]], pts_ids[smp.coords[1]], smp.weight))
            create_csv(df_lines, ["P1", "P2", "Weight"], paths["lines"])

        if ("triangles" in paths):
            for i in range (len(self.simplexes[2])):
                smp = self.simplexes[2][i]
                df_triangle.append((pts_ids[smp.coords[0]], pts_ids[smp.coords[1]], pts_ids[smp.coords[2]], smp.weight))
            create_csv(df_triangle, ["S1", "S2", "S3", "Weight"], paths["triangles"])

        return

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
            for smp in smp_orders:
                #ADD 0_faces:
                if (simplex.order == 0) and (smp.ID != simplex.ID) and (smp.order == 1 or smp.order == 2) and simplex.coords[0] in smp.coords:
                    self.adj[simplex.ID].append(smp.ID)
                    self.adj[smp.ID].append(simplex.ID)

                #ADD 1_faces:
                if (simplex.order == 1) and (smp.ID != simplex.ID) and (
                        (smp.order == 2 and (simplex.coords[0] in smp.coords and simplex.coords[1] in smp.coords))
                    or  (smp.order == 0 and (simplex.coords[0] in smp.coords or simplex.coords[1] in smp.coords))):
                    self.adj[simplex.ID].append(smp.ID)
                    self.adj[smp.ID].append(simplex.ID)

                #ADD 2_faces:
                if (simplex.order == 2) and (smp.ID != simplex.ID):
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
