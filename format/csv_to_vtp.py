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
    faces = pd.read_csv("faces_split.csv")
    points = pd.read_csv("points.csv")
    lines = pd.read_csv("lines.csv")
    
    vtk_poly = vtk.vtkPolyData()
    vtk_pts = vtk.vtkPoints()
    vtk_cells = vtk.vtkCellArray()

    init_points(vtk_pts, points)
    init_lines(vtk_cells, lines)
    init_faces(vtk_cells, faces)

    vtk_poly.SetPoints(vtk_pts)
    vtk_poly.SetPolys(vtk_cells)

    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName('output.vtp')
    writer.SetInputData(vtk_poly)

    writer.Write()   
    
if __name__ == "__main__":
    main()
