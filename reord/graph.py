class Face:
    def __init__(self, id, vertices = []):
        self.id = id
        self.dim = len(vertices) - 1
        self.vertices = vertices
        self.parents = []
        self.children = []
    
    def add_neigbor(self, face):
        if face.dim > self.dim and face not in self.parent:
            self.parents.append(face)

        if face.dim < self.dim and face not in self.parent:
            self.children.append(face)

class Graph:
    def __init__(self):
        self.faces_0 = {}
        self.faces_1 = {}
        self.faces_2 = {}

    def add_faces(self, id, vertices):
        face = Face(id, vertices)
        if face.dim == 0:
            self.faces_0[face.id] = face

        elif face.dim == 1:
            self.faces_1[face.id] = face
            self.add_face_1_neighbors(face)

        elif face.dim == 2:
            self.faces_2[face.id] = face
            self.add_face_2_neighbors(face)
    
    def add_face_1_neighbors(self, face):
        for v in face.vertices:
            for vertice in self.faces_0:
                if v in vertice.vertices:
                    vertice.add_neighbor(face)
                    face.add_neighbor(vertice)

    def add_face_2_neighbors(self, face):
        a, b, c = face.vertices
        for edge in self.faces_1:
            if a in edge.vertices and b in edge.vertices or \
                a in edge.vertices and c in edge.vertices or \
                b in edge.vertices and c in edge.vertices :
                edge.add_neighbor(face)
                face.add_neighbor(edge)
        self.add_face_1_neighbors(face)
            
    
