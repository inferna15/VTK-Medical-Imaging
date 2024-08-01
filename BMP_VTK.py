import vtk
import os
from glob import glob

# BMP dosyalarının bulunduğu klasör
bmp_folder = "C:/Users/fatil/OneDrive/Masaüstü/HURMA_360_72"

# BMP dosyalarını oku ve sıralı hale getir
bmp_files = sorted(glob(os.path.join(bmp_folder, "*.bmp")))

# Görüntü boyutlarını öğrenmek için ilk dosyayı kullan
reader = vtk.vtkBMPReader()
reader.SetFileName(bmp_files[0])
reader.Update()
extent = reader.GetOutput().GetExtent() 
width, height = extent[1] - extent[0] + 1, extent[3] - extent[2] + 1

# VTK'de bir hacim (volume) oluştur
image_data = vtk.vtkImageData()
image_data.SetDimensions(width, height, len(bmp_files))
image_data.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 1) # Bellekte görüntü verisi için yer ayırır.

# BMP dosyalarını okuyup hacim veri setine ekle
for z, bmp_file in enumerate(bmp_files):
    reader.SetFileName(bmp_file)
    reader.Update()
    for y in range(height):
        for x in range(width):
            pixel_value = reader.GetOutput().GetScalarComponentAsFloat(x, y, 0, 0) # Belirli bir pikselin değerini alır.
            image_data.SetScalarComponentFromFloat(x, y, z, 0, pixel_value) # Piksel değerini VTK hacim verisine ekler.

# Volume mapper ve volume oluşturma
volume_mapper = vtk.vtkSmartVolumeMapper() # Normal VolumeMapper'dan daha iyi
volume_mapper.SetInputData(image_data)

volume_property = vtk.vtkVolumeProperty()
volume_property.ShadeOn() # Gölgelendirme Açık
volume_property.SetInterpolationTypeToLinear() # Piksel değerleri arasındaki geçişlerin lineer interpolasyonla yapılmasını sağlar.

'''
* Lineer Interpolasyon (Linear Interpolation):

1 - İki bilinen veri noktası arasındaki doğrusal (düz) bir çizgi boyunca ara değerleri tahmin eder.
2 - Basit ve hızlıdır, ancak bazı durumlarda doğru sonuçlar vermeyebilir.
'''


volume_color = vtk.vtkColorTransferFunction()
'''
"vtkColorTransferFunction", VTK'de hacim görselleştirme sırasında veri değerlerini renk değerlerine eşlemek için 
kullanılan bir sınıftır. Bu sınıf, farklı veri değerlerine belirli renkler atayarak görselleştirmenin daha anlaşılır 
ve estetik olmasını sağlar
'''
volume_color.AddRGBPoint(0, 0.0, 0.0, 0.0)
volume_color.AddRGBPoint(255, 1.0, 1.0, 1.0)
'''
vtkColorTransferFunction, veri değerleri arasında renk geçişlerini düzgün bir şekilde yapar. 
Örneğin, yukarıdaki örnekte, 0 değerinde siyah ve 255 değerinde beyaz olacak şekilde renkler atanmışsa, 
bu iki değer arasındaki tüm değerler gri tonlarında olur. 
Bu, verinin tüm spektrumunu görselleştirmeyi sağlar.
'''
volume_property.SetColor(volume_color)


volume_oppacity = vtk.vtkPiecewiseFunction()
'''
vtkPiecewiseFunction, VTK'de hacim görselleştirme sırasında veri değerlerinin opaklık (şeffaflık) 
ve diğer özelliklerini belirlemek için kullanılan bir sınıftır.
'''
volume_oppacity.AddPoint(0, 0.0)
volume_oppacity.AddPoint(255, 1.0)
volume_property.SetScalarOpacity(volume_oppacity)

volume = vtk.vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)

# Renderer, render window ve render window interactor oluşturma
renderer = vtk.vtkRenderer()
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

renderer.AddVolume(volume)
renderer.SetBackground(0.1, 0.2, 0.3)  # Arka plan rengini ayarla

render_window.Render()
render_window_interactor.Start()