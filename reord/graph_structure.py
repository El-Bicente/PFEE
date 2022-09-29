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

def create_csv(df, columns, filename):
    res = pd.DataFrame(df)
    res.columns = columns
    res.to_csv(filename, index=False)

class Graph:
    def __init__(self):
        #List where each position represents the ID and each value represents
        #the simplex
        self.simplexes_id = []
        self.simplexes = [[], [], []]
        #Adjency list of the graph
        self.adj = []

        #List of dual graph 0-faces or vertices
        self.dual_vertices = []
        #List of dual graph 1-faces or edges
        self.dual_edges = []
        #Adjency list of the dual_graph
        self.dual_adj = []
        #Dual graph in union_find form
        self.dual_union_form = []


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

    def convert_dual_to_csv(self, paths):
        df_points = []#np.zeros((len(self.simplexes[0]), 5))
        df_lines = []#np.zeros((len(self.simplexes[1]), 3))
        pts_ids = {}

        for i in range (len(self.dual_vertices)):
            smp = self.dual_vertices[i]
            df_points.append((i, smp.coords[0].x, smp.coords[0].y, smp.coords[0].z, smp.weight))
            pts_ids[smp.coords[0]] = i

        for i in range (len(self.dual_edges)):
            smp = self.dual_edges[i]
            df_lines.append((pts_ids[smp.coords[0]], pts_ids[smp.coords[1]], smp.weight))

        create_csv(df_points, ["Node Number", "X", "Y", "Z", "Weight"], paths["points"])
        create_csv(df_lines, ["P1", "P2", "Weight"], paths["lines"])

        return


    def insert_dual(self, simplex_coords, weight):
        new_smp_id = len(self.dual_vertices) + len(self.dual_edges)
        new_simplex = Simplex(simplex_coords, new_smp_id, weight)

        #Verify if 0-face already exists
        #Can't happen with 1-face and there is no 2-faces in dual graph
        if (len(simplex_coords) == 1):
            for i in range (len(self.dual_vertices)):
                simplex = self.dual_vertices[i]
                if simplex.coords == simplex_coords:
                    return i, simplex.ID
            self.dual_vertices.append(new_simplex)
            return len(self.dual_vertices) - 1, new_smp_id

        self.dual_edges.append(new_simplex)
        return len(self.dual_edges) - 1, new_smp_id
        

    #Return a 1-face simplex that is shared by two 2-faces ones
    def find_concurent_2_faces(self, smp1, smp2):
        smp1_neighbors = self.get_neighboors(smp1.ID)
        smp2_neighbors = self.get_neighboors(smp2.ID)
        res = []
        for smp_ID in smp1_neighbors:
            smp = self.simplexes_id[smp_ID]
            if (smp.order == 1 and smp_ID in smp2_neighbors):
                res.append(smp)
        return res[0]

    def add_simplex(self, coord, weight=0.0):
        simplex = Simplex(coord, len(self.simplexes_id), weight)
        self.simplexes_id.append(simplex)
        self.simplexes[simplex.order].append(simplex)

        self.adj.append([])
        self.dual_adj.append([])

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
                    if  (smp.order == 2 and ((smp.coords[0] in simplex.coords and smp.coords[1] in simplex.coords)
                        or  (smp.coords[1] in simplex.coords and smp.coords[2] in simplex.coords)
                        or  (smp.coords[0] in simplex.coords and smp.coords[2] in simplex.coords))):
                        vert1_ID, vert1_ID_global = self.insert_dual([simplex.get_centroid()], simplex.weight)
                        vert2_ID , vert2_ID_global = self.insert_dual([smp.get_centroid()], smp.weight)

                        new_dual_edge = self.find_concurent_2_faces(simplex, smp)
                        edge_ID, edge_ID_global = self.insert_dual([self.dual_vertices[vert1_ID].coords[0], self.dual_vertices[vert2_ID].coords[0]], new_dual_edge.weight)


                        self.dual_adj[vert1_ID_global].append(edge_ID_global)
                        self.dual_adj[vert2_ID_global].append(edge_ID_global)
                        self.dual_adj[edge_ID_global].append(vert2_ID_global)
                        self.dual_adj[edge_ID_global].append(vert1_ID_global)

                        self.dual_union_form.append([vert1_ID, vert2_ID, new_dual_edge.weight])

        return simplex.ID

    def get_neighboors(self, ID):
        return self.adj[ID]

    def to_string(self):
        strs = [elm.to_string() for elm in self.simplexes]
        return "\n".join(strs)
