import gmsh
import sys

gmsh.initialize()

gmsh.model.add("test")

# http://gmsh.info/dev/doc/texinfo/gmsh.pdf#265
gmsh.model.addDiscreteEntity(1, 100)

# http://gmsh.info/dev/doc/texinfo/gmsh.pdf#275
gmsh.model.mesh.addNodes(1, 100, [1, 2, 3, 4],
                         [0., 0., 0., 1., 0., 0., 0., 1., 0., 1., 1., 0.])

# http://gmsh.info/dev/doc/texinfo/gmsh.pdf#279
gmsh.model.mesh.addElements(1, 100, [1], [[1, 2, 3, 4, 5]], [[1, 2, 2, 3, 3, 1, 2, 4, 3, 4]])

# http://gmsh.info/dev/doc/texinfo/gmsh.pdf#329
edge_tag = gmsh.view.add("Edges")
gmsh.view.addModelData(edge_tag, 0, "test", "ElementData", [1, 2, 3, 4, 5], [[100], [200], [300], [400], [500]])

gmsh.view.write(edge_tag, "edge.msh")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()
