from gpiozero import LED
from time import sleep

class TrafficLight:
    def __init__(self, green_pin, yellow_pin, red_pin):
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
    
    def transition_to(self, target_light):
        if target_light == "green":
            if self.current_light == "red":
                self.set_yellow()
                sleep(1)  # 1 saniye sarı ışık süresi
            self.set_green()
            sleep(5)
        elif target_light == "red":
            if self.current_light == "green":
                self.set_yellow()
                sleep(1)
            self.set_red()
            sleep(3)
        elif target_light == "yellow":
            self.set_yellow()

