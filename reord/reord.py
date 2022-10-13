from logging import raiseExceptions
from reord.graph_structure import Graph, Coordinates
from operator import itemgetter
from copy import deepcopy
import pandas as pd

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

# Transform a given valued complex F into a 2-1 simplicial stack F_prime
def reord_algorithm(F):
    # Initialization
    F_prime = deepcopy(F)
    deja_vu = get_minimas(F)
    G_past = [[] for _ in range(len(F_prime.dual_adj))]
    queue = []
    for m in deja_vu:
        for h in F.dual_adj[m]:
            if h not in  deja_vu:
                cost = F.simplexes_id[h].weight - F.simplexes_id[m].weight
                if cost >= 0:
                    queue.append((cost, m, h))

    # Propagation until the queue is empty
    cpt = 1
    while queue:
        count, a, b = max(queue,key=itemgetter(0))
        queue.remove((count, a, b))

        # We treat ab when adding it to G_past does not create a cycle or connect
        # two different minima
        if a not in deja_vu or b not in deja_vu:
            cost = F.simplexes_id[b].weight - F.simplexes_id[a].weight
            queue.append((cost, a, b))
            deja_vu.add(b)

            # G_past = G_past U {a,b}
            G_past[a].append(b)
            G_past[b].append(a)

            v = cpt
            cpt += 1

            # F_prime(Dual(ab)) = v
            F_prime.simplexes_id[dual(a, b, F_prime)].weight = v
            F_prime.simplexes_id[b].weight = v

            # We look for the new edges to push
            for c in F.dual_adj[b]:
                cost = F.simplexes_id[c].weight - F.simplexes_id[b].weight
                if cost >= 0:
                    queue.append((cost, b, c))

    # Valuation of the remaining simplices to ensure we obtain a stack

    for i in range(len(F.dual_adj)):
        not_visited = list(set(F.dual_adj[i]).difference(G_past[i]))
        for edge in not_visited:
            # Adding the edge not to make the operation twice
            G_past[edge].append(i)
            F_prime.simplexes_id[dual(edge, i, F_prime)].weight = cpt
            cpt += 1

    for i in range(len(F_prime.simplexes[0])):
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

def find_minimas(graph, id, visited, minimas):
    if id not in visited:
        if all(neighbor not in minimas and graph.simplexes_id[neighbor].weight >= graph.simplexes_id[id].weight
        for neighbor in graph.dual_adj[id]):
            minimas.append(id)
        visited.append(id)

        for neighbor in graph.dual_adj[id]:
            find_minimas(graph, neighbor, visited, minimas)
    return minimas

def set_border_as_minimas(graph):
    for i in range(len(graph.dual_adj)):
        if graph.dual_adj[i] and len(graph.dual_adj[i]) <= 2:
            graph.simplexes_id[i].weight = 0

def set_minimas(graph):
    for simplex in graph.simplexes_id:
        simplex.weight += 100
    first_id = next(i for i, j in enumerate(graph.dual_adj) if j)

    set_border_as_minimas(graph)
    minimas = find_minimas(graph, first_id, [], [])

    for min in minimas:
        graph.simplexes_id[min].weight = 0
    return graph
