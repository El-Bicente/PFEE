from graph_structure import Graph, Coordinates

g = Graph()
print(g.add_simplex([Coordinates((0,0,0))]))
print(g.add_simplex([Coordinates((0,1,0))]))
print(g.add_simplex([Coordinates((0,0,1))]))
print(g.add_simplex([Coordinates((1,1,1))]))

print(g.add_simplex([Coordinates((0,0,0)), Coordinates((0,0,1))], 0.5))
print(g.add_simplex([Coordinates((0,1,0)), Coordinates((1,1,1))]))

print(g.add_simplex([Coordinates((0,0,0)), Coordinates((0,0,1)), Coordinates((0,1,0))], 0.2))
print(g.add_simplex([Coordinates((0,0,0)), Coordinates((0,0,1)), Coordinates((1,1,1))], 0.1))

print(g.adj)
for elm in g.dual_vertices:
    print(elm.ID, elm.weight)
print()
for elm in g.dual_edges:
    print(elm.ID, elm.weight)


g.convert_to_csv()
g.convert_dual_to_csv()
#print(g.simplexes_order)
#print(g.simplexes)
