import time
from trafficLight import TrafficLamp
import os
import shutil

class Algorithm:  
    def __init__(self, roads, traffic_lights):
        self.TLS = TrafficLamp()
        self.roads = roads
        self.traffic_lights = traffic_lights
        self.config()
        self.write_txt(txt="None", counter=0, mode="w")
        self.clear_folder('review')
        self.clear_folder('videos')
        
    def config(self, min_vehicle_threshold=1, margin_err=2, vehicle_departure_time=0.25, max_waiting_time=5):
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
        max_road = None
        
        for road in self.roads:
            if road.state:
                if road.waiting_time > self.max_waiting_time:
                    max_road = road

        if max_road:
            return [False, [info for info in self.vehicle_count_info if info[2] == max_road.road_id]]
        else:
            return [True, None]

    """ Ambulance Road """
    def calc_ambulance_road(self):
        return sorted(self.ambulance_info, key=lambda info: info[0], reverse=False)[-1]

    """ Min Vehicle Road """
    def calc_min_road(self):
        return sorted(self.vehicle_count_info, key=lambda info: info[0], reverse=False)[0]

    """ Max Vehicle Road """
    def calc_max_road(self, max_num=1):
        if max_num==1:            
            return sorted(self.vehicle_count_info, key=lambda info: info[0], reverse=False)[-max_num]
        else:
            return sorted(self.vehicle_count_info, key=lambda info: info[0], reverse=False)[-max_num]

    def write_txt(self, txt, counter, mode="a"):
        if mode == "w":
            with open('docs/run.txt', mode) as file:
                pass
        else:
            with open('docs/run.txt', mode) as file:
                file.write(f'Step: {counter}\n{txt}\n\n')

    def text(self, road_id, type, count, duration, reason):
        if road_id != None:
            return f"Road: {road_id}\nType: {type}\nCount: {count}\nDuration: {duration}\nWaiting Time: {self.roads[road_id].waiting_time}\nREASON: {reason}"
        else:
            return f"Road: {road_id}\nType: {type}\nCount: {count}\nDuration: {duration}\nREASON: {reason}"

    def clear_folder(self, folder_path):
        # Klasörün içeriğini listele
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                # Dosya ise sil
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                # Klasör ise içeriğiyle birlikte sil
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

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
    def run_camera(self, counter):
        for i, road in enumerate(self.roads):
            if road.state:
                count, class_info = road.camera_run(counter)
                info = [count, class_info, road.road_id]
                self.vehicle_count_info.append(info)
                if i == len(self.roads):
                    break

    def run_algorithm(self, counter):
        try:
            self.vehicle_count_info = []
            txt = "None Data"
            self.run_camera(counter)
            if self.isThere_ambulance():
                try:
                    info = self.calc_ambulance_road()
                    duration = self.calc_green_duration(info)
                    txt = self.text(road_id=info[2], type=info[1], count=info[0], duration=duration, reason="Ambulance")
                    self.run_traffic_light(info=info, duration=duration)
                except Exception as ex:
                    print("AMBULANCE EXCEPTION: ",ex)
            else:
                try:
                    print(self.vehicle_count_info)
                    info_min = self.calc_min_road()
                    info_max = self.calc_max_road(max_num=1)
                    info_max_2 = self.calc_max_road(max_num=2)
                    if info_max[0]:
                        waiting_bool, waiting_info = self.calc_max_waiting_time()
                        if waiting_bool:
                            if 0 < info_min[0] <= self.min_vehicle_threshold:
                                info = info_min
                                duration = self.calc_green_duration(info)
                                txt = self.text(road_id=info[2], type=info[1], count=info[0], duration=duration, reason="Min Vehicle Count Road")
                            else:
                                if info_max[0] - self.margin_err <= info_max_2[0]:
                                    if self.calc_average_waiting_time(info_max) >= self.calc_average_waiting_time(info_max_2):
                                        info = info_max
                                        duration = self.calc_green_duration(info)
                                        txt = self.text(road_id=info[2], type=info[1], count=info[0], duration=duration, reason="Max Vehicle Count Road")
                                    else:
                                        info = info_max_2
                                        duration = self.calc_green_duration(info)
                                        txt = self.text(road_id=info[2], type=info[1], count=info[0], duration=duration, reason="Max Vehicle Count (For Waiting Time) Road")
                                else:
                                    info = info_max
                                    duration = self.calc_green_duration(info)
                                    txt = self.text(road_id=info[2], type=info[1], count=info[0], duration=duration, reason="Max Vehicle Count Road")
                            self.run_traffic_light(info=info, duration=duration)
                        else:
                            info = waiting_info[0]
                            duration = self.calc_green_duration(info)
                            txt = self.text(road_id=info[2], type=info[1], count=info[0], duration=duration, reason="Max Waiting Time Road")
                            self.run_traffic_light(info=info, duration=duration)
                    else:
                        txt = self.text(road_id=None, type=None, count=0, duration=0, reason="Saving Mode")
                        self.run_traffic_light(info="saving_mode", duration=0)
                except Exception as ex:
                    print("BURADA EXCEPTON: ", ex)
                    
            for road in self.roads:
                if road.state:
                    if road.road_id != info[2]:
                        road.set_waiting_times(duration=duration)
                    else:
                        road.set_waiting_times(duration=0)
        except Exception as ex:
            print("EXCEPTION: ", ex)
        finally:
            self.write_txt(txt=txt, counter=counter)
