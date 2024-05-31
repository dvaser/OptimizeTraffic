from trafficLight import TrafficLight
from camera import Camera
from road import Road

# Trafik ışıkları, kameralar ve yolları oluşturun
traffic_lights = [TrafficLight(green_pin=17, yellow_pin=27, red_pin=22),  # Örnek pinler
                  TrafficLight(green_pin=23, yellow_pin=24, red_pin=25),
                  TrafficLight(green_pin=5, yellow_pin=6, red_pin=13),
                  TrafficLight(green_pin=19, yellow_pin=26, red_pin=20)]

cameras = [Camera(source=0), Camera(source=1), Camera(source=2), Camera(source=3)]

roads = [Road(road_id=0, camera=cameras[0], traffic_light=traffic_lights[0]),
         Road(road_id=1, camera=cameras[1], traffic_light=traffic_lights[1]),
         Road(road_id=2, camera=cameras[2], traffic_light=traffic_lights[2]),
         Road(road_id=3, camera=cameras[3], traffic_light=traffic_lights[3])]

def main():
    for road in roads:
        road.check_for_ambulance()
        waiting_times = road.get_waiting_times()
        # Burada bekleme sürelerine göre karar verme algoritması ekleyin

if __name__ == "__main__":
    main()
