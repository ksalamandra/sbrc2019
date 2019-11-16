from mininet.topo import Topo
from mininet.util import irange


class PaperTopo(Topo):
    "Paper Topo"

    def build(self):
        # Adicionando os switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')

        # Adicionando os Hosts legitimos
        b1 = self.addHost('b1')
        b2 = self.addHost('b2')
        b3 = self.addHost('b3')

        # Adicionando os Hosts malignos
        m1 = self.addHost('m1')
        m2 = self.addHost('m2')
        m3 = self.addHost('m3')
        m4 = self.addHost('m4')

        # Adicionando os enlaces entre os switches
        self.addLink(s1, s2)
        self.addLink(s1, s5)
        self.addLink(s5, s4)
        self.addLink(s5, s3)

        # Adicionando os links entre hosts e switches
        self.addLink(s2, m1)
        self.addLink(s2, b1)
        self.addLink(s3, b2)
        self.addLink(s3, b3)
        self.addLink(s3, m2)
        self.addLink(s4, m3)
        self.addLink(s4, m4)


# Allows the file to be imported using `mn --custom <filename> --topo dcbasic`
topos = {
    'papertopo': PaperTopo
}
