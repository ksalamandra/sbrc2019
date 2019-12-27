from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib
import time
import numpy as np
from models import settings

font = {'family' : 'DejaVu Sans',
        'weight' : 'bold',
        'size'   : 15}
matplotlib.rc('font', **font)

def percent(x, pos):
    'The two args are the value and tick position'
    return f"{x}%"

proc50 =  [29.6, 27.8, 34.2, 31.7, 33.2, 32.6, 36.8, 32.6, 34.6, 30.8, 35.1, 30.6, 33.0, 31.8, 48.5, 43.6, 37.1, 56.2, 61.4, 36.1]
proc100 = [26.2, 24.6, 31.0, 32.2, 31.3, 37.8, 33.7, 34.3, 31.5, 34.1, 33.1, 34.2, 31.5, 34.5, 31.3, 32.8, 31.2, 38.3, 36.5, 35.8]
proc150 = [24.6, 28.0, 38.0, 34.7, 35.1, 47.8, 40.9, 31.4, 37.2, 36.3, 34.4, 38.0, 33.5, 38.3, 34.9, 39.6, 34.8, 34.8, 37.3, 35.0]
proc200 = [30.2, 33.2, 31.6, 32.7, 31.7, 33.4, 38.5, 37.8, 35.2, 34.1, 32.7, 37.7, 31.0, 33.1, 32.7, 36.3, 33.3, 34.5, 30.8, 32.3]



x = [50, 100, 150, 200]
y1 = [
    np.mean(proc50),
    np.mean(proc100),
    np.mean(proc150),
    np.mean(proc200),
]
y1err = [
    1.96*np.std(proc50)/np.sqrt(len(proc50)),
    1.96*np.std(proc100)/np.sqrt(len(proc100)),
    1.96*np.std(proc150)/np.sqrt(len(proc150)),
    1.96*np.std(proc200)/np.sqrt(len(proc200)),
]
y2 = [2056, 4056, 6056, 8056]
y3 = [20056, 80056, 180056, 320056]

plt.subplot(1,2,1)
plt.bar(x, y1, align='center', alpha=1, width=49)
plt.xlabel("Quantidade de estados")
plt.ylim(35, 38)
plt.xticks(x, x)
plt.grid(axis="y")
plt.ylabel("Porcentagem de processamento consumido em média [%]")
"""
plt.subplot(1,3,2)
plt.plot(x, y2)
plt.xlabel("Quantidade de estados")
plt.ylabel("Memória ocupada [B]")
plt.grid(True)

"""
plt.subplot(1,2,2)
plt.plot(x, y3,linewidth=3,)
plt.xlabel("n")
plt.ylabel("Memória ocupada [B]")
plt.grid(True)
plt.show()