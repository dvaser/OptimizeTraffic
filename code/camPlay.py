from camAI import CAM
import time
import numpy as np

class CAMERA:
    def __init__(self):
        try:
            self.camera_count = 1
            self.runtime = 5 # second

            self.cams = [CAM(f"CAM_{i}", i).__return__() for i in range(self.camera_count)]

            while True:
                for cam in self.cams:
                    for cam_step in cam["model"]:
                        cam["all_count"].append(cam_step.boxes.__len__())

                        if time.time() - cam["runtime"] > self.runtime:
                            cam["vehicle_count"] = int(np.average(cam["all_count"]) + 0.5)
                            break
                    break

        except Exception as ex:
            print(ex)

