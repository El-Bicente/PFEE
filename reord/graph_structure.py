
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

    def tuple(self):
        return (self.x, self.y, self.z)

class Simplex:
    def __init__(self, coords, vertex_ids, ID, weight):
        self.order = len(coords) - 1
        self.coords = coords
        self.vertex_ids = vertex_ids
        self.weight = weight
        self.ID = ID
        
    def __str__(self):
        res = []
        for count, elm in enumerate(self.coords):
            vertex = ""
            if self.order == 0:
                vertex += str(self.ID) + ": "
            else:
                vertex += str(self.vertex_ids[count]) + ": "
            vertex += str(elm)
            res.append(vertex)
        return "[" + ", ".join(res) + "]"

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

    def add_simplex(self, coords, vertex_ids = [], weight = 0):
        if (id_found := self.get_simplex(coords)):
            return id_found

        simplex = Simplex(coords, vertex_ids, len(self.simplexes_order), weight)
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

    def save(self):
        heads = [("points", "Node Number,X,Y,Z,Weight"), ("lines", "P1,P2,Weight"), ("faces", "S1,S2,S3,Weight")]
        for count, (file_name, head) in enumerate(heads):
            with open(file_name + ".csv", "w") as file:
                csv = head + "\n"
                if count == 0:
                    for smp in self.simplexes[count]:
                        csv += str(smp.ID) + "," + ",".join([str(coord) for coord in smp.coords[0].tuple()]) + "," + str(smp.weight) + "\n"
                else:
                    for smp in self.simplexes[count]:
                        csv += ",".join([str(vertex_id) for vertex_id in smp.vertex_ids]) + "," + str(smp.weight) + "\n"
                file.write(csv)

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
    first_vertex_id = graph.add_simplex([first_vertex], weight=func(first_vertex))

    ## init second vertex (top side)
    second_vertex = first_vertex + main_vector
    second_vertex_id = graph.add_simplex([second_vertex], weight=func(second_vertex))


    ## init edge between first and second vertex
    graph.add_simplex([first_vertex, second_vertex], [first_vertex_id, second_vertex_id], weight=func((first_vertex + second_vertex) / 2))

    ## build lines of simplices side by side
    for _ in range(nb_lines):
        for _ in range(nb_columns):
            ## if the triangle is pointing upwards
            if first_vertex.y < second_vertex.y:
                ## create the third vertex
                third_vertex = second_vertex - main_vector
                third_vertex_id = graph.add_simplex([third_vertex], weight=func(third_vertex))

                ## create edge between second vertex and third vertex
                graph.add_simplex([second_vertex, third_vertex], [second_vertex_id, third_vertex_id], weight=func((second_vertex + third_vertex) / 2))

                ## create edge between first vertex and third vertex
                graph.add_simplex([first_vertex, third_vertex], [first_vertex_id, third_vertex_id],  weight=func((first_vertex + third_vertex) / 2))

            ## if the triangle is pointing downwards
            else:
                ## create the third vertex
                third_vertex = second_vertex + main_vector
                graph.add_simplex([third_vertex], weight=func(third_vertex))

                ## create edge between second vertex and third vertex
                graph.add_simplex([second_vertex, third_vertex], [second_vertex_id, third_vertex_id], weight=func((second_vertex + third_vertex) / 2))

                ## create edge between first vertex and third vertex
                graph.add_simplex([first_vertex, third_vertex], [first_vertex_id, third_vertex_id], weight=func((first_vertex + third_vertex) / 2))


            ## create the face between the three vertices
            graph.add_simplex([first_vertex, second_vertex, third_vertex], [first_vertex_id, second_vertex_id, third_vertex_id], func((first_vertex + second_vertex + third_vertex) / 3))
            first_vertex = second_vertex
            first_vertex_id = second_vertex_id
            second_vertex = third_vertex
            second_vertex_id = third_vertex_id
        
        ## a bit complicated, we will fix it later
        break
    return graph

def wave_function(point: Coordinates):
    return math.sin(math.sqrt(point.x ** 2 + point.y ** 2))


main_vector = Coordinates(x = 1, y = 1, z = 0)
graph = create_graph(wave_function, main_vector, 1, 4)
graph.save()

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
