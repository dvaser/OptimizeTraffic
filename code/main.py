from trafficLight import TrafficLight
from camera import Camera
from road import Road

traffic_lights = [
    TrafficLight(green_pin=5, yellow_pin=21, red_pin=13),  
    TrafficLight(green_pin=19, yellow_pin=12, red_pin=6),
    TrafficLight(green_pin=20, yellow_pin=26, red_pin=16),
    ]

duration = 10
cameras = [
    Camera(source=0, output_file=f"videos/cam{0}.h264", duration=duration), 
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
        info = [count, class_info, road.road_id]
        count_info.append(info)

    # Ambulance s?n?f?na sahip yollar? filtreleme
    ambulance_roads = [info for info in count_info if info[1] == 'Ambulance']

    if ambulance_roads:
        # E?er Ambulance yollar varsa, en y�ksek count'a sahip olan? bul
        max_road = max(ambulance_roads, key=lambda info: info[0])
    else:
        # E?er Ambulance yollar yoksa, di?er yollar aras?nda en y�ksek count'a sahip olan? bul
        max_road = max(count_info, key=lambda info: info[0])

    print(max_road)

if __name__ == "__main__":
    main()
