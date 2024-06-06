import cv2
from picamera2.encoders import H264Encoder, Quality
from picamera2 import Picamera2
from ultralytics import YOLO
import time
import numpy as np
import matplotlib.pyplot as plt

class Camera:
    def __init__(self, source=0, file_name="cam", duration=5):
        self.source = source
        self.file_name = file_name
        self.output_file = f"videos/{file_name}.h264"
        self.duration = duration
        self.yolo_config()
        self.yolo_classes_counts = []
        self.vehicle_loc = []
        self.lane_info = 0
        self.midpoints_vehicle = []

    def data(self): 
        self.yolo_classes_counts = []
        self.vehicle_loc = []

    def graph_midpoints(self, points, output_file="cam"):
        if not points:
            print("No valid points to plot.")
            return
        
        x, y = zip(*points)
        plt.scatter(x, y, color='blue')

        # Her noktayı etiketleme
        for i, (x_val, y_val) in enumerate(points):
            plt.text(x_val, y_val, f'({x_val:.2f}, {y_val:.2f})', fontsize=9, ha='right')

        # Grafik başlığı ve eksen etiketleri
        plt.title('Points Plot')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')

        # Eksenleri göster
        plt.grid(True)
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')

        plt.savefig(f'review/{output_file}.png')
        plt.show()

    def get_lane_info(self, vehicle_loc_list):
        def calc_vehicle_location(vehicle_loc_list, tolerance=10, threshold=0.6):
            all_positions = []
            position_indices = []
            
            for i, tensor in enumerate(vehicle_loc_list):
                for pos in tensor:
                    # print(pos)
                    all_positions.append(pos)
                    position_indices.append(i)

            # print(all_positions, end="\n\n")
            # print(position_indices, end="\n\n")
            
            clusters = []
            cluster_indices = []
            
            for position, index in zip(all_positions, position_indices):
                added_to_cluster = False
                for cluster, indices in zip(clusters, cluster_indices):
                    if all(np.linalg.norm(np.array(position[:2]) - np.array(p[:2])) <= tolerance for p in cluster):
                        cluster.append(position)
                        indices.append(index)
                        added_to_cluster = True
                        break
                if not added_to_cluster:
                    clusters.append([position])
                    cluster_indices.append([index])
            
            # print(clusters, end="\n\n")
            # print(cluster_indices, end="\n\n")

            averaged_positions = []
            total_detections = len(vehicle_loc_list)
            
            for cluster, indices in zip(clusters, cluster_indices):
                unique_indices = set(indices)
                detection_ratio = len(unique_indices) / total_detections
                # print(detection_ratio, len(unique_indices) , total_detections)
                if detection_ratio >= threshold:
                    averaged_positions.append(np.mean(cluster, axis=0).tolist())
            
            # print(averaged_positions, end="\n\n")
            return averaged_positions
        
        def calc_vehicle_midpoint(x, y, w, h):
            mid_x = x + (w / 2)
            mid_y = y + (h / 2)
            return mid_x, mid_y

        def isThere_same_lane(midpoint_1, midpoint_2, tolerance=30):
            return abs(midpoint_1[1] - midpoint_2[1]) <= tolerance

        def calc_midpoints():
            self.midpoints = []
            for loc in self.midpoints_loc:
                x, y, w, h = loc
                self.midpoints.append(calc_vehicle_midpoint(x,y,w,h))

        def calc_same_y_midpoints():
            self.same_y_midpoints = []
            added_points = set()
            for ind, midpoint_1 in enumerate(self.midpoints):
                if midpoint_1 in added_points:
                    continue
                group = []
                for midpoint_2 in self.midpoints[ind+1:]:
                    if isThere_same_lane(midpoint_1=midpoint_1, midpoint_2=midpoint_2, tolerance=30):
                        group.append(midpoint_2)
                        added_points.add(midpoint_2)
                if group:
                    group.append(midpoint_1)
                    added_points.add(midpoint_1)
                    self.same_y_midpoints.append(group)

        self.midpoints_loc = calc_vehicle_location(vehicle_loc_list=vehicle_loc_list)
        calc_midpoints()
        self.midpoints_vehicle = self.midpoints
        calc_same_y_midpoints()
        return len(self.same_y_midpoints)

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

    def run(self, graph=False):
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
            
            self.lane_info = self.get_lane_info(self.vehicle_loc)
            print(self.lane_info)
        except Exception as ex:
            print("EXCEPTION: ", ex)

        finally:
            self.video_stop()
            try:
                if graph:
                    print(self.midpoints_vehicle)
                    self.graph_midpoints(points=self.midpoints_vehicle, output_file=self.file_name)
            except Exception as ex:
                print("PLOT EXCEPTION: ", ex)
            return self.calculate_yolo_classes()


cam = Camera(1,"cam",5)
cam.yolo_config(yolo_conf=0.15)
x = cam.run(graph=True)
print(x)



