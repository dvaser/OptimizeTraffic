from trafficLight import TrafficLight
from camera import Camera
from road import Road
import time

current_road_id = 0

traffic_lights = [
    TrafficLight(green_pin=5, yellow_pin=21, red_pin=13),  
    TrafficLight(green_pin=19, yellow_pin=12, red_pin=6),
    TrafficLight(green_pin=20, yellow_pin=26, red_pin=16),
    ]

duration = 5
cameras = [
    Camera(source=3, output_file=f"videos/cam{3}.h264", duration=duration), 
    Camera(source=1, output_file=f"videos/cam{1}.h264", duration=duration), 
    Camera(source=2, output_file=f"videos/cam{2}.h264", duration=duration), 
    # Camera(source=3, output_file=f"videos/cam{3}.h264", duration=duration)
    ]

roads = [
    Road(road_id=0, camera=cameras[0], traffic_light=traffic_lights[0]),
    Road(road_id=1, camera=cameras[1], traffic_light=traffic_lights[1]),
    Road(road_id=2, camera=cameras[2], traffic_light=traffic_lights[2]),
    # Road(road_id=3, camera=cameras[3], traffic_light=traffic_lights[3])
    ]

def main():
    count_info = []
    for road in roads:
        count, class_info = road.camera_run()
        road.camera.video_stop()
        info = [count, class_info, road.road_id]
        count_info.append(info)

    ambulance_roads = [info for info in count_info if info[1] == 'Ambulance']

    if ambulance_roads:
        info = max(ambulance_roads, key=lambda info: info[0])
    else:
        info = max(count_info, key=lambda info: info[0])

    target_road_id = info[2]
    print("ROAD_ID: ", target_road_id)

    road_red_light = [road.road_id for road in roads if road.road_id != target_road_id or road.road_id != current_road_id]

    def traffic_system(target, current=0):
        if not current:
            roads[target].traffic_light.set_green()
            for road_id in road_red_light:
                roads[road_id].traffic_light.set_red()
        else:
            roads[current].traffic_light.set_yellow()
            roads[target].traffic_light.set_yellow()
            for road_id in road_red_light:
                roads[road_id].traffic_light.set_red()
            time.sleep(2)
            for road_id in road_red_light:
                roads[road_id].traffic_light.set_red()
            roads[current].traffic_light.set_red()
            roads[target].traffic_light.set_green()
        
        return target_road_id
    
    current_road_id = traffic_system(target=target_road_id, current=current_road_id)

if __name__ == "__main__":
    while True:
        main()
