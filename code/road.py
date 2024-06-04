
class Road:
    def __init__(self, road_id, camera, traffic_light):
        self.road_id = road_id
        self.camera = camera
        self.traffic_light = traffic_light

    def get_waiting_times(self):
        # lambda waiting time 
        return sum(self.camera.vehicles)

    def camera_run(self):
        self.camera.yolo_config(yolo_conf=0.25)
        ambulance_count, car_count = self.camera.run()

        if ambulance_count:
            return ambulance_count, "Ambulance"
        else:
            return car_count, "Car"

    def waiting_time(self):
        pass

    def run(self):
        pass