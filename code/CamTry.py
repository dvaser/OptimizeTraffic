"""
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
    cameras = create_cameras(num_cameras=1)
    threads = []

    for cam in cameras:
        thread = threading.Thread(target=cam.start)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    cv2.destroyAllWindows()
"""


import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality

result = Picamera2.global_camera_info()

for r in result:
    print(r)

def capture_image(video_device, output_file):
    try:
        picam = Picamera2(camera_num=video_device)
        image_config = picam.create_still_configuration(main={"size": (640, 480)})
        picam.configure(image_config)
        picam.start()
        # time.sleep(1)  # Give some time for the camera to start
        picam.capture_file(output_file)
        picam.stop()
        picam.close()
        print(f"Captured image from video device /dev/video{video_device} and saved to {output_file}")
    except Exception as e:
        print(f"Error capturing image from video device /dev/video{video_device}: {e}")

def capture_video(video_device, output_file, duration):
    try:
        picam = Picamera2(camera_num=video_device)
        video_config = picam.create_video_configuration(main={"size": (640, 480)})
        picam.configure(video_config)
        picam.start()
        encoder = H264Encoder(bitrate=10000000)
        picam.start_recording(output=output_file, encoder=encoder, quality=Quality.HIGH)
        time.sleep(duration)
        picam.stop_recording()
        picam.stop()
        picam.close()
        print(f"Captured video from video device /dev/video{video_device} and saved to {output_file}")
    except Exception as e:
        picam.stop_recording()
        picam.stop()
        picam.close()
        print(f"Error capturing video from video device /dev/video{video_device}: {e}")


if __name__ == "__main__":
    # Assuming the video device nodes for the cameras are /dev/video0, /dev/video1, /dev/video2, /dev/video3
    video_devices = [0, 1, 2, 3]

    for i, video_device in enumerate(video_devices):
        print(f"Accessing video device /dev/video{video_device}")
        # capture_image(video_device, f"images/cam{i}.jpg")
        duration = 20
        capture_video(video_device, f"videos/cam{i}.h264", duration=duration)
        time.sleep(duration+1)  # Add delay to avoid conflicts