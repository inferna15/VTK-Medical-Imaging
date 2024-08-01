import vtk

reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName("C:/Users/fatil/OneDrive/Belgeler/Dicoms/beyin")
reader.Update()

extent = reader.GetDataExtent()
spacing = reader.GetOutput().GetSpacing()
origin = reader.GetOutput().GetOrigin()

print(spacing)
print(origin)

# Görüntü merkezini hesaplama
center = [
    origin[0] + spacing[0] * 0.5 * (extent[0] + extent[1]),
    origin[1] + spacing[1] * 0.5 * (extent[2] + extent[3]),
    origin[2] + spacing[2] * 0.5 * (extent[4] + extent[5])
]

reslice = vtk.vtkImageReslice()
reslice.SetInputConnection(reader.GetOutputPort())
reslice.SetOutputDimensionality(2)
#reslice.SetResliceAxesDirectionCosines(0, 1, 0, 0, 0, 1, 1, 0, 0) # X ekseni
#reslice.SetResliceAxesDirectionCosines(1, 0, 0, 0, 0, 1, 0, 1, 0) # Y ekseni
reslice.SetResliceAxesDirectionCosines(1, 0, 0, 0, 1, 0, 0, 0, 1) # Z ekseni

reslice.SetResliceAxesOrigin(center[0], center[1], center[2])
reslice.GetResliceTransform()

reslice.SetOutputExtent(0,1600,0,800,0,0)
reslice.SetOutputSpacing(0.5, 0.5, 0.5)

mapper = vtk.vtkImageMapper()
mapper.SetInputConnection(reslice.GetOutputPort())
mapper.SetColorWindow(100)
mapper.SetColorLevel(50)

actor = vtk.vtkActor2D()
actor.SetMapper(mapper)

renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)

renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# İleri ve geri hareket için offset değeri
offset = 0


def key_press(obj, event):
    key = obj.GetKeySym()
    global offset

    if key == "Left":
        offset -= 0.5
    elif key == "Right":
        offset += 0.5

    # Yeni konumu ayarla ve güncelle
    #new_origin = (center[0] + offset, center[1], center[2])  # X ekseni
    #new_origin = (center[0], center[1] + offset, center[2])  # Y ekseni
    new_origin = (center[0], center[1] , center[2] + offset) # Z ekseni
    reslice.SetResliceAxesOrigin(new_origin)
    reslice.Update()
    renderWindow.Render()


renderWindowInteractor.AddObserver("KeyPressEvent", key_press)

renderWindow.Render()
renderWindowInteractor.Start()