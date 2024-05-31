class Road:
    def __init__(self, road_id, camera, traffic_light):
        self.road_id = road_id
        self.camera = camera
        self.traffic_light = traffic_light

    def update_traffic_light(self, target_light):
        self.traffic_light.transition_to(target_light)

    def get_vehicle_count(self):
        return len(self.camera.vehicles)

    def check_for_ambulance(self):
        # Kameradan ambulans tespit etme ve trafik ışığını güncelleme
        for vehicle_id, info in self.camera.vehicles.items():
            if self.camera.detect_ambulance(info["class"]):
                self.update_traffic_light("green")
                break

    def get_waiting_times(self):
        return self.camera.get_waiting_times()
