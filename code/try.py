

"""
import cv2
from picamera2 import Picamera2
from ultralytics import YOLO

# Initialize the Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280, 720)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Load the YOLOv8 model
model = YOLO("models/yolov8n.pt")

while True:
    # Capture frame-by-frame
    frame = picam2.capture_array()

    # Run YOLOv8 inference on the frame
    results = model(frame)

    # Visualize the results on the frame
    annotated_frame = results[0].plot()

    # Display the resulting frame
    cv2.imshow("Camera", annotated_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) == ord("q"):
        break

# Release resources and close windows
cv2.destroyAllWindows()
"""

"""
import cv2
from picamera2 import Picamera2, Preview
from ultralytics import YOLO
import time

class CAM:
    def __init__(self, cam_nums):
        self.cameras(cam_nums)

    def cameras(self, cam_nums):
        for s in range(cam_nums):
            self.main(source=s)

    def main(self, source):
        picam2 = Picamera2(source)
        picam2.preview_configuration.main.size = (1280, 720)
        picam2.preview_configuration.main.format = "RGB888"
        picam2.preview_configuration.align()
        picam2.configure("preview")
        picam2.start()

        # Load the YOLOv8 model
        model = YOLO("models/yolov8n.pt")

        while True:
            start = time.time()
            
            # Capture frame-by-frame
            frame = picam2.capture_array()

            # Run YOLOv8 inference on the frame
            results = model(frame)

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Display the resulting frame
            cv2.imshow("Camera", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) == ord("q"):
                break
            if start + 20000:
                break

        # Release resources and close windows
        cv2.destroyAllWindows()


cam = CAM(cam_nums=4)
"""

"""
import cv2
from picamera2 import Picamera2
from ultralytics import YOLO
import time

class CAM:
    def __init__(self, cam_nums):
        self.cam_nums = cam_nums
        self.picam2_list = [Picamera2(camera_num=i) for i in range(cam_nums)]
        self.model = YOLO("models/yolov8n.pt")
        self.init_cameras()

    def init_cameras(self):
        for i, picam2 in enumerate(self.picam2_list):
            picam2.configure(picam2.create_preview_configuration(main={"size": (1280, 720), "format": "RGB888"}))

    def run(self):
        while True:
            for i, picam2 in enumerate(self.picam2_list):
                picam2.start()
                frame = picam2.capture_array()
                picam2.stop()

                results = self.model(frame)
                annotated_frame = results[0].plot()

                cv2.imshow(f"Camera {i}", annotated_frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    self.cleanup()
                    return

        self.cleanup()

    def cleanup(self):
        for picam2 in self.picam2_list:
            picam2.stop()
        cv2.destroyAllWindows()

# Create and run the camera system
cam = CAM(cam_nums=4)
cam.run()
"""

'''
from picamera2 import Picamera2
import time

result = Picamera2.global_camera_info()

for r in result:
    print(r)

picam2d = Picamera2(0)
picam2d.start()
picam2d.capture_file("images/cam0.jpg")
picam2d.stop()

picam2c = Picamera2(1)
picam2c.start()
picam2c.capture_file("images/cam1.jpg")
picam2c.stop()


picam2b = Picamera2(2)
picam2b.start()
picam2b.capture_file("images/cam2.jpg")
picam2b.stop()


picam2a = Picamera2(3)
picam2a.start()
picam2a.capture_file("images/cam3.jpg")
picam2a.stop()'''


'''import time
from picamera2 import Picamera2

def capture_image(camera_num, output_file):
    try:
        picam = Picamera2()
        camera_config = picam.create_still_configuration(main={"size": (640, 480)})
        picam.configure(camera_config)
        picam.start()
        time.sleep(2)  # Give some time for the camera to start
        picam.capture_file(output_file)
        picam.stop()
        picam.close()
        print(f"Captured image from camera {camera_num} and saved to {output_file}")
    except Exception as e:
        print(f"Error capturing image from camera {camera_num}: {e}")

if __name__ == "__main__":
    camera_ids = [
        "/base/axi/pcie@120000/rp1/i2c@80000/pca@70/i2c@0/imx219@10",
        "/base/axi/pcie@120000/rp1/i2c@80000/pca@70/i2c@1/imx219@10",
        "/base/axi/pcie@120000/rp1/i2c@80000/pca@70/i2c@2/imx219@10",
        "/base/axi/pcie@120000/rp1/i2c@80000/pca@70/i2c@3/imx219@10"
    ]

    for i, cam_id in enumerate(camera_ids):
        print(f"Accessing camera {i} with ID {cam_id}")
        capture_image(i, f"images/cam{i}.jpg")
        time.sleep(5)  # Add delay to avoid conflicts
'''

import time
from picamera2 import Picamera2

def capture_image(video_device, output_file):
    try:
        picam = Picamera2(camera_num=video_device)
        camera_config = picam.create_still_configuration(main={"size": (640, 480)})
        picam.configure(camera_config)
        picam.start()
        time.sleep(2)  # Give some time for the camera to start
        picam.capture_file(output_file)
        picam.stop()
        picam.close()
        print(f"Captured image from video device /dev/video{video_device} and saved to {output_file}")
    except Exception as e:
        print(f"Error capturing image from video device /dev/video{video_device}: {e}")

if __name__ == "__main__":
    # Assuming the video device nodes for the cameras are /dev/video0, /dev/video1, /dev/video2, /dev/video3
    video_devices = [0, 1, 2, 3]

    for i, video_device in enumerate(video_devices):
        print(f"Accessing video device /dev/video{video_device}")
        capture_image(video_device, f"images/cam{i}.jpg")
        time.sleep(5)  # Add delay to avoid conflicts
