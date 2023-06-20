#!/usr/bin/python

from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.node import RemoteController

REMOTE_CONTROLLER_IP = "127.0.0.1"


class SimpleTopo(Topo):
    "<l> switches, each has <hpl> hosted s-s-s-s-s"

    def __init__(self):
        # Initialize topology
        Topo.__init__(self)
        switches = []
        hosts = []
        l = 5
        hpl = 4
        # Switches
        for i in range(l):
            nm = "S{}".format(i + 1)
            switches.append(self.addSwitch(nm))

        # Hosts
        for i in range(l * hpl):
            nm = "H{}".format(i + 1)
            hosts.append(self.addHost(nm))

        # Links
        for s in range(l - 1):
            self.addLink(switches[s], switches[s + 1])

        s = 0
        for host in range(l * hpl):
            self.addLink(switches[s], hosts[host])
            if ((host + 1) % hpl) == 0:
                s += 1

class SpineLeaf ( Topo ):
    "Spine Leaf Topology S2 L4 H4/L"

    def __init__(self):
        #Initialize topology
        Topo.__init__(self)
        switchesSpine=[]
        switchesLeaf=[]
        hosts=[]
        s = 2
        l = 4
        hpl = 4
        #Switches
        for i in range (s):
            nm="SS{}".format(i+1)
            switchesSpine.append(self.addSwitch(nm))

        for i in range (l):
            nm = "SL{}".format(i + 1)
            switchesLeaf.append(self.addSwitch(nm))

        #Hosts
        for i in range (l*hpl):
            nm = "H{}".format(i + 1)
            hosts.append(self.addHost(nm))

        #Links
        for leaf in range(l):
            for spine in range(s):
                self.addLink(switchesSpine[spine], switchesLeaf[leaf])

        leaf = 0
        for host in range (l*hpl):
            self.addLink(switchesLeaf[leaf], hosts[host])
            if ((host+1)%hpl)==0:
                leaf+=1


topos = {'simpletopo': (lambda: SimpleTopo()), 'spineleaf': (lambda: SpineLeaf())}

if __name__ == '__main__':
    setLogLevel('info')
    topo=SimpleTopo()
    net = Mininet(topo=topo)
    #net = Mininet(topo=topo, controller=None, autoStaticArp=True)
    # net.addController("c0", controller=RemoteController, ip=REMOTE_CONTROLLER_IP)
    net.start()
    CLI(net)
    net.stop()
