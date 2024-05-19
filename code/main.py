import numpy as np
import time
from camPlay import CAMERA


tls = 3
camera = CAMERA()

maxCount = 0
activeCam = 0

while True:
    for cam in camera.cams:
        if maxCount <= cam["vehicle_count"]:
            activeCam = cam
        else:
            continue

