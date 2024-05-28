
class DecisionCenter:
    def __init__(self):
        self.kavşak = {
            "road1":{
                "vehicle1":42,
                "vehicle2":35,
                "vehicle5":22
            },
            "road2":{
                "vehicle3":62,
                "vehicle4":55
            }
        }
        self.max_road_id = None
        self.vehicle_margin_err = 0 # Vehicle Count amount of deviation
        self.max_vehicle_count = 0 
        self.max2_vehicle_count = 0

