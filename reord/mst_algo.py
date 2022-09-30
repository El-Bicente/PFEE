from reord.graph_structure import Graph, Coordinates
from format import csv_to_vtp

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
"""

#https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/

csv_paths = {
    "points" : "function_to_csv/generated_csv/points_mst.csv",
    "lines" : "function_to_csv/generated_csv/lines_mst.csv",
    "output": "format/generated_vtp/output_graph_mst.vtu"
}

def find(parent, i):
    if parent[i] == i:
        return i
    return find(parent, parent[i])

def union(parent, rank, x, y):
    xroot = find(parent, x)
    yroot = find(parent, y)

    # Attach smaller rank tree under root of
    # high rank tree (Union by Rank)
    if rank[xroot] < rank[yroot]:
        parent[xroot] = yroot
    elif rank[xroot] > rank[yroot]:
        parent[yroot] = xroot

    # If ranks are same, then make one as root
    # and increment its rank by one
    else:
        parent[yroot] = xroot
        rank[xroot] += 1

def kruskal_mst(G):
        result_g = Graph()

        result = []  # This will store the resultant MST

        # An index variable, used for sorted edges
        i = 0
        # An index variable, used for result[]
        e = 0

        parent = []
        rank = []

        graph = sorted(G.dual_union_form,
                            key=lambda item: item[2])

        for node_id in range (len(G.dual_vertices)):
            parent.append(node_id)
            rank.append(0)

        # Number of edges to be taken is equal to V-1
        while e < len(G.dual_vertices) - 1:

            # Step 2: Pick the smallest edge and increment
            # the index for next iteration
            u, v, w = graph[i]
            i = i + 1
            x = find(parent, u)
            y = find(parent, v)

            # If including this edge doesn't
            # cause cycle, then include it in result
            # and increment the index of result
            # for next edge
            if x != y:
                e = e + 1
                result.append([u, v, w])
                union(parent, rank, x, y)
            # Else discard the edge
        minimumCost = 0
        print("Edges in the constructed MST")
        for u, v, weight in result:
            minimumCost += weight
            p1 = G.dual_vertices[u]
            p2 = G.dual_vertices[v]
            result_g.add_simplex(p1.coords, p1.weight)
            result_g.add_simplex(p2.coords, p2.weight)
            result_g.add_simplex([p1.coords[0], p2.coords[0]], weight)
            #print("%d -- %d == %f" % (u, v, weight))
        result_g.convert_to_csv(csv_paths)
        csv_to_vtp.main(csv_paths)
        print("Minimum Spanning Tree", minimumCost)

#kruskal_mst(g)
