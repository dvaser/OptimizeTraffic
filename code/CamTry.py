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
                if not self.display_frame(results):
                    break
                time.sleep(1)
                count -= 1
        finally:
            self.stop()


cameras = 4
for cam in range(cameras):
    camera = CAM(source=cam, output_file=f"videos/cam{cam}.h264", duration=5)
    camera.run()
