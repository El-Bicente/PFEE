import gmsh
import sys
import math

gmsh.initialize()

gmsh.model.add("test")

N = 1


# Helper function to return a node tag given two indices i and j:
def tag(i, j):
    return (N + 1) * i + j + 1


# The x, y, z coordinates of all the nodes:
coords = []

# The tags of the corresponding nodes:
nodes = []

# The connectivities of the triangle elements (3 node tags per triangle) on the
# terrain surface:
tris = []

# The connectivities of the line elements on the 4 boundaries (2 node tags
# for each line element):
lin = [[], [], [], []]

# The connectivities of the point elements on the 4 corners (1 node tag for each
# point element):
pnt = [tag(0, 0), tag(N, 0), tag(N, N), tag(0, N)]

for i in range(N + 1):
    for j in range(N + 1):
        nodes.append(tag(i, j))
        coords.extend([
            float(i) / N,
            float(j) / N, 0.05 * math.sin(10 * float(i + j) / N)
        ])
        if i > 0 and j > 0:
            tris.extend([tag(i - 1, j - 1), tag(i, j - 1), tag(i - 1, j)])
            tris.extend([tag(i, j - 1), tag(i, j), tag(i - 1, j)])
        if (i == 0 or i == N) and j > 0:
            lin[3 if i == 0 else 1].extend([tag(i, j - 1), tag(i, j)])
        if (j == 0 or j == N) and i > 0:
            lin[0 if j == 0 else 2].extend([tag(i - 1, j), tag(i, j)])

print(lin)
# Create 4 discrete points for the 4 corners of the terrain surface:
for i in range(4):
    gmsh.model.addDiscreteEntity(0, i + 1)
gmsh.model.setCoordinates(1, 0, 0, coords[3 * tag(0, 0) - 1])
gmsh.model.setCoordinates(2, 1, 0, coords[3 * tag(N, 0) - 1])
gmsh.model.setCoordinates(3, 1, 1, coords[3 * tag(N, N) - 1])
gmsh.model.setCoordinates(4, 0, 1, coords[3 * tag(0, N) - 1])

# Create 4 discrete bounding curves, with their boundary points:
for i in range(4):
    gmsh.model.addDiscreteEntity(1, i + 1, [i + 1, i + 2 if i < 3 else 1])

# Create one discrete surface, with its bounding curves:
gmsh.model.addDiscreteEntity(2, 1, [1, 2, -3, -4])

# Add all the nodes on the surface (for simplicity... see below):
gmsh.model.mesh.addNodes(2, 1, nodes, coords)

# Add point elements on the 4 points, line elements on the 4 curves, and
# triangle elements on the surface:
for i in range(4):
    # Type 15 for point elements:
    gmsh.model.mesh.addElementsByType(i + 1, 15, [], [pnt[i]])
    # Type 1 for 2-node line elements:
    gmsh.model.mesh.addElementsByType(i + 1, 1, [], lin[i])
# Type 2 for 3-node triangle elements:
gmsh.model.mesh.addElementsByType(1, 2, [], tris)

# Reclassify the nodes on the curves and the points (since we put them all on
# the surface before with `addNodes' for simplicity)
gmsh.model.mesh.reclassifyNodes()

# Create a geometry for the discrete curves and surfaces, so that we can remesh
# them later on:
gmsh.model.mesh.createGeometry()

node_tag = gmsh.view.add("Nodes")
gmsh.view.addModelData(node_tag, 0, "test", "NodeData", [1, 2, 3, 4], [[1], [2], [3], [4]])

edge_tag = gmsh.view.add("Edges")
gmsh.view.addModelData(edge_tag, 0, "test", "ElementData", [1, 2, 3], [[100], [200], [300]])

face_tag = gmsh.view.add("Faces")
gmsh.view.addModelData(face_tag, 0, "test", "ElementData", [1], [[150]])


# Launch the GUI to see the results:
if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()
