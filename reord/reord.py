from logging import raiseExceptions
from reord.graph_structure import Graph, Coordinates, Simplex
from operator import itemgetter
from copy import deepcopy
import pandas as pd
import os
from format import csv_to_vtp

def get_minimas(F):
    minimas = set()
    for face in F.simplexes[2]:
        if face.weight == 0:
            minimas.add(face.ID)
    return minimas

def dual(a, b, F):
    coords_a = F.simplexes_id[a].coords
    coords_b = F.simplexes_id[b].coords
    for edge in F.simplexes[1]:
        if edge.coords[0] in coords_a and edge.coords[1] in coords_a and \
           edge.coords[0] in coords_b and edge.coords[1] in coords_b:
           return edge.ID
    raiseExceptions("Edge not found")

def get_diagonaly_neighbors(graph, faceId, neighbors):
    points = []
    for faceNeighborsId in graph.adj[faceId]:
        otherFace = graph.simplexes_id[faceNeighborsId]
        if otherFace.order == 0:
            points.append(otherFace.ID)

    for pointId in points:
        for pointNeighborsId in graph.adj[pointId]:
            otherFace = graph.simplexes_id[pointNeighborsId]
            if otherFace.order == 2 and otherFace.ID not in neighbors and otherFace.ID != faceId:
                neighbors.append(otherFace.ID)

    return neighbors

def get_face_neighbors(graph, faceId, mode):
    neighbors = []
    for faceNeighborsId in graph.adj[faceId]:
        otherFace = graph.simplexes_id[faceNeighborsId]
        if otherFace.order == 1:
            for edgeNeighborsId in graph.adj[otherFace.ID]:
                face = graph.simplexes_id[edgeNeighborsId]
                if face.order == 2 and face.ID != faceId:
                    neighbors.append(face.ID)

    if mode > 1:
        return get_diagonaly_neighbors(graph, faceId, neighbors)

    return neighbors

def get_face_neighbors_reval(graph, faceId):
    neighbors = []
    for faceNeighborsId in graph.adj[faceId]:
        otherFace = graph.simplexes_id[faceNeighborsId]
        if otherFace.order == 1:
            for edgeNeighborsId in graph.adj[otherFace.ID]:
                face = graph.simplexes_id[edgeNeighborsId]
                if face.order == 2 and face.ID != faceId:
                    neighbors.append(face.ID)

    return neighbors

# Set all weights to 0 for video purpose
def set_to_black(graph):
    for simplex in graph.simplexes_id:
        if simplex.weight == 0:
            simplex.weight = 1000
        else:
            simplex.weight = 0
    return graph

def generate_video_vtp(graph, cpt):
    csv_video_path = {
            "points" : "reord/generate_video/reord_points.csv",
            "lines" : "reord/generate_video/reord_lines.csv",
            "triangles" : "reord/generate_video/reord_triangles.csv",
            "output": f"reord/generate_video/file{cpt}.vtu"
        }

    graph.convert_to_csv(csv_video_path)
    csv_to_vtp.main(csv_video_path)

"""
def supress_tuple_list(l, e, verif):
    res = 0
    for i, elm in enumerate(l):
        in_it = True
        for j, to_verif in enumerate(verif):
            if to_verif and e[j] != elm[j]:
                in_it = False
        if in_it:
            res += 1
            l.pop(i)
    return res
"""

