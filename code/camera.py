from picamera2 import Picamera2
import time
import threading
import cv2

class Camera:
    def __init__(self, source):
        self.source = source
        self.cam = Picamera2()
        self.cam.configure(self.cam.create_still_configuration())
        self.cam.start()
        self.vehicles = {}
        self.lock = threading.Lock()

    def process_frame(self):
        # Bu fonksiyon her bir frame'i işleyerek araçları ve pozisyonlarını belirleyecek
        frame = self.cam.capture_array()
        # YOLOv8 ile araç algılama ve konum belirleme kodu buraya gelecek

    def update_vehicle_info(self, vehicle_id, position):
        with self.lock:
            if vehicle_id not in self.vehicles:
                self.vehicles[vehicle_id] = {"position": position, "start_time": time.time()}
            else:
                self.vehicles[vehicle_id]["position"] = position

    def get_waiting_times(self):
        waiting_times = {}
        with self.lock:
            for vehicle_id, info in self.vehicles.items():
                if self.is_vehicle_stopped(info["position"]):
                    waiting_times[vehicle_id] = time.time() - info["start_time"]
        return waiting_times

    def is_vehicle_stopped(self, position):
        # Araç pozisyonuna göre durup durmadığını belirleyecek olan kod
        pass

    def detect_ambulance(self, class_label):
        # YOLOv8 modelinden gelen class label'ı kontrol ederek ambulans olup olmadığını belirle
        return class_label == "truck"

    def run(self):
        while True:
            self.process_frame()
            time.sleep(0.1)  # 100 ms'de bir frame işle
