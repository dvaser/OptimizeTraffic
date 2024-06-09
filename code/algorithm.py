import time
from trafficLight import TrafficLamp

class Algorithm:  
    def __init__(self, roads, traffic_lights):
        self.TLS = TrafficLamp()
        self.roads = roads
        self.traffic_lights = traffic_lights
        self.vehicle_count_info = []
        self.config()
        
    def config(self, min_vehicle_threshold=1, margin_err=2, vehicle_departure_time=0.25, max_waiting_time=30):
        self.min_vehicle_threshold = min_vehicle_threshold
        self.margin_err = margin_err
        self.vehicle_departure_time = vehicle_departure_time 
        self.max_waiting_time = max_waiting_time

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
        try:
            print(f"ROAD {info[2]} - waiting time: ", self.roads[info[2]].waiting_time)
            print(f"ROAD {info[2]} - lane: ", self.roads[info[2]].camera.lane_info)
            if info[0]:
                waiting_time = ((info[0] * 1.5) + self.roads[info[2]].waiting_time + (self.roads[info[2]].camera.lane_info * self.vehicle_departure_time)) / info[0]
            else:
                waiting_time = (self.roads[info[2]].waiting_time + (self.roads[info[2]].camera.lane_info * self.vehicle_departure_time)) / 1
        except Exception as ex:
            print("WAITING TIME EXCEPTION: ", ex)
        return waiting_time

    def calc_green_duration(self, info):
        try:
            return (info[0] * 1.5) + (self.roads[info[2]].camera.lane_info * self.vehicle_departure_time)
        except Exception as ex:
            print("GREEN EXCEPTION: ", ex)

    def calc_max_waiting_time(self):
        for i, road in enumerate(self.roads):
            if road.state:
                print(road.waiting_time)
                if road.waiting_time >= self.max_waiting_time:
                    return road.road_id, [info for info in self.vehicle_count_info if info[2] == road.road_id]
                else:
                    return -1, []

    """ Ambulance Road """
    def calc_ambulance_road(self):
        return sorted(self.vehicle_count_info, key=lambda info: info[0], reverse=False)[-1]

    """ Min Vehicle Road """
    def calc_min_road(self):
        return sorted(self.vehicle_count_info, key=lambda info: info[0], reverse=False)[0]

    """ Max Vehicle Road """
    def calc_max_road(self, max_num=1):
        if max_num==1:            
            return sorted(self.vehicle_count_info, key=lambda info: info[0], reverse=False)[-max_num]
        else:
            return sorted(self.vehicle_count_info, key=lambda info: info[0], reverse=False)[-max_num]

    """ Run Traffic Light Library """
    def run_traffic_light(self, info="saving_mode", duration=5):
        if info == "saving_mode":
            self.TLS.traffic_light_system(traffic_lights=self.traffic_lights, info="saving_mode")
        else:
            if not duration:
                duration = 5
            target_road_id = info[2]
            current_road_id = self.TLS.traffic_light_system(traffic_lights=self.traffic_lights, info="run", target_id=target_road_id, green_duration=duration, current_id=self.TLS.current_road_id)
            self.TLS.light_config(target_id=target_road_id, current_id=current_road_id)

    """ Run Road & Camera Library """
    def run_camera(self):
        for i, road in enumerate(self.roads):
            if road.state:
                count, class_info = road.camera_run()
                info = [count, class_info, road.road_id]
                self.vehicle_count_info.append(info)
                if i == len(self.roads):
                    break

    def run_algorithm(self):
        try:
            self.run_camera()
            if self.isThere_ambulance():
                try:
                    print("ambulance")
                    info = self.calc_ambulance_road()
                    duration = self.calc_green_duration(info)
                    self.run_traffic_light(info=info, duration=duration)
                except Exception as ex:
                    print("AMBULANCE EXCEPTION: ",ex)
            else:
                try:
                    info_min = self.calc_min_road()
                    info_max = self.calc_max_road(max_num=1)
                    info_max_2 = self.calc_max_road(max_num=2)
                    if info_max[0]:
                        waiting_info = self.calc_max_waiting_time()
                        if waiting_info[0] == -1:
                            if info_min[0] <= self.min_vehicle_threshold:
                                info = info_min
                                print("min")
                                duration = self.calc_green_duration(info)
                            else:
                                if info_max[0] - self.margin_err <= info_max_2[0]:
                                    if self.calc_average_waiting_time(info_max) >= self.calc_average_waiting_time(info_max_2):
                                        info = info_max
                                        print("max 1")
                                        duration = self.calc_green_duration(info)
                                    else:
                                        info = info_max_2
                                        print("max 2")
                                        duration = self.calc_green_duration(info)

                            self.run_traffic_light(info=info, duration=duration)
                        else:
                            info = waiting_info[1]
                            print("max waiting time")
                            duration = self.calc_green_duration(info)
                            self.run_traffic_light(info=info, duration=duration)
                    else:
                        info = [0, "Car", -1]
                        print("saving mode")
                        duration = self.calc_average_waiting_time(info)
                        self.run_traffic_light(info="saving_mode", duration=0)
                except Exception as ex:
                    print("BURADA EXCEPTON: ", ex)
                    
            for road in self.roads:
                if road.road_id != info[2]:
                    road.set_waiting_times(duration=duration)
                else:
                    road.set_waiting_times(duration=0)

        except Exception as ex:
            print("EXCEPTION: ", ex)

