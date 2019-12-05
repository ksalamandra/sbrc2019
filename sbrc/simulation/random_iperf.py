import os
import random
import numpy as np
import time



while 1:
    speed = random.randint(1, 8000)
    #speed = np.random.poisson(8000, 20)
    elapsed = random.randrange(1,700,1)/10
    st = f"iperf -c 192.168.0.22 -u -b {speed}k -t {elapsed}"
    print(st)
    #process = os.popen(st)
    #preprocessed = process.read()
    #process.close()
    #print(preprocessed)
    time.sleep(elapsed)
    print("-----------------------", speed)
