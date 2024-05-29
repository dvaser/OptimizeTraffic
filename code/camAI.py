
from ultralytics import YOLO
import time

class CAM:
    def __init__(self, cam_num, source):
        self.model = YOLO('model/yolov8s.pt')
        self.classes = [2, # car
                        5, # bus
                        7, # truck
                        ]
        # self.model = YOLO('model/carModel.pt')
        # self.classes = [0] # car
        self.cam_num = cam_num
        self.source = source
        self.cam = self.createCAM()
    
    def createCAM(self):
        return {
            "port" : f"{self.cam_num}",
            "model" : self.model.predict(
                source=f"--camera {self.source}", 
                conf=0.85, 
                classes=self.classes, 
                show=True, 
                stream=True, 
                save=False
            ),
            "runtime" : time.time(),
            "tls_port": f"--tls {self.cam_num}",
            "vehicle_count" : 0,
            "all_count" : [],   # All vehicle count at runtime
        }

    def closeCAM(self):
        self.model.close()

    def __return__(self):
        return self.cam

""" EXAMPLE
    ? cam = CAM(cam_num="CAM_0", source=0).__return__()
    ? print(cam)
"""