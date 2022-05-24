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

def main():
    faces = pd.read_csv("faces.csv")
    points = pd.read_csv("points.csv")
    
    vtk_poly = vtk.vtkPolyData()
    vtk_pts = vtk.vtkPoints()
    vtk_cells = vtk.vtkCellArray()

    init_points(vtk_pts, points)
    init_faces(vtk_cells, faces)

    vtk_poly.SetPoints(vtk_pts)
    vtk_poly.SetPolys(vtk_cells)

    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName('output.vtp')
    writer.SetInputData(vtk_poly)

    writer.Write()   
    
if __name__ == "__main__":
    main()
