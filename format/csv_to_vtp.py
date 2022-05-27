import vtk
import pandas as pd

def build_point_weights(vtk_poly, points):
    pointWeights = vtk.vtkDoubleArray()
    pointWeights.SetName("Weight")

    points.apply(lambda x: pointWeights.InsertNextValue(int(x[4])), axis = 1)

    vtk_poly.GetPointData().SetScalars(pointWeights)

def build_lines_weights(vtk_poly, lines):
    lineWeights = vtk.vtkDoubleArray()
    lineWeights.SetName("Weight")

    lines.apply(lambda x: lineWeights.InsertNextValue(int(x[2])), axis = 1)

    vtk_poly.GetLineData().SetScalars(lineWeights)

def build_cell_weights(vtk_poly, cells):
    cellWeights = vtk.vtkDoubleArray()
    cellWeights.SetName("Weight")

    cells.apply(lambda x: cellWeights.InsertNextValue(int(x[3])), axis = 1)

    vtk_poly.GetCellData().SetScalars(cellWeights)

def init_points(vtk_pts, points):
    points.apply(lambda x: vtk_pts.InsertPoint(int(x[0]), x[1], x[2], x[3]), axis = 1)


def build_line(points):
    line = vtk.vtkLine()
    line.GetPointIds().SetId(0, int(points[0]))
    line.GetPointIds().SetId(1, int(points[1]))
    return line

def init_lines(vtk_cells, lines):
    lines.apply(lambda x: vtk_cells.InsertNextCell(build_line(x)), axis = 1)

def build_cell(x):
    cell = vtk.vtkTriangle()
    Ids = cell.GetPointIds()
    Ids.SetId(0,int(x[0]))
    Ids.SetId(1,int(x[1]))
    Ids.SetId(2,int(x[2]))
    return cell

def init_faces(vtk_cells, faces):
    faces.apply(lambda x: vtk_cells.InsertNextCell(build_cell(x)), axis = 1)

def build_vectors(vtk_poly_glyph, vectors_dir):
    vectors = vtk.vtkDoubleArray()
    vectors.SetName("Vector Field")
    vectors.SetNumberOfComponents(3)
    vectors.SetNumberOfTuples(vtk_poly_glyph.GetNumberOfPoints())
    vectors_dir.apply(lambda x: vectors.SetTuple3(x[0],x[1], x[2], x[3]), axis = 1)
    vtk_poly_glyph.GetPointData().AddArray(vectors)
    vtk_poly_glyph.GetPointData().SetActiveVectors("Vector Field")

def build_mesh(faces, points, lines):
    vtk_poly = vtk.vtkPolyData()

    vtk_pts = vtk.vtkPoints()
    vtk_cells = vtk.vtkCellArray()
    vtk_lines = vtk.vtkCellArray()

    init_points(vtk_pts, points)
    init_lines(vtk_lines, lines)
    init_faces(vtk_cells, faces)

    vtk_poly.SetPoints(vtk_pts)
    vtk_poly.SetPolys(vtk_cells)
    vtk_poly.SetLines(vtk_lines)
 
    build_point_weights(vtk_poly, points)
    # build_lines_weights(vtk_poly, lines)
    # build_cell_weights(vtk_poly, faces)

    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName('output.vtp')
    writer.SetInputData(vtk_poly)

    writer.Write()

def build_glyph(vectors_pts, vectors_dir):
    vtk_poly_glyph = vtk.vtkPolyData()
    vtk_vec_pts = vtk.vtkPoints()

    init_points(vtk_vec_pts, vectors_pts)
    vtk_poly_glyph.SetPoints(vtk_vec_pts)

    build_vectors(vtk_poly_glyph, vectors_dir)
    arrow_source = vtk.vtkArrowSource()

    add_arrows = vtk.vtkGlyph3D()
    add_arrows.SetInputData(vtk_poly_glyph)
    add_arrows.SetSourceConnection(arrow_source.GetOutputPort())
    add_arrows.Update()

    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetInputConnection(add_arrows.GetOutputPort())
    writer.SetFileName('output2.vtp')
    writer.SetInputData(vtk_poly_glyph)

    writer.Write()

def main():
    faces = pd.read_csv("cells.csv")
    points = pd.read_csv("points.csv")
    lines = pd.read_csv("lines.csv")
    
    vectors_pts = pd.read_csv("vectors.csv")
    vectors_dir = pd.read_csv("vectors_dir.csv")
    
    build_mesh(faces, points, lines)
    build_glyph(vectors_pts, vectors_dir)

if __name__ == "__main__":
    main()
