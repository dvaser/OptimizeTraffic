import cv2
from picamera2.encoders import H264Encoder, Quality
from picamera2 import Picamera2
from ultralytics import YOLO
import time
import numpy as np

class Camera:
    def __init__(self, source=0, file_name="cam", duration=5):
        self.source = source
        self.output_file = f"videos/{file_name}.h264"
        self.duration = duration
        self.yolo_config()
        self.yolo_classes_counts = []
        self.vehicles = {}
        self.vehicle_loc = []

    def data(self):
        self.yolo_classes_counts = []
        self.vehicles = {}
        self.vehicle_loc = []

    def get_lane_info(self, vehicle_loc_list):
        self.midpoints_loc = []
        self.midpoints = []

        def calc_vehicle_location(vehicle_loc_list, point_tolerance=1.5, threshold=0.6):
            all_positions = []
            position_indices = []
            
            for i, loc in enumerate(vehicle_loc_list):
                for pos in loc:
                    all_positions.append(pos)
                    position_indices.append(i)
            
            clusters = []
            cluster_indices = []
            
            for position, index in zip(all_positions, position_indices):
                added_to_cluster = False
                for cluster, indices in zip(clusters, cluster_indices):
                    if all(np.linalg.norm(np.array(position[:2]) - np.array(p[:2])) <= point_tolerance for p in cluster):
                        cluster.append(position)
                        indices.append(index)
                        added_to_cluster = True
                        break
                if not added_to_cluster:
                    clusters.append([position])
                    cluster_indices.append([index])
            
            averaged_positions = []
            total_detections = len(vehicle_loc_list)
            
            for cluster, indices in zip(clusters, cluster_indices):
                unique_indices = set(indices)
                detection_ratio = len(unique_indices) / total_detections
                if detection_ratio >= threshold:
                    averaged_positions.append(np.mean(cluster, axis=0).tolist())
            
            return averaged_positions
        
        def calc_vehicleBox_midpoint(x, y, w, h):
            mid_x = x + (w / 2)
            mid_y = y + (h / 2)
            return mid_x, mid_y

        def calc():
            self.midpoints_loc = calc_vehicle_location

    def config(self, size_x=640, size_y=480):
        self.camera_config(source=self.source)
        self.video_config(size_x=size_x, size_y=size_y)

    def camera_config(self, source):
        self.cam = Picamera2(camera_num=source)
    
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
        self.vehicle_loc.append(results[0].boxes.xywh.numpy().tolist())

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
            self.data()
            print(f"Source {self.source}")
            self.config()
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


cam = Camera(3,"cam",5)
cam.yolo_config(yolo_conf=0.15)
x = cam.run()
print(x)



