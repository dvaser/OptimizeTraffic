
import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
import threading

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
        try:
            picam.stop_recording()
            picam.stop()
            picam.close()
        except:
            pass
        print(f"Error capturing video from video device /dev/video{video_device}: {e}")

if __name__ == "__main__":
    # Assuming the video device nodes for the cameras are /dev/video0, /dev/video1, /dev/video2, /dev/video3
    video_devices = [0, 1, 2, 3]
    duration = 20  # Duration for video capture in seconds

    # Create and start threads for each camera with a delay
    threads = []
    for i, video_device in enumerate(video_devices):
        output_file = f"videos/cam{i}.h264"
        thread = threading.Thread(target=capture_video, args=(video_device, output_file, duration))
        threads.append(thread)
        thread.start()
        time.sleep(2)  # Delay to avoid conflicts when starting cameras

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("All video captures completed.")

