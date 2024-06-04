import time
from trafficLight import TrafficLamp

class Algorithm:  
    def __init__(self, roads, traffic_lights):
        self.TLS = TrafficLamp
        self.roads = roads
        self.traffic_lights = traffic_lights
        self.vehicle_count_info = []
        self.config()
        
    def config(self, min_vehicle_threshold=2, margin_err=2, vehicle_departure_time=0.25):
        self.min_vehicle_threshold = min_vehicle_threshold
        self.margin_err = margin_err
        # second
        self.vehicle_departure_time = vehicle_departure_time 

    """ Is there Ambulance """
    def isThere_ambulance(self):
        self.ambulance_info = [info for info in self.vehicle_count_info if info[1] == 'Ambulance']
        if self.ambulance_info:
            return True
        else:
            return False
    
    """ Calculate Average info """
    def calc_average_waiting_time(self, info):
        """ waiting time """
        return sum(self.roads[info[2]].get_waiting_times(), 
                    (self.roads[info[2]].camera.lane_info * self.vehicle_departure_time)) / info[0]

    """ Ambulance Road """
    def calc_ambulance_road(self):
        return max(self.ambulance_info, key=lambda info: info[0])

    """ Min Vehicle Road """
    def calc_min_road(self):
        return min(self.vehicle_count_info, key=lambda info: info[0])

    """ Max Vehicle Road """
    def calc_max_road(self, max_num=1):
        if max_num==1:            
            return max(self.vehicle_count_info, key=lambda info: info[0])
        else:
            return sorted(self.vehicle_count_info, key=lambda info: info[0], reverse=False)[-max_num]

    """ Run Traffic Light Library """
    def run_traffic_light(self, info="saving_mode"):
        if info == "saving_mode":
            self.TLS.traffic_light_system(traffic_lights=self.traffic_lights, info="saving_mode")
        else:
            target_road_id = info[2]
            current_road_id = self.TLS.traffic_light_system(traffic_lights=self.traffic_lights, info="run", target_id=target_road_id, green_duration=5, current_id=current_road_id)
            self.TLS.light_config(target_id=target_road_id, current_id=current_road_id)

    """ Run Road & Camera Library """
    def run_camera(self):
        for road in self.roads:
            count, class_info = road.camera_run()
            # road.camera.video_stop()
            info = [count, class_info, road.road_id]
            self.vehicle_count_info.append(info)

    def run_algorithm(self):
        try:
            self.run_camera()
            
            if self.isThere_ambulance():
                info = self.calc_ambulance_road()
                self.run_traffic_light(info=info)
            else:
                info_min = self.calc_min_road()
                info_max = self.calc_max_road(max_num=1)
                info_max_2 = self.calc_max_road(max_num=2)
                if info_max[0]:
                    if info_min[0] <= self.min_vehicle_threshold:
                        info = info_min
                    else:
                        if info_max[0] - self.margin_err <= info_max_2[0]:
                            if self.calc_average_waiting_time(info_max) >= self.calc_average_waiting_time(info_max_2):
                                info = info_max
                            else:
                                info = info_max_2

                    self.run_traffic_light(info=info)
                else:
                    self.run_traffic_light(info="saving_mode")

        except Exception as ex:
            print("EXCEPTION: ", ex)

