import vtk
import pandas as pd

def init_points(vtk_pts, points):
    points.apply(lambda x: vtk_pts.InsertPoint(int(x[0]), x[1], x[2], x[3]), axis = 1)

def init_cell(x):
    cell = vtk.vtkTriangle()
    Ids = cell.GetPointIds()
    for kId in range(len(x)):
        Ids.SetId(kId,int(x[kId]))
    return cell

def init_faces(vtk_cells, faces):
    faces.apply(lambda x: vtk_cells.InsertNextCell(init_cell(x)), axis = 1)

def build_line(points):
    line = vtk.vtkLine()
    line.GetPointIds().SetId(0, points[0])
    line.GetPointIds().SetId(1, points[1])
    return line

def init_lines(vtk_cells, lines):
    lines.apply(lambda x: vtk_cells.InsertNextCell(build_line(x)), axis = 1)

def main():
    faces = pd.read_csv("faces_split_ex2.csv")
    points = pd.read_csv("points_ex2.csv")
    lines = pd.read_csv("lines_ex2.csv")
    
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

    vectors = vtk.vtkDoubleArray()
    vectors.SetNumberOfTuples(5)
    vectors.SetName("Vector Field")
    vectors.SetNumberOfComponents(3)
    vectors.SetTuple3(0,1,1,10)

    vtk_poly.GetPointData().AddArray(vectors)
    vtk_poly.GetPointData().SetActiveVectors("Vector Field")

    arrow_source = vtk.vtkArrowSource()

    add_arrows = vtk.vtkGlyph3D()
    add_arrows.SetInputData(vtk_poly)
    add_arrows.SetSourceConnection(arrow_source.GetOutputPort())
    add_arrows.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(add_arrows.GetOutputPort())
    """
    array = vtk.vtkDoubleArray()
    array.SetNumberOfComponents(3)
    array.SetName("Three Components")
    array.SetNumberOfTuples(300)
    for i in range(300):
        array.SetTuple3(i,1,1,10)

    vtk_poly.GetPointData().SetVectors(array)
    vtk_poly.GetPointData().SetActiveVectors("Three Components")

    arrow = vtk.vtkArrowSource()
    arrow.Update()

    glyph = vtk.vtkGlyph3D()
    arrowSize=0.02
    glyph.SetScaleFactor(arrowSize)
    glyph.SetSourceData(arrow.GetOutput())
    glyph.SetInputData(vtk_poly)
    glyph.SetVectorModeToUseNormal()
    glyph.Update()
    """
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName('output.vtp')
    writer.SetInputData(vtk_poly)


    writer.Write()
if __name__ == "__main__":
    main()
