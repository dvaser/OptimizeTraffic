from trafficLight import TrafficLight
from camera import Camera
from road import Road
import time

current_road_id = 0

traffic_lights = [
        TrafficLight(id= 0, green_pin=5, yellow_pin=21, red_pin=13),  
        TrafficLight(id= 1, green_pin=19, yellow_pin=12, red_pin=6),
        TrafficLight(id= 2, green_pin=20, yellow_pin=26, red_pin=16),
    ]

duration = 5
cameras = [
        Camera(source=0, output_file=f"videos/cam{0}.h264", duration=duration), 
        Camera(source=1, output_file=f"videos/cam{1}.h264", duration=duration), 
        Camera(source=2, output_file=f"videos/cam{2}.h264", duration=duration), 
        Camera(source=3, output_file=f"videos/cam{3}.h264", duration=duration)
    ]

roads = [
        Road(road_id=0, camera=cameras[0], traffic_light=traffic_lights[0]),
        Road(road_id=1, camera=cameras[1], traffic_light=traffic_lights[1]),
        Road(road_id=2, camera=cameras[2], traffic_light=traffic_lights[2]),
        # Road(road_id=3, camera=cameras[3], traffic_light=traffic_lights[3])
    ]


