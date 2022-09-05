class Coordinates:
    def __init__(self, coord):
        self.x, self.y, self.z = coord
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def to_string(self):
        return f'(x: {self.x}, y: {self.y}, z:{self.z})'

class Simplex:
    def __init__(self, coords, ID, weight):
        self.order = len(coords) - 1
        self.coords = coords
        self.weight = weight
        self.ID = ID
        
    def to_string(self):
        strs = [elm.to_string() for elm in self.coords]
        return "[" + ", ".join(strs) + "]"

class Graph:
    def __init__(self):
        self.simplexes_id = []
        self.simplexes = [[], [], []]
        self.adj = []
        self.dual_adj = []
    
    def add_simplex(self, coord, weight=0):
        simplex = Simplex(coord, len(self.simplexes_id), weight)
        self.simplexes_id.append(simplex)
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

    def get_neighboors(ID):
        return self.adj[ID] + self.dual_adj[ID]

    def to_string(self):
        strs = [elm.to_string() for elm in self.simplexes]
        return "\n".join(strs)

    #def get_d_simpexes(self, order):
    #    return self.simplex[order]

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
