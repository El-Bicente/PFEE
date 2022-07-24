import vtk
import pandas as pd

def build_point_weights(vtk_ungrid, points):
    pointWeights = vtk.vtkDoubleArray()
    pointWeights.SetName("PointWeight")
    pointWeights.SetNumberOfComponents(1)
    pointWeights.SetNumberOfTuples(vtk_ungrid.GetNumberOfPoints())

    points.apply(lambda x: pointWeights.SetTuple1(int(x[0]), x[4]), axis = 1)
    return pointWeights

def build_weights(vtk_ungrid, cells, name):
    cellWeights = vtk.vtkDoubleArray()
    cellWeights.SetName(name)
    cellWeights.SetNumberOfComponents(1)
    cellWeights.SetNumberOfTuples(vtk_ungrid.GetNumberOfCells())
    cells.apply(lambda x: cellWeights.SetTuple1(int(x[0]), x[1]), axis = 1)
    return cellWeights

def init_points(vtk_pts, points):
    points.apply(lambda x: vtk_pts.InsertPoint(int(x[0]), x[1], x[2], x[3]), axis = 1)

def build_line(points):
    line = vtk.vtkLine()
    line.GetPointIds().SetId(0, int(points[0]))
    line.GetPointIds().SetId(1, int(points[1]))
    return line

def init_lines(vtk_cells, lines):
    """
    return a table with 2 columns {Cell ID (generated by vtk), Weight (read in input)}
    """
    return lines.apply(lambda x: pd.Series({"ID": vtk_cells.InsertNextCell(build_line(x)), "Weight": x[2]}), axis = 1)

def build_cell(x):
    cell = vtk.vtkTriangle()
    Ids = cell.GetPointIds()
    Ids.SetId(0,int(x[0]))
    Ids.SetId(1,int(x[1]))
    Ids.SetId(2,int(x[2]))
    return cell

def init_faces(vtk_cells, faces):
    """
    return a table with 2 columns {Cell ID (generated by vtk), Weight (read in input)}
    """
    return faces.apply(lambda x: pd.Series({"ID": vtk_cells.InsertNextCell(build_cell(x)), "Weight": x[3]}), axis = 1)

def build_tetra(x):
    tetra = vtk.vtkTetra()
    Ids = tetra.GetPointIds()
    Ids.SetId(0, int(x[0]))
    Ids.SetId(1, int(x[1]))
    Ids.SetId(2, int(x[2]))
    Ids.SetId(3, int(x[3]))
    return tetra
    
    
def init_tetras(vtk_cells, tetras):
    """
    return a table with 2 columns {Cell ID (generated by vtk), Weight (read in input)}
    """
    return tetras.apply(lambda x: pd.Series({"ID": vtk_cells.InsertNextCell(build_tetra(x)), "Weight": x[4]}), axis = 1)

def get_vtypes(weights, types):
    vtypes = vtk.vtkUnsignedCharArray()
    vtypes.SetNumberOfComponents(1)
    nb_cells = sum([df.shape[0] for df in weights])
    vtypes.SetNumberOfTuples(nb_cells)
    for i in range(len(weights)):
        df = weights[i]
        tpe = types[i]
        df.apply(lambda x: vtypes.SetTuple1(int(x[0]), tpe), axis = 1)
    return vtypes

def build_vectors(vtk_ungrid_glyph, vectors_dir):
    vectors = vtk.vtkDoubleArray()
    vectors.SetName("Vector Field")
    vectors.SetNumberOfComponents(3)
    vectors.SetNumberOfTuples(vtk_ungrid_glyph.GetNumberOfPoints())
    vectors_dir.apply(lambda x: vectors.SetTuple3(x[0],x[1], x[2], x[3]), axis = 1)
    vtk_ungrid_glyph.GetPointData().AddArray(vectors)
    vtk_ungrid_glyph.GetPointData().SetActiveVectors("Vector Field")

def build_mesh(faces, points, lines, tetras):
    vtk_ungrid = vtk.vtkUnstructuredGrid()

    vtk_pts = vtk.vtkPoints()
    vtk_cells = vtk.vtkCellArray()

    init_points(vtk_pts, points)
    
    lines_weight = init_lines(vtk_cells, lines)
    faces_weight = init_faces(vtk_cells, faces)
    # tetras_weight = init_tetras(vtk_cells, tetras)
    

    vtypes = get_vtypes([lines_weight, faces_weight, """tetras_weight"""], [vtk.VTK_LINE, vtk.VTK_TRIANGLE, """vtk.VTK_TETRA"""])

    vtk_ungrid.SetPoints(vtk_pts)
    vtk_ungrid.SetCells(vtypes, vtk_cells)

    faces_weight = faces_weight.set_index("ID").reindex(range(vtk_ungrid.GetNumberOfCells()), fill_value=float("nan")).reset_index()
    lines_weight = lines_weight.set_index("ID").reindex(range(vtk_ungrid.GetNumberOfCells()), fill_value=float("nan")).reset_index()
    # tetras_weight = tetras_weight.set_index("ID").reindex(range(vtk_ungrid.GetNumberOfCells()), fill_value=float("nan")).reset_index()

    vtk_pts_weight = build_point_weights(vtk_ungrid, points)
    vtk_ungrid.GetPointData().SetScalars(vtk_pts_weight)
    vtk_ungrid.GetPointData().SetActiveScalars("PointWeight")

    vtk_lines_weight = build_weights(vtk_ungrid, lines_weight, "LineWeight")
    vtk_ungrid.GetCellData().AddArray(vtk_lines_weight)

    vtk_faces_weight = build_weights(vtk_ungrid, faces_weight, "FacesWeight")
    vtk_ungrid.GetCellData().AddArray(vtk_faces_weight)
    
    # vtk_tetras_weight = build_weights(vtk_ungrid, tetras_weight, "TetrasWeight")
    # vtk_ungrid.GetCellData().AddArray(vtk_tetras_weight)

    writer = vtk.vtkXMLUnstructuredGridWriter()
    writer.SetFileName('output.vtu')
    writer.SetInputData(vtk_ungrid)

    writer.Write()

def build_glyph(vectors_pts, vectors_dir):
    vtk_ungrid_glyph = vtk.vtkUnstructuredGrid()
    vtk_vec_pts = vtk.vtkPoints()

    init_points(vtk_vec_pts, vectors_pts)
    vtk_ungrid_glyph.SetPoints(vtk_vec_pts)

    build_vectors(vtk_ungrid_glyph, vectors_dir)
    arrow_source = vtk.vtkArrowSource()

    add_arrows = vtk.vtkGlyph3D()
    add_arrows.SetInputData(vtk_ungrid_glyph)
    add_arrows.SetSourceConnection(arrow_source.GetOutputPort())
    add_arrows.Update()

    writer = vtk.vtkXMLUnstructuredGridWriter()
    writer.SetInputConnection(add_arrows.GetOutputPort())
    writer.SetFileName('output2.vtu')
    writer.SetInputData(vtk_ungrid_glyph)

    writer.Write()

def main():
    faces = pd.read_csv("graph/cells.csv")
    points = pd.read_csv("graph/points.csv")
    lines = pd.read_csv("graph/lines.csv")
    tetras = pd.read_csv("tetra.csv")

    # vectors_pts = pd.read_csv("vectors.csv")
    # vectors_dir = pd.read_csv("vectors_dir.csv")

    build_mesh(faces, points, lines, tetras)
    # build_glyph(vectors_pts, vectors_dir)

if __name__ == "__main__":
    main()
