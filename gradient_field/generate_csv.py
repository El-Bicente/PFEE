from reord.graph_structure import Graph, Coordinates

def build_paper_example():
    graph = Graph()

    # Create vertices
    graph.add_simplex([Coordinates((0, 0, 0))], 3)
    graph.add_simplex([Coordinates((2, 3.5, 0))], 10)
    graph.add_simplex([Coordinates((4, 0, 0))], 13)
    graph.add_simplex([Coordinates((6, 3.5, 0))], 11)
    graph.add_simplex([Coordinates((8, 0, 0))], 12)
    graph.add_simplex([Coordinates((4, -1.5, 0))], 9)
    graph.add_simplex([Coordinates((4, -3, 0))], 14)

    # Create edges
    graph.add_simplex([Coordinates((0, 0, 0)), Coordinates((4, 0, 0))], 2)
    graph.add_simplex([Coordinates((0, 0, 0)), Coordinates((2, 3.5, 0))], 3)
    graph.add_simplex([Coordinates((2, 3.5, 0)), Coordinates((4, 0, 0))], 6)
    graph.add_simplex([Coordinates((2, 3.5, 0)), Coordinates((6, 3.5, 0))], 7)
    graph.add_simplex([Coordinates((4, 0, 0)), Coordinates((6, 3.5, 0))], 5)
    graph.add_simplex([Coordinates((4, 0, 0)), Coordinates((8, 0, 0))], 8)
    graph.add_simplex([Coordinates((6, 3.5, 0)), Coordinates((8, 0, 0))], 1)

    # Create faces
    graph.add_simplex([Coordinates((0, 0, 0)), Coordinates((2, 3.5, 0)), Coordinates((4, 0, 0))], 2)
    graph.add_simplex([Coordinates((2, 3.5, 0)), Coordinates((4, 0, 0)), Coordinates((6, 3.5, 0))], 4)
    graph.add_simplex([Coordinates((4, 0, 0)), Coordinates((6, 3.5, 0)), Coordinates((8, 0, 0))], 1)

    return graph