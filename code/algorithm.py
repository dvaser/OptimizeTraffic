
class DecisionCenter:
    def __init__(self):
        self.crossroad = {
            "road" : [],
            "vehicle_count" : [],
            "waiting_time" : [],
        }
        self.max_road_id = None
        self.vehicle_margin_err = 0 # Vehicle Count amount of deviation
        self.max_vehicle_count = 0 
        self.max2_vehicle_count = 0
    
    def trafficScenario(self):
        pass

    
