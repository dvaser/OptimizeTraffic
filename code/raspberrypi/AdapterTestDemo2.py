from gpiozero import LED
import os
import time

# Define the GPIO pins for LEDs
led_7 = LED(7)
led_11 = LED(11)
led_12 = LED(12)

def main():
    print('Start testing the camera A')
    i2c = "i2cset -y 1 0x70 0x00 0x04"
    os.system(i2c)
    led_7.off()
    led_11.off()
    led_12.on()
    capture(1)
    
    print('Start testing the camera B') 
    i2c = "i2cset -y 1 0x70 0x00 0x05"
    os.system(i2c)
    led_7.on()
    led_11.off()
    led_12.on()
    capture(2)
    
    print('Start testing the camera C')
    i2c = "i2cset -y 1 0x70 0x00 0x06"
    os.system(i2c)
    led_7.off()
    led_11.on()
    led_12.off()
    capture(3)
    
    print('Start testing the camera D')
    i2c = "i2cset -y 1 0x70 0x00 0x07"
    os.system(i2c)
    led_7.on()
    led_11.on()
    led_12.off()
    capture(4)
    
def capture(cam):
    cmd = "libcamera-still -o capture_%d.jpg" % cam
    os.system(cmd)

if __name__ == "__main__":
    main()
    
    led_7.off()
    led_11.off()
    led_12.on()
