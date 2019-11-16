#!/usr/bin/python2

#
# Minimal example showing how to use MaxiNet
#

import time

from MaxiNet.Frontend import maxinet
#from MaxiNet.tools import FatTree
from mininet.topo import Topo, SingleSwitchTopo
from mininet.node import UserSwitch, OVSSwitch
from mininet.link import TCULink
import random

class DC(Topo):

    def __init__(self, **opts):
        Topo.__init__(self, **opts)

    def build(self):
        h1 = self.addHost('h1', ip="10.0.0.1")
        h2 = self.addHost('h2', ip="10.0.0.2")
        s1 = self.addSwitch('s1', dpid='1')
        h1s1 = self.addLink(h1, s1, cls=TCULink)
        h2s1 = self.addLink(h2, s1, cls=TCULink)


topo = DC()
print "Done Topo"
cluster = maxinet.Cluster()
print "Done Cluster"

exp = maxinet.Experiment(cluster, DC(), switch=UserSwitch)
exp.setup()

print "set up done"

print "waiting 5 seconds for routing algorithms on the controller to converge"
time.sleep(5)

exp.CLI(locals(), globals())
exp.stop()



#print exp.get_node("h1").cmd("ifconfig")  # call mininet cmd function of h1
#print exp.get_node("h4").cmd("ifconfig")
#print exp.get_node("h1").cmd("ping -c 5 10.0.0.4")
