import vtk

reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName("C:/Users/Admin/Documents/Documents/Dicoms/beyin")
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

#

value = 128

lookupTable = vtk.vtkLookupTable()
lookupTable.SetNumberOfTableValues(256)  # Gri tonlama için 256 seviye
lookupTable.SetRange(0, value)  # Piksel değer aralığı
lookupTable.Build()

# Renk tablosuna birkaç örnek renk ekleyin
lookupTable.SetTableValue(0, 0.0, 0.0, 0.0, 1.0)  # Siyah
lookupTable.SetTableValue(100, 1.0, 1.0, 0.0, 1.0)  # Kırmızı

# 4. Görüntüyü Renk Tablosuna Bağlayın
imageMapToColors = vtk.vtkImageMapToColors()
imageMapToColors.SetInputConnection(reslice.GetOutputPort())
imageMapToColors.SetLookupTable(lookupTable)
imageMapToColors.Update()

#

mapper = vtk.vtkImageMapper()
mapper.SetInputConnection(imageMapToColors.GetOutputPort())
mapper.SetColorWindow(100)
mapper.SetColorLevel(50)

actor = vtk.vtkActor2D()
actor.SetMapper(mapper)

renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0, 0, 0)

renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)

renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# İleri ve geri hareket için offset değeri
offset = 0

offsetText = vtk.vtkTextActor()
offsetText.SetDisplayPosition(60, 20)
offsetText.GetTextProperty().SetJustificationToCentered()
offsetText.GetTextProperty().SetFontSize(18)
renderer.AddActor(offsetText)

valueText = vtk.vtkTextActor()
valueText.SetDisplayPosition(60, 40)
valueText.GetTextProperty().SetJustificationToCentered()
valueText.GetTextProperty().SetFontSize(18)
renderer.AddActor(valueText)

def key_press(obj, event):
    key = obj.GetKeySym()
    global offset
    global value

    if key == "Left":
        offset -= 0.5
    elif key == "Right":
        offset += 0.5
    elif key == "Up":
        if value < 256:
            value += 1
    elif key == "Down":
        if value > 1:
            value -= 1

    # Yeni konumu ayarla ve güncelle
    #new_origin = (center[0] + offset, center[1], center[2])  # X ekseni
    #new_origin = (center[0], center[1] + offset, center[2])  # Y ekseni
    new_origin = (center[0], center[1] , center[2] + offset) # Z ekseni
    reslice.SetResliceAxesOrigin(new_origin)
    reslice.Update()
    offsetText.SetInput(f"Offset value: {offset}")

    lookupTable.SetRange(0, value)
    lookupTable.Build()
    valueText.SetInput(f"Color value: {value}")

    renderWindow.Render()


renderWindowInteractor.AddObserver("KeyPressEvent", key_press)

renderWindow.Render()
renderWindowInteractor.Start()