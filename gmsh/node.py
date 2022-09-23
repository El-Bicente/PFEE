import gmsh
import sys

gmsh.initialize()

gmsh.model.add("test")

# http://gmsh.info/dev/doc/texinfo/gmsh.pdf#265
gmsh.model.addDiscreteEntity(2, 1)

# http://gmsh.info/dev/doc/texinfo/gmsh.pdf#275
gmsh.model.mesh.addNodes(2, 1, [1, 2, 3],
                         [0., 0., 0., 1., 0., 0., 0., 1., 0.])


# http://gmsh.info/dev/doc/texinfo/gmsh.pdf#329
node_tag = gmsh.view.add("Nodes")
gmsh.view.addModelData(node_tag, 0, "test", "NodeData", [1, 2, 3], [[92], [42], [57]])

gmsh.view.write(node_tag, "node.msh")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()