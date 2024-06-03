import cv2
from picamera2.encoders import H264Encoder, Quality
from picamera2 import Picamera2
from ultralytics import YOLO
import time
import threading

class Camera:
    def __init__(self, source=0, output_file="videos/", duration=5):
        self.source = source
        self.cam = Picamera2(camera_num=source)
        self.output_file = output_file
        self.video_config()
        self.yolo_config()
        self.duration = duration
        self.yolo_classes_counts = []
        self.vehicles = {}
        self.lock = threading.Lock()
    
    def video_config(self, size_x=640, size_y=480):
        config = self.cam.create_video_configuration(main={"size": (size_x, size_y), "format": "RGB888"})
        self.cam.configure(config)
        self.encoder = H264Encoder(bitrate=10000000)

    def yolo_config(self, model="yolov8n", yolo_conf=0.80, yolo_classes=[2,5,7]):
        self.model = YOLO(f"models/{model}.pt")
        self.yolo_conf = yolo_conf
        self.yolo_classes = yolo_classes

    def video_start(self):
        self.cam.start()
        self.cam.start_recording(output=self.output_file, encoder=self.encoder, quality=Quality.HIGH)
    
    def video_stop(self):
        self.cam.stop_recording()
        self.cam.stop()
        self.cam.close()
        cv2.destroyAllWindows()

    def yolo_process(self):
        frame = self.cam.capture_array()
        results = self.model.predict(frame, classes=self.yolo_classes, conf=self.yolo_conf)
        self.yolo_classes_counts.append(results[0].boxes.cls.numpy().tolist())

        def display_frame(results):
            annotated_frame = results[0].plot()
            cv2.imshow(f"Camera {self.source}", annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return False
            return True
    
        if not display_frame(results):
            return False
        else:
            return True

    def calculate_yolo_classes(self):
        yolo_classes_count = len(self.yolo_classes_counts)
        if yolo_classes_count == 0:
            yolo_classes_count = 1 
        ambulance_count = sum(1 for sublist in self.yolo_classes_counts if 5 in sublist or 7 in sublist)
        ambulance_count = int((ambulance_count / yolo_classes_count) + .5)
        car_count = sum(sublist.count(2) for sublist in self.yolo_classes_counts)
        car_count =int((car_count / yolo_classes_count) + .5)
        return ambulance_count, car_count

    def run(self):
        try:
            print(f"Source {self.source}")
            self.video_start()
            count = self.duration

            while count:
                if not self.yolo_process():
                    break
                time.sleep(1)
                count -= 1

        except Exception as ex:
            print("EXCEPTION: ", ex)

        finally:
            self.video_stop()
            return self.calculate_yolo_classes()

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


cameras = [2,3] 
for cam in cameras:
    camera = Camera(source=cam, output_file=f"videos/cam{cam}.h264", duration=10)
    camera.yolo_config(yolo_conf=0.25)
    a_c, c_c = camera.run()
    print(a_c, c_c)