import serial
import time

class ARDUINO:
    def __init__(self, tls):
        self.port = serial.Serial("COM6", 9600)
        self.tls = tls

    def control(self, CAM):
        self.cam = CAM

    def sendInput(self, data):
        self.port.write(str(data).encode()) 
    
    def targetTLS(self, data):
        self.sendInput(data)
    
    def delayTLS(self, data):
        self.sendInput(data)

    def tlsData(self):
        self.sendInput(self.tls)
    
    def readData(self):
        self.port.readline().decode('utf-8').strip()

tlsList = [3,2,1,3,2,1,2,3,2,1,3,1]
# tlsList = [1,2,1,2,1]

# tls num
x = ARDUINO(3)
# data = input("target TLS (1,2,3): ")
data = 2
for i in tlsList:
    # data2 = input("target 2 TLS (1,2,3): ")
    data2 = i
    # trafik lamb
    x.tlsData()
    x.targetTLS(data)
    x.targetTLS(data2)
    # second
    x.delayTLS("3")
    time.sleep(3)
    data = data2
