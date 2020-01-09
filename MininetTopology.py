#!/usr/bin/python

"""
Topology:

  host -- SWITCH -- host
            |
            |
           host

"""

from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def emptyNet():

    "Create an empty network and add nodes to it."

    net = Mininet( controller=Controller )

    info( '*** Adding controller\n' )
    net.addController( 'c0' )

    info( '*** Adding hosts\n' )
    h1 = net.addHost( 'h1', ip='10.0.0.1' )     # server
    h2 = net.addHost( 'h2', ip='10.0.0.2' )     # renderer
    h3 = net.addHost( 'h3', ip='10.0.0.3' )     # controller

    info( '*** Adding switch\n' )
    s4 = net.addSwitch( 's4' )

    info( '*** Creating links\n' )
    net.addLink( h1, s4 )
    net.addLink( h2, s4 )
    net.addLink( h3, s4)

    info( '*** Starting network\n')
    net.start()

    info( '*** Running CLI\n' )
    CLI( net )

    info( '*** Stopping network' )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    emptyNet()
