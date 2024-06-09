from picamera2 import Picamera2
import cv2
import time

class MyCamera:
    def __init__(self, source=0):
        self.source = source
        self.camera = Picamera2(camera_num=self.source)
        self.camera.configure(self.camera.create_preview_configuration(main={"format": 'RGB888', "size": (1920, 1080)}))

    def start_preview(self):
        self.camera.start()
        print("Preview started.")

    def stop_preview(self):
        self.camera.stop()
        print("Preview stopped.")


camera = MyCamera(source=3)

try:
    camera.start_preview()
    while True:
        frame = camera.camera.capture_array()
        cv2.imshow('Preview', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q' tuşuna basılarak çıkış yapılabilir
            break
except KeyboardInterrupt:
    pass
finally:
    camera.stop_preview()
    cv2.destroyAllWindows()
