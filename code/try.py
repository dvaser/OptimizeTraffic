from ultralytics import YOLO


model = YOLO('models/yolov8s.pt')

cam = model.predict(
                source="libcamera-hello -t 0 --camera 0", 
                conf=0.85, 
                classes=[2,5,7], 
                show=True, 
                stream=False, 
                save=False
            ),