import os
import random
import numpy as np
import time

while 1:
    speed = random.randint(1, 200)
    #speed = np.random.poisson(8000, 20)
    elapsed = random.randrange(1,3,1)
    for i in range(elapsed):
        st = f"iperf -c 10.0.0.1 -u -b {speed}k -t {1}"
        print(st)
        process = os.popen(st)
        preprocessed = process.read()
        process.close()
        print(preprocessed)
        time.sleep(elapsed)
        print("-----------------------", speed)
