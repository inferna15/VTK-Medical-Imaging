import vtk

# Ayarlar
renWin_width = 640
renWin_height = 480
ren1GradientBackground = 0
ren1GradientColor_r = 0.5
ren1GradientColor_g = 0.6
ren1GradientColor_b = 0.8

isoLevel = 128
opacity = 0.5
color = [0.9804, 0.9216, 0.8431]

# Veri okuma
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName("C:/Users/Admin/Documents/Documents/Dicoms/beyin")
reader.Update()

# Marching Cubes
iso = vtk.vtkMarchingCubes()
iso.SetInputData(reader.GetOutput())
iso.SetValue(0, isoLevel)

# Mapper ve Lookup Table
lut = vtk.vtkLookupTable()
lut.SetHueRange(0.66667, 0.0)
lut.SetSaturationRange(1, 1)
lut.SetValueRange(1, 1)
lut.SetAlphaRange(1, 1)
lut.SetNumberOfColors(255)
lut.Build()

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(iso.GetOutputPort())
mapper.SetLookupTable(lut)
mapper.SetScalarRange(0, 255)

# Actor
isoActor = vtk.vtkActor()
isoActor.SetMapper(mapper)
isoActor.GetProperty().SetOpacity(opacity)

# Renderer ve RenderWindow
ren1 = vtk.vtkRenderer()
ren1.SetBackground(ren1GradientColor_r, ren1GradientColor_g, ren1GradientColor_b)
ren1.AddActor(isoActor)

renWin = vtk.vtkRenderWindow()
renWin.SetSize(renWin_width, renWin_height)
renWin.AddRenderer(ren1)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Metin ekleme
textActor = vtk.vtkTextActor()
textActor.SetDisplayPosition(70, 20)
textActor.GetTextProperty().SetJustificationToCentered()
textActor.GetTextProperty().SetFontSize(18)
ren1.AddActor(textActor)

# Görüntü filtreleme
w2if = vtk.vtkWindowToImageFilter()
w2if.SetInput(renWin)

level = 60

def key_press(obj, event):
    global level
    key = obj.GetKeySym()

    if key == "Left":
        level -= 2
    elif key == "Right":
        level += 2

    textActor.SetInput(f"Iso value: {level}")
    iso.SetValue(0, level)
    renWin.Render()
    


iren.AddObserver("KeyPressEvent", key_press)

# Başlat
iren.Initialize()
renWin.Render()
iren.Start()