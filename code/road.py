
class Road:
    def __init__(self, road_id, camera, traffic_light, state=True):
        self.state = state
        self.road_id = road_id
        self.camera = camera
        self.traffic_light = traffic_light
        self.waiting_time = 0

    def set_waiting_times(self, duration=0):
        if duration:
            self.waiting_time += duration
        else:
            self.waiting_time = duration

    def camera_run(self, counter):
        self.camera.yolo_config(yolo_conf=0.25)
        (ambulance_count, car_count) = self.camera.run(graph=True, counter=counter)

        if ambulance_count:
            return ambulance_count, "Ambulance"
        else:
            return car_count, "Car"

    def waiting_time(self):
        return self.waiting_time
