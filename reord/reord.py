from logging import raiseExceptions
from graph_structure import Graph, Coordinates
from operator import itemgetter
from copy import deepcopy

def get_minimas(F):
    minimas = []
    for face in F.simplexes[2]:
        if face.weight == 0:
            minimas.append(face.ID)
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
            deja_vu.append(b)

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
                    queue.append((cost, c, b))
    
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

g = Graph()

g.add_simplex([Coordinates((0,0,0))], 2)
g.add_simplex([Coordinates((1,0,0))], 3)
g.add_simplex([Coordinates((0,1,0))], 1)

g.add_simplex([Coordinates((0,0,0)), Coordinates((1,0,0))], 9)
g.add_simplex([Coordinates((0,0,0)), Coordinates((0,1,0))], 8)
g.add_simplex([Coordinates((1,0,0)), Coordinates((0,1,0))], 7)

g.add_simplex([Coordinates((0,0,0)), Coordinates((1,0,0)), Coordinates((0,1,0))], 0)

g.add_simplex([Coordinates((1,1,0))], 4)

g.add_simplex([Coordinates((1,1,0)), Coordinates((0,1,0))], 11)
g.add_simplex([Coordinates((1,0,0)), Coordinates((1,1,0))], 10)

g.add_simplex([Coordinates((1,1,0)), Coordinates((1,0,0)), Coordinates((0,1,0))], 3)

print(g.adj)
print(f'[{",".join([str(simplex.weight) for simplex in g.simplexes_id])}]')
print(g.dual_adj)

print("\nRevaluation\n")

g = reord_algorithm(g)
print(g.adj)
print(f'[{",".join([str(simplex.weight) for simplex in g.simplexes_id])}]')
print(g.dual_adj)