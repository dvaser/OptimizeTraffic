"""
from ultralytics import YOLO


model = YOLO('models/yolov8s.pt')

cam = model.predict(source="/dev/video0",conf=0.85)
"""



"""
import cv2
# print(cv2.VideoCapture(1).isOpened())

# Kamera cihazını tanımla
cap = cv2.VideoCapture(0)

# Kamera cihazı başarıyla açıldı mı diye kontrol et
if not cap.isOpened():
    print("Kamera cihazı açılamadı.")
    exit()

# Kamera görüntüsünü oku ve göster
while True:
    ret, frame = cap.read()  # Görüntüyü oku
    if not ret:
        print("Görüntü alınamadı.")
        break
    
    cv2.imshow('Kamera Görüntüsü', frame)  # Görüntüyü göster
    
    # 'q' tuşuna basıldığında döngüyü sonlandır
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırak
cap.release()
cv2.destroyAllWindows()
"""


"""
import time
import picamera2 as picamera

# Kamera nesnesini oluştur
camera = picamera.Picamera2()

try:
    # Kamera önizlemesini başlat
    camera.start_preview()
    
    # 5 saniye beklet
    time.sleep(5)
    
    # Kamera önizlemesini durdur
    camera.stop_preview()
finally:
    # Kamera kaynağını serbest bırak
    camera.close()
"""