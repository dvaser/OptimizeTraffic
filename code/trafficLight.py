from gpiozero import LED
import time
import random

class TrafficLight:
    def __init__(self, light_id, green_pin, yellow_pin, red_pin, state=True):
        self.id = light_id
        self.state = state
        if state:
            self.green = LED(green_pin)
            self.yellow = LED(yellow_pin)
            self.red = LED(red_pin)
            self.current_light = "red"

    def set_green(self):
        self.green.on()
        self.yellow.off()
        self.red.off()
        self.current_light = "green"

    def set_yellow(self):
        self.green.off()
        self.yellow.on()
        self.red.off()
        self.current_light = "yellow"

    def set_red(self):
        self.green.off()
        self.yellow.off()
        self.red.on()
        self.current_light = "red"

    def set_saving_mode(self):
        self.green.off()
        self.yellow.off()
        self.red.off()
        self.current_light = "saving mode"

# Pin Test
class TrafficLamp:
    def __init__(self):
        self.target_road_id = 0
        self.current_road_id = 0

    """ Raspberry Pi Led pin test """
    def test_pin(self, *pins):
        led_groups = []
        
        def connect_pins(*pins):
            """Connects the provided pins to LEDs and organizes them into groups."""
            for i in range(0, len(pins), 3):
                group = [LED(pins[j]) for j in range(i, min(i + 3, len(pins)))]
                led_groups.append(group)

        def set_led_state(led, state):
            """Sets the LED state to on or off."""
            if state:
                led.on()
            else:
                led.off()
            
        def get_led_state(led):
            """Returns the current state of the LED (True if on, False if off)."""
            return led.is_lit

        def shutdown_system():
            """Shuts down the system, turning off all LEDs."""
            for group in led_groups:
                for led in group:
                    set_led_state(led, False)

        def run():
            
            connect_pins(*pins)

            """Runs the traffic light system, turning LEDs on and off in sequence."""
            try:
                while True:
                    for group in led_groups:
                        for led in group:
                            time.sleep(0.5)
                            set_led_state(led, True)
                            time.sleep(1)
                            set_led_state(led, False)

            except KeyboardInterrupt:
                shutdown_system()

        run()

    """ Save: Target & Current Light """
    def light_config(self, target_id, current_id):
        self.target_road_id = target_id
        self.current_road_id = current_id

    """ Run traffic light mechanism system  """
    def traffic_light_system(self, traffic_lights, info="saving_mode", target_id=0, green_duration=5, current_id=0):
        
        def get_yellow(target, current, yellow_duration=2):
            target.set_yellow()
            current.set_yellow()
            time.sleep(yellow_duration)

        if info == "saving_mode":
            for light in traffic_lights:
                light.set_saving_mode()
            return info
        else:
            while traffic_lights[current_id].state == False:
                current_id = random.randint(0, len(traffic_lights)-1)

            target_light = traffic_lights[target_id]
            current_light = traffic_lights[current_id]

            if target_id != self.current_road_id:
                get_yellow(target_light, current_light, 2)

            for light in traffic_lights:
                if light.state:
                    if light != target_light:
                        light.set_red()
            target_light.set_green()
            time.sleep(green_duration)

            return target_light.id
    

"""TEST"""

'''
traffic_lights = [
    TrafficLight(id= 0, green_pin=5, yellow_pin=21, red_pin=13),  
    TrafficLight(id= 1, green_pin=19, yellow_pin=12, red_pin=6),
    TrafficLight(id= 2, green_pin=20, yellow_pin=26, red_pin=16),
]

light = [
    [0,5],
    [1,3],
    [0,5],
    [2,4],
    [0,5],
    [1,4],
    [2,5],
    [1,3],
    ]

current_id = 0
tls = TrafficLamp()
for l in light:
    current_id = tls.traffic_light_system(traffic_lights=traffic_lights, target_id=l[0], green_duration=l[1], current_id=current_id)
'''


# tls = TrafficLamp()
# tls = tls.test_pin(26, 20, 21, 5, 6, 12, 13, 19, 16)