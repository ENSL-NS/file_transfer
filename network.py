'''
This is a simple network class that can be used to create a network of nodes.
'''

from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.node import OVSController

class SimpleTopo(Topo):
    "Simple topology for content transfer."

    def __init__(self, bw_host=1000, bw_net=1000, delay="10ms"):
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

def get_network(bw=1000, delay="10ms"):
  topo = SimpleTopo(bw_host=bw, bw_net=bw, delay=delay)
  net = Mininet(topo=topo, controller=OVSController, link=TCLink)
  return net
  
def start_network(net):
  net.start()
  return
  
def stop_network(net):
  net.stop()
  return

def start_client(net, client_cmd):
  h1 = net.getNodeByName('h1')
  print("Starting client")
  h1.popen(client_cmd)
  
def start_server(net, server_cmd):
  h2 = net.getNodeByName('h2')
  print("Starting server")
  h2.popen(server_cmd)
  
def stop_client(net, cmd):
  h1 = net.getNodeByName('h1')
  h1.cmd('kill %{}'.format(cmd))
  
def stop_server(net, cmd):
  h2 = net.getNodeByName('h2')
  h2.cmd('kill %{}'.format(cmd))
  
def start_server(net, server_cmd):
  h2 = net.getNodeByName('h2')
  print("Starting server")
  h2.popen(server_cmd)
  
def test_ping(net):
    # Hint: Use host.popen(cmd, shell=True).  If you pass shell=True
    # to popen, you can redirect cmd's output using shell syntax.
    # i.e. ping ... > /path/to/ping.
    print("Starting to ping...")
    h1 = net.getNodeByName('h1')
    h2 = net.getNodeByName('h2')
    #Getting host2 IP
    serverIP = h2.IP()
    output = h1.cmd("ping " + serverIP + " -i 0.1 -c 10")
    return output 
  
def test_iperf(net):
    # Hint: Use host.popen(cmd, shell=True).  If you pass shell=True
    # to popen, you can redirect cmd's output using shell syntax.
    # i.e. ping ... > /path/to/ping.
    print("Starting to ping...")
    h1 = net.getNodeByName('h1')
    h2 = net.getNodeByName('h2')
    # Start iperf serer
    h2.popen("iperf -s")
    # Getting host2 IP
    serverIP = h2.IP()
    output = h1.cmd("iperf -c " + serverIP)
    return output 