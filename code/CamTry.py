import cv2
import threading
from picamera2 import Picamera2
from ultralytics import YOLO

class CAM:
    def __init__(self, source=0):
        self.source = source
        self.picam = Picamera2(source)
        self.picam.preview_configuration.main.format = "RGB888"
        self.picam.preview_configuration.align()
        self.picam.configure("preview")
        self.picam.start()
        self.model = YOLO("models/yolov8n.pt")
        self.is_running = False

    def capture_frame(self):
        return self.picam.capture_array()

    def run_yolo_inference(self, frame):
        return self.model(frame)

    def display_frame(self, frame):
        annotated_frame = frame.plot()
        cv2.imshow(f"Camera {self.source}", annotated_frame)

    def start(self):
        self.is_running = True
        while self.is_running:
            frame = self.capture_frame()
            results = self.run_yolo_inference(frame)
            self.display_frame(results[0])

            if cv2.waitKey(1) == ord("q"):
                break

        self.picam.stop()

    def stop(self):
        self.is_running = False

def create_cameras(num_cameras=1):
    cameras = []
    for i in range(num_cameras):
        camera = CAM(source=i)
        cameras.append(camera)
    return cameras

""""""
if __name__ == "__main__":
    cameras = create_cameras(num_cameras=4)
    threads = []

    for cam in cameras:
        thread = threading.Thread(target=cam.start)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    cv2.destroyAllWindows()