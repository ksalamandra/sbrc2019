import models
from models import settings
import psutil
import time
import numpy as np

if __name__ == "__main__":
    if input("The current data will be destroyed, is this ok?") == "y":
        cpus = []
        t = 0
        dc = models.DC(cap=settings.MAX_SERVER_LOAD)
        clients = list()
        clients.append(models.Client(2, settings.CLIENT1_BW, dc))
        clients.append(models.Client(3, settings.CLIENT2_BW, dc))
        clients.append(models.Client(4, settings.CLIENT3_BW, dc))
        rp = models.RewardProvider('192.168.0.22', clients, dc)
        try:
            while 1:
                print("T =", t, " ------------------------------------------------------------------")
                cpus.append(psutil.cpu_percent())
                print("CPU=", np.mean(cpus))
                time.sleep(settings.STEP)
                rp.step()
                t += 1
                print(cpus)
        except:
            print(cpus)
