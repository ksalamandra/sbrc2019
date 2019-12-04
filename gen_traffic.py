import os
import random
import numpy as np


while 1:
    #speed = random.randint(1, 30)
    speed = np.random.poisson(50, 1)
    process = os.popen(f"iperf -c 192.168.0.22 -u -b {speed}m -t 1")
    preprocessed = process.read()
    process.close()
    print(preprocessed)
    print("-----------------------", speed)
