
from pip import main
import math

class Coordinates:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __add__(self, other):
        res = Coordinates()
        if isinstance(other, Coordinates):
            res.x = self.x + other.x
            res.y = self.y + other.y
            res.z = self.z + other.z
        else:
            raise ValueError("You try to add Coordinates with something else")
        
        return res
    
    ## Be carefull, it's not a simple vector substraction !!!
    def __sub__(self, other):
        res = Coordinates()
        if isinstance(other, Coordinates):
            res.x = self.x + other.x
            res.y = self.y - other.y
            res.z = self.z + other.z
        else:
            raise ValueError("You try to substract Coordinates with something else")
        
        return res
    
    def __truediv__(self, other):
        res = Coordinates()
        if isinstance(other, int):
            res.x = self.x / other
            res.y = self.y / other
            res.z = self.z / other
        else:
            raise ValueError("You try to divide Coordinates with something else than int")
        
        return res

    def __str__(self):
        return f'(x: {self.x}, y: {self.y}, z:{self.z})'

class Simplex:
    def __init__(self, coords, ID, weight):
        self.order = len(coords) - 1
        self.coords = coords
        self.weight = weight
        self.ID = ID
        
    def __str__(self):
        strs = [str(elm) for elm in self.coords]
        return "[" + ", ".join(strs) + "]"

class Graph:
    def __init__(self):
        self.simplexes_id = []
        self.simplexes_order = []
        self.simplexes = [[], [], []]
        self.adj = []
        self.dual_adj = []
    
    def get_simplex(self, coords):
        simplices = self.simplexes[len(coords) - 1]
        for simplex in simplices:
            if simplex.coords == coords:
                return simplex.ID
        return None

    def add_simplex(self, coords, weight=0):
        if (id_found := self.get_simplex(coords)):
            return id_found

        simplex = Simplex(coords, len(self.simplexes_order), weight)
        self.simplexes_id.append(simplex)
        self.simplexes_order.append(simplex.order)
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

    def __str__(self):
        res = ""
        for count, simplex_name in enumerate(["Vertices", "Edges", "Faces"]):
            res += simplex_name + ": [\n"
            for smp in self.simplexes[count]:
                res += "\t" + str(smp) + ",\n"
            res += "]\n\n"
        return res

def create_graph(func, main_vector, nb_lines, nb_columns):
    ## init graph
    graph = Graph()

    ## init first vertex (left side)
    first_vertex = Coordinates()
    graph.add_simplex([first_vertex], func(first_vertex))

    ## init second vertex (top side)
    second_vertex = first_vertex + main_vector
    graph.add_simplex([second_vertex], func(second_vertex))


    ## init edge between first and second vertex
    graph.add_simplex([first_vertex, second_vertex], func((first_vertex + second_vertex) / 2))

    ## build lines of simplices side by side
    for _ in range(nb_lines):
        for _ in range(nb_columns):
            ## if the triangle is pointing upwards
            if first_vertex.y < second_vertex.y:
                ## create the third vertex
                third_vertex = second_vertex - main_vector
                graph.add_simplex([third_vertex], func(third_vertex))

                ## create edge between second vertex and third vertex
                graph.add_simplex([second_vertex, third_vertex], func((second_vertex + third_vertex) / 2))

                ## create edge between first vertex and third vertex
                graph.add_simplex([first_vertex, third_vertex], func((first_vertex + third_vertex) / 2))

            ## if the triangle is pointing downwards
            else:
                ## create the third vertex
                third_vertex = second_vertex + main_vector
                graph.add_simplex([third_vertex], func(third_vertex))

                ## create edge between second vertex and third vertex
                graph.add_simplex([second_vertex, third_vertex], func((second_vertex + third_vertex) / 2))

                ## create edge between first vertex and third vertex
                graph.add_simplex([first_vertex, third_vertex], func((first_vertex + third_vertex) / 2))


            ## create the face between the three vertices
            graph.add_simplex([first_vertex, second_vertex, third_vertex], func((first_vertex + second_vertex + third_vertex) / 3))
            first_vertex = second_vertex
            second_vertex = third_vertex
        
        ## a bit complicated, we will fix it later
        break
    return graph

def wave_function(point: Coordinates):
    return math.sin(math.sqrt(point.x ** 2 + point.y ** 2))


main_vector = Coordinates(x = 1, y = 1, z = 0)
graph = create_graph(wave_function, main_vector, 1, 4)

print(f"{str(graph)}")


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
"""
