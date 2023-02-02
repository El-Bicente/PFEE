from paraview.simple import *

files= ["../format/output.vtp"]

reader = OpenDataFile(files)

if reader:
  print("Success")

  display = Show(reader)

  layoutPoint = GetLayout()
  layoutLine = GetLayout()
  layoutFace = GetLayout()

  renderViewPoint = CreateView('RenderView')
  renderViewLine = CreateView('RenderView')
  renderViewFace = CreateView('RenderView')

  # place view in the layout
  layoutPoint.AssignView(0, renderViewPoint)

  pointDisplay = Show()
  pointDisplay.SetRepresentationType('Surface With Edges')

  # Use the ColorBy interface to create a separated color map
  ColorBy(pointDisplay, 'PointWeight', separate = True)

  # get separate color transfer function/color map for 'RTData'
  separate_linesDisplay_RTDataLUT = GetColorTransferFunction('PointWeight', pointDisplay, separate=True)

  # Apply a preset using its name.
  separate_linesDisplay_RTDataLUT.ApplyPreset('Linear Green (Gr4L)', True)

  # VECTOR
  reader = OpenDataFile("../format/output2.vtp")
  Show(reader)

  ResetCamera(renderViewPoint)
  ResetCamera(renderViewLine)
  ResetCamera(renderViewFace)

  RenderAllViews()

else:
  print("Failed")
