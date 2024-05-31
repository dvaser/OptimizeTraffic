
from gpiozero import LED
from time import sleep

class TrafficLamp:
    """Pins must come in sequence (green-yellow-red)"""
    def __init__(self, *pins):
        self.led_groups = []
        self.connect_pins(*pins)
        self.run_system()

    def connect_pins(self, *pins):
        """Connects the provided pins to LEDs and organizes them into groups."""
        for i in range(0, len(pins), 3):
            group = [LED(pins[j]) for j in range(i, min(i + 3, len(pins)))]
            self.led_groups.append(group)

    def set_led_state(self, led, state):
        """Sets the LED state to on or off."""
        if state:
            led.on()
        else:
            led.off()
        
    def get_led_state(self, led):
        """Returns the current state of the LED (True if on, False if off)."""
        return led.is_lit

    def run_system(self):
        """Runs the traffic light system, turning LEDs on and off in sequence."""
        try:
            while True:
                for group in self.led_groups:
                    for led in group:
                        sleep(0.5)
                        self.set_led_state(led, True)
                        sleep(1)
                        self.set_led_state(led, False)

        except KeyboardInterrupt:
            self.shutdown_system()

    def shutdown_system(self):
        """Shuts down the system, turning off all LEDs."""
        for group in self.led_groups:
            for led in group:
                self.set_led_state(led, False)

t = TrafficLamp(14,15,17,18,27,22,23,24,25)