# Transform a given valued complex F into a 2-1 simplicial stack F_prime
def reord_algorithm(F, video = False):
    # Initialization
    F_prime = deepcopy(F)
    deja_vu = get_minimas(F)
    G_past = set()
    queue = []

    for m in deja_vu:
        for h in get_face_neighbors_reval(F, m):
            if h not in deja_vu:
                cost = F.simplexes_id[h].weight - F.simplexes_id[m].weight
                if cost >= 0:
                    queue.append((cost, m, h))

    print(queue)
    # Propagation until the queue is empty
    cpt = 1

    if video:
        dir = 'reord/generate_video'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        F_prime = set_to_black(F_prime)

    while queue:
        cost, a, b = max(queue,key=itemgetter(0))
        queue.remove((cost, a, b))

        # We treat ab when adding it to G_past does not create a cycle or connect
        # two different minima
        if b not in deja_vu:
            print((F_prime.simplexes_id[a].weight, F_prime.simplexes_id[b].weight))
            deja_vu.add(b)

            # G_past = G_past U {a,b}
            G_past.add(dual(a, b, F))

            if video:
                v = 1000
            else:
                v = cpt
            cpt += 1

            # F_prime(Dual(ab)) = v
            F_prime.simplexes_id[dual(a, b, F_prime)].weight = v
            F_prime.simplexes_id[b].weight = v

            if video:
                generate_video_vtp(F_prime, cpt)

            # We look for the new edges to push
            for c in get_face_neighbors_reval(F, b):
                cost = F.simplexes_id[c].weight - F.simplexes_id[b].weight
                if cost >= 0:
                    print("second:", (F.simplexes_id[b].weight, F.simplexes_id[c].weight))
                    queue = list(filter(lambda x: x[2] != c, queue))
                    queue.append((cost, b, c))

    # Valuation of the remaining simplices to ensure we obtain a stack
    for edge in F.simplexes[1]:
        if edge.ID not in G_past:
            # Adding the edge not to make the operation twice
            G_past.add(edge.ID)

            if video:
                F_prime.simplexes_id[edge.ID].weight = 1000
                #generate_video_vtp(F_prime, cpt)
            else:
                F_prime.simplexes_id[edge.ID].weight = cpt
            cpt += 1

    for i in range(len(F_prime.simplexes[0])):
        if video:
                F_prime.simplexes[0][i].weight = 1000
                #generate_video_vtp(F_prime, cpt)
        else:
            F_prime.simplexes[0][i].weight = cpt
        cpt += 1

    return F_prime

def parse_csv(graph, paths):
    if ("points" in paths):
        points = pd.read_csv(paths["points"])
        for _, row in points.iterrows():
            coords = [Coordinates([row['X'], row['Y'], row['Z']])]
            graph.add_simplex(coords, row['Weight'])

    if ("lines" in paths):
        lines = pd.read_csv(paths["lines"])
        for _, row in lines.iterrows():
            coords = [graph.simplexes[0][int(row['P1'])].coords[0], graph.simplexes[0][int(row['P2'])].coords[0]]
            graph.add_simplex(coords, row['Weight'])

    if ("triangles" in paths):
        faces = pd.read_csv(paths["triangles"])
        for _, row in faces.iterrows():
            coords = [graph.simplexes[0][int(row['S1'])].coords[0], graph.simplexes[0][int(row['S2'])].coords[0], graph.simplexes[0][int(row['S3'])].coords[0]]
            graph.add_simplex(coords, row['Weight'])

    return graph

def find_minimas(graph, mode):
    for face in graph.simplexes[2]:
        faceId = face.ID
        neighbors = get_face_neighbors(graph, faceId, mode)

        if mode % 2 == 0:
            if all(graph.simplexes_id[neighbor].weight != 0 and graph.simplexes_id[neighbor].weight > graph.simplexes_id[faceId].weight for neighbor in neighbors):
                graph.simplexes_id[faceId].weight = 0

        if mode % 2 == 1:
            if all(graph.simplexes_id[neighbor].weight != 0 and graph.simplexes_id[neighbor].weight >= graph.simplexes_id[faceId].weight for neighbor in neighbors):
                graph.simplexes_id[faceId].weight = 0



# finding vertices on the border
def set_border_as_minimas(graph):
    visited = set()
    for i in range(len(graph.simplexes[0])):
        vertexId = graph.simplexes[0][i].ID
        if len(graph.adj[vertexId]) <= 9:
            for neighborId in graph.adj[vertexId]:
                if graph.simplexes_id[neighborId].order == 2:
                    graph.simplexes_id[neighborId].weight = 0
                    visited.add(neighborId)

    return visited

map_minima_path = {
            "points" : "function_to_csv/generated_csv/map_minima_points.csv",
            "lines" : "function_to_csv/generated_csv/map_minima_lines.csv",
            "triangles" : "function_to_csv/generated_csv/map_minima_triangles.csv",
            "output": "format/generated_vtp/map_minima_output_graph.vtu"
        }

def set_minimas(graph, mode, map=False):
    """
    for simplex in graph.simplexes_id:
        simplex.weight += 100
    """

    set_border_as_minimas(graph)
    find_minimas(graph, mode)

    if map:
        copy = deepcopy(graph)
        map = set_to_black(copy)
        copy.convert_to_csv(map_minima_path)
        csv_to_vtp.build_graph_mesh(map_minima_path)

    return graph
