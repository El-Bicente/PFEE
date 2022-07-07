from paraview.simple import *

files= ["../format/output.vtp", 
        "../format/output2.vtp"]

reader = OpenDataFile(files)

if reader:
  print("Success")
  """
  renderView1 = GetActiveView()
  figure = Show(reader)
  figure.SetRepresentationType('Surface With Edges')
  colormap = GetColorTransferFunction('Weight', figure, separate = True)
  colormap.ApplyPreset('X Ray', True)
  
  ResetCamera(renderView1)
  RenderAllViews()
  """
  wavelet1Display = Show(reader)
  wavelet1Display.SetRepresentationType('Surface With Edges')

  # set scalar coloring
  ColorBy(wavelet1Display, 'Weight')

  # set the usage of a Separate Color Map
  wavelet1Display.UseSeparateColorMap = True

  # or use the ColorBy interface directly
  ColorBy(wavelet1Display, 'Weight', separate = True)

  # display the same data in another view for comparison with different color map
  # get layout
  layout1 = GetLayout()

  # split cell
  layout1.SplitHorizontal(0, 0.5)

  renderView1 = GetActiveView()

  # Create a new 'Render View'
  renderView2 = CreateView('RenderView')

  # place view in the layout
  layout1.AssignView(2, renderView2)

  # set active view
  SetActiveView(renderView2)

  wavelet2Display = Show()
  wavelet2Display.SetRepresentationType('Surface With Edges')

  # Use the ColorBy interface to create a separated color map
  ColorBy(wavelet2Display, 'Weight', separate = True)

  # get separate color transfer function/color map for 'RTData'
  separate_wavelet2Display_RTDataLUT = GetColorTransferFunction('Weight', wavelet2Display, separate=True)

  # Apply a preset using its name.
  separate_wavelet2Display_RTDataLUT.ApplyPreset('Linear Green (Gr4L)', True)

  ResetCamera(renderView1)
  ResetCamera(renderView2)
  RenderAllViews()

else:
  print("Failed")
