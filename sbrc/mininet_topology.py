#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, UserSwitch
from mininet.cli import CLI
from mininet.link import Intf, TCULink
from mininet.log import setLogLevel, info
from mininet.topo import Topo

class Project(Topo):
    def __init__(self):
        Topo.__init__(self)

        # hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        # switches
        s1 = self.addSwitch('s1')
        #Intf('eth2', node=s1)

        # links
        self.addLink(h1, s1, cls=TCULink)
        self.addLink(h2, s1, cls=TCULink)
        self.addLink(h3, s1, cls=TCULink)



if __name__ == '__main__':
    setLogLevel('info')
    topo = Project()
    net = Mininet(
        topo=topo,
        controller=lambda name: RemoteController(name, ip='192.168.0.16'),
        switch=UserSwitch,
        autoSetMacs=True,
    )
    net.start()
    try:
        print("variando...")
        server = net.getNodeByName('h2')
        server.cmdPrint("ifconfig enp0s3:2 192.168.0.30")
    except Exception as e:
        print("Houve um erro, stopando...", str(e))
        net.stop()
    CLI(net)
    net.stop()

# Allows the file to be imported using `mn --custom <filename> --topo minimal`
topos = {
    'mytopo': Project
}

