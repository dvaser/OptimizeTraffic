import cv2
from picamera2.encoders import H264Encoder, Quality
from picamera2 import Picamera2
from ultralytics import YOLO
import time

class CAM:
    def __init__(self, source=0, output_file="videos/", duration=0):
        self.source = source
        self.picam = Picamera2(camera_num=source)
        self.output_file = output_file
        self.config()
        self.yolo_config()
        self.model = YOLO("models/yolov8n.pt")
        self.duration = duration
        self.yolo_classes_counts = [[],]

    def yolo_config(self, yolo_conf=0.80, yolo_classes=[2,5,7]):
        self.yolo_conf = yolo_conf
        self.yolo_classes = yolo_classes

    def config(self):
        video_config = self.picam.create_video_configuration(main={"size": (640, 480), "format": "RGB888"})
        self.picam.configure(video_config)
        self.encoder = H264Encoder(bitrate=10000000)

    def start(self):
        self.picam.start()
        self.picam.start_recording(output=self.output_file, encoder=self.encoder, quality=Quality.HIGH)

    def capture_frame(self):
        return self.picam.capture_array()

    def run_yolo_inference(self, frame):
        return self.model.predict(frame, classes=self.yolo_classes, conf=self.yolo_conf)

    def display_frame(self, results):
        annotated_frame = results[0].plot()
        cv2.imshow(f"Camera {self.source}", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False
        return True
    
    def stop(self):
        self.picam.stop_recording()
        self.picam.stop()
        self.picam.close()
        cv2.destroyAllWindows()

    def run(self):
        try:
            print(f"Source {self.source}")
            self.start()
            count = self.duration

            while count:
                frame = self.capture_frame()
                results = self.run_yolo_inference(frame)

                print("Results")
                for r in results:
                    self.yolo_classes_counts.append(r.boxes.cls.numpy().tolist())

                if not self.display_frame(results):
                    break
                time.sleep(1)
                count -= 1
        finally:
            self.stop()

            return self.calculate_yolo_classes()

    def calculate_yolo_classes(self):
        ambulance_count = sum(1 for sublist in self.yolo_classes_counts if 5 or 7 in sublist)
        ambulance_count = int((ambulance_count / len(self.yolo_classes_counts)) + .5)
        car_count = sum(sublist.count(2) for sublist in self.yolo_classes_counts)
        car_count =int((car_count / len(self.yolo_classes_counts)) + .5)
        return ambulance_count, car_count

cameras = 4
for cam in range(cameras):
    camera = CAM(source=cam, output_file=f"videos/cam{cam}.h264", duration=10)
    camera.yolo_config(yolo_conf=0.25)
    a_c, c_c = camera.run()

print(a_c, c_c)