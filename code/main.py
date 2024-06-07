from trafficLight import TrafficLight
from camera import Camera
from road import Road
from algorithm import Algorithm

traffic_lights = [
        TrafficLight(id= 0, green_pin=0, yellow_pin=0, red_pin=0, state=False),  
        TrafficLight(id= 1, green_pin=26, yellow_pin=20, red_pin=21),
        TrafficLight(id= 2, green_pin=5, yellow_pin=6, red_pin=12),
        TrafficLight(id= 2, green_pin=13, yellow_pin=19, red_pin=16),
    ]

cameras = [
        Camera(source=0, file_name=f"cam{0}", duration=5), 
        Camera(source=1, file_name=f"cam{1}", duration=5), 
        Camera(source=2, file_name=f"cam{2}", duration=5), 
        Camera(source=3, file_name=f"cam{3}", duration=5)
    ]

roads = [
        # Road(road_id=0, camera=cameras[0], traffic_light=traffic_lights[0]),
        Road(road_id=1, camera=cameras[1], traffic_light=traffic_lights[1]),
        Road(road_id=2, camera=cameras[2], traffic_light=traffic_lights[2]),
        Road(road_id=3, camera=cameras[3], traffic_light=traffic_lights[3])
    ]

algo = Algorithm(roads=roads, traffic_lights=traffic_lights)

while True:
    algo.run_algorithm()
