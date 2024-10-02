'''
This is a simple network class that can be used to create a network of nodes.
'''

from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet

class SimpleTopo(Topo):
    "Simple topology for content transfer."

    def __init__(self, bw_host=1000, bw_net=1000, delay=10):
      super(SimpleTopo, self).__init__()

      # Creating the two hosts
      h1 = self.addHost('h1')
      h2 = self.addHost('h2')

      # Here I have created a switch.  If you change its name, its
      # interface names will change from s0-eth1 to newname-eth1.
      s0 = self.addSwitch('s0')

      # Adding link between h1 and s0 using parsed arguments
      self.addLink(h1, s0, bw=bw_host, delay=delay)
      # Adding link between s0 and h2 using parsed arguments
      self.addLink(h2, s0, bw=bw_net, delay=delay)

      return

def get_network(bw=1000, delay=10):
  topo = SimpleTopo(bw_host=bw, bw_net=bw, delay=delay/2)
  net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
  return net
  
def start_network(net):
  net.start()
  return
  
def stop_network(net):
  net.stop()
  return