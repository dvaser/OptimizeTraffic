# !pip install RPi.GPIO

import RPi.GPIO as GPIO
import time

class Pi:
    def __init__(self):
        # GPIO modunu belirleme (BCM veya BOARD)
        GPIO.setmode(GPIO.BCM)
        self.greenPin = 2
        self.yellowPin = 3
        self.redPin = 4
        self.activePin = ''
        self.targetPin = ''
        self.targetPin2 = ''

        self.trafficLamb = 0
        self.targetTLS = 0
        self.targetTLS2 = 0

        self.activeTLS = 0

        self.delayTLS = 0

    # Definition: Pin indexes of leds
    def ledPin(self, *pin):
        for _pin in pin:
            # Set as OUT for pin
            GPIO.setup(_pin, GPIO.OUT)

    # What's the pin status
    def isPinHigh(self, pin):
        return GPIO.input(pin) == GPIO.HIGH

    # 
    def system(self):
        while True:
            self.activeTLS = self.activeTLSPin(self.greenPin, self.trafficLamb)
            self.activePin = (self.activeTLS - 1) * 3 + 2
            self.targetPin = self.TargetPin(self.greenPin, self.targetTLS)
            self.targetPin2 = self.TargetPin(self.greenPin, self.targetTLS2)

            # control
            self.getGreen(self.delayTLS, self.activePin, self.targetPin)

            self.activePin = self.targetPin

            self.getYellow(self.activePin, self.targetPin2)

    # Pin of led is turn HIGH
    def highLED(self, pin):
        GPIO.output(pin, GPIO.HIGH)

    # Pin of led is turn LOW
    def lowLED(self, pin):
        GPIO.output(pin, GPIO.LOW)

    # HIGH/LOW GREEN for GREEN led
    # HIGH/LOW RED for non-GREEN led
    def getGreen(self, delayTLS, active, target):
        # HIGH green
        self.highLED(target)
        # HIGH non-green for Red
        self.highRed(delayTLS, 'g')
        # Set as time for green led
        self.delay(delayTLS*1000)
        # LOW green
        self.lowRed(delayTLS, 'g')
        # LOW non-green for Red
        self.lowLED(target)

    # HIGH/LOW YELLOW for target/active green led
    # HIGH/LOW RED for non-target/non-active green led
    def getYellow(self, active, target):
        # HIGH yellow for target green led
        self.highLED(target+1)
        # HIGH yellow for active green led
        self.highLED(active+1)
        # HIGH non-yellow for Red
        self.highRed(0, 'y')
        # YELLOW time
        self.delay(2500)
        # LOW non-yellow for Red
        self.lowRed(0, 'y')
        # LOW yellow for target green led
        self.lowLED(target+1)
        # LOW yellow for active green led
        self.lowLED(active+1)

    def highRed(self, delayTLS, mode):
        # Green Mode
        if mode == 'g':
            # All Traffic Lamb Index
            for tls in range(1,len(self.trafficLamb)+1):
                if self.targetTLS == tls:
                    # LOW red led pin in Target TLS for Green Led 
                    self.lowLED(tls*3+1) # TLS (which traffic lamb?) * 3 (g:1/y:2/r:3) + startPin
                else:
                    # HIGH red led pin not in Target TLS for Green Led 
                    self.highLED(tls*3+1) # TLS (which traffic lamb?) * 3 (g:1/y:2/r:3) + startPin
        # Yellow Mode
        elif mode == 'y':
            # All Traffic Lamb Index
            for tls in range(1,len(self.trafficLamb)+1):
                if (self.targetTLS == tls) or (self.targetTLS2 == tls):
                    # LOW red led pin in Active/Target TLS for Yellow Led 
                    self.lowLED(tls*3+1) # TLS (which traffic lamb?) * 3 (g:1/y:2/r:3) + startPin
                else:
                    # HIGH red led pin not in Active/Target TLS for Yellow Led 
                    self.highLED(tls*3+1) # TLS (which traffic lamb?) * 3 (g:1/y:2/r:3) + startPin

    def lowRed(self, delayTLS, mode):
        if (mode == 'g'):
            for tls in range(1,len(self.trafficLamb)+1):
                if(self.activeTLS == tls):
                    self.highLED(tls*3+1)
                else:
                    self.lowLED(tls*3+1)
        elif (mode == 'y'):
            for tls in range(1,len(self.trafficLamb)+1):
                if(self.targetTLS2 == tls):
                    self.lowLED(tls*3+1)
                else:
                    self.highLED(tls*3+1)

    def startSystem(self, greenP, redP, trafficL):
        self.highLED(greenP)
        for pin in range(redP + 3, 13):
            self.highLED(pin)
            pin += trafficL
        self.delay(5000)

    # return activeTLSPin
    def activeTLSPin(self, pin, trafficL):
        for p in range(pin, 13):
            if (self.isPinHigh(p)):
                return (int)((p / 2) + 1)
            p += trafficL
        return 1

    # return targetPin
    def TargetPin(self, pin, target):
        return (pin + ((target - 1) * 3))


try:
    while True:
        pass 
except KeyboardInterrupt:
    # Program? sonland?rmak i�in Ctrl+C'ye bas?ld???nda GPIO ayarlar?n? temizleyin
    GPIO.cleanup()
