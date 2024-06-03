
class Road:
    def __init__(self, road_id, camera, traffic_light):
        self.road_id = road_id
        self.camera = camera
        self.traffic_light = traffic_light

    def camera_run(self):
        self.camera.config_start(yolo_conf=0.25)
        ambulance_count, car_count = self.camera.run()

        if ambulance_count:
            return ambulance_count, "Ambulance"
        else:
            return car_count, "Car"
