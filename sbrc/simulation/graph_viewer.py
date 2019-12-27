from matplotlib import pyplot as plt
import matplotlib
import time
import numpy as np
from models import settings

#f = open(settings.MAIN_FILE, "r")
f = open("general_first_result.txt", "r")

server_load = 100000
b = f.read().replace("\x00", "")
f.close()

y = []
m = []
k = []
z = []
L = []
for line in b.splitlines()[1::]:
    #if float(line.split(',')[0]):
    if line != "0,0,0" and line:
        #if float(line.split(',')[0]) and float(line.split(',')[1]) and float(line.split(',')[2]):
        k.append(float(line.split(',')[0]))
        y.append(float(line.split(',')[1]))
        #z.append(float(line.split(',')[2]))
        #L.append(float(line.split(',')[3]))
        m.append(server_load)
x = range(len(y))
font = {'family' : 'DejaVu Sans',
        #'weight' : 'bold',
        'size'   : 30}
matplotlib.rc('font', **font)
matplotlib.use('Agg')

wd = 3

print(np.mean(k)/50000)
print(np.mean(y)/500000)
##print(np.mean(z)/150000)
#print(np.mean(L))
scale = 0.4
plt.figure(figsize=(scale*50,scale*30), dpi=100)

plt.plot(x, np.asarray(k)/1000, 'b-',label="L", linewidth=wd)
plt.plot(x, np.asarray(y)/1000, 'r-.', label="M", linewidth=wd, markersize=20, markeredgewidth=4)
#plt.plot(x, np.asarray(z)/1000, 'r', label="Cliente 3", linewidth=wd)
plt.plot(x, np.asarray(m)/1000, 'k', label="Limite de banda médio L_c", linestyle='dotted', linewidth=wd)
#
#plt.plot(x, L, 'orange', label="L", linewidth=wd)
#plt.plot(x, L, 'k', label="L", linewidth=wd)
#plt.plot(x, z, label="Reward")
legend = plt.legend()
for line in legend.get_lines():
    line.set_linewidth(4)
#plt.title(f"media-reward={np.mean(z)}")
#plt.grid(True)
plt.xlabel("Tempo (s)")
plt.ylabel("Tráfego na Nuvem (kb/s)")

#plt.show()
plt.savefig('result1.pdf')


#plt.savefig(f'{time.time()}.png')
