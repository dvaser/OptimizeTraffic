







class TrafficIntersection:
    def __init__(self, roads, vehicle_counts, waiting_times):
        self.roads = roads
        self.vehicle_counts = vehicle_counts
        self.waiting_times = waiting_times
        self.max_vehicle_error_margin = 2

    def get_max_vehicle_road(self):
        max_vehicles = max(self.vehicle_counts)
        max_vehicle_index = self.vehicle_counts.index(max_vehicles)
        return self.roads[max_vehicle_index], max_vehicles

    def get_second_max_vehicle_road(self):
        sorted_counts = sorted(self.vehicle_counts, reverse=True)
        second_max_vehicles = sorted_counts[1]
        second_max_vehicle_index = self.vehicle_counts.index(second_max_vehicles)
        return self.roads[second_max_vehicle_index], second_max_vehicles

    def calculate_average(self, road_index):
        total_waiting_time = sum(self.waiting_times[road_index])
        vehicle_count = self.vehicle_counts[road_index]
        return total_waiting_time / vehicle_count

    def determine_traffic_light(self, ambulance_road=None):
        # Check if there's an ambulance
        if ambulance_road is not None:
            max_road = ambulance_road
        else:
            max_road, max_vehicle_count = self.get_max_vehicle_road()
            second_max_road, second_max_vehicle_count = self.get_second_max_vehicle_road()

            # Remove low vehicle count roads
            if max_vehicle_count < self.max_vehicle_error_margin:
                max_road = min(self.vehicle_counts)
            else:
                # Compare average waiting times
                max_road_index = self.roads.index(max_road)
                second_max_road_index = self.roads.index(second_max_road)
                if self.calculate_average(max_road_index) >= self.calculate_average(second_max_road_index):
                    max_road = max_road
                else:
                    max_road = second_max_road

        return max_road

# # Example usage:
# roads = ["Road 1", "Road 2", "Road 3", "Road 4"]
# vehicle_counts = [40, 20, 15, 10]
# waiting_times = [
#     [10, 10, 10],
#     [10, 10, 10],
#     [5, 5, 5],
#     [2, 2, 2]
# ]

# traffic = TrafficIntersection(roads, vehicle_counts, waiting_times)
# print("Green light for:", traffic.determine_traffic_light(ambulance_road=None))
