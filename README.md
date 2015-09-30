

# SymPyNet 
### A simulator for any level mechanism in the TCP/IP model.
===========================================================

Description of the project
--------------------------

SimPyNet is a composition of three words that characterise the project

1. Simulator
2. Python
3. Network

`simpynet` is a framework totally written in `Python`,it is able to simulate the mechanism at any level of the TCP/IP model in a network ( physical, link,network,transport,application).

The simulation is done by  the model DES (Discrete-Event-Simulation).
The simulator doesn't provide a GUI (such different simulator of networks as GNS3,OMNeT++).

`simpynet` provides a `logging` mechanism  and collectors that collects data during the execution of a simulation in order to realize `statistical`  analysis.

`simpynet` was born  as support theaching software for the course of Computer Network at university of Florence.

# Requirements
--------------------------
* Python 2.7
* [simpy](http://simpy.readthedocs.org/en/latest/simpy_intro/installation.html)


# Install in a virtual environment
---------------------------------

1. [Download the  archive of the latest release X.Y](https://github.com/dido18/spn/releases)
2. Unack the archive name `simpynet-X.Y.tar.gz` (or `zip`) and will unpack into a directory `simpynet-x.y`
3. Create a virtualenv and activate it with the command ``` source /path_to_venv/bin/activate ```
4. run the command ```python setup.py install ```


# Write the first simulation
--------------------------
This program simulate a DHCP clinet and DHCP server interaction
```
import simpynet as spn


def DHCP( env ):

    """
    |dhcp_client|------link 1------ |dhcp_server|
    """
    # creates the two Host: client and server with their own MAC and IP address
    c_host = spn.Host( env, spn.Mac('aa.aa.aa.aa.aa.aa'),  spn.IP('0.0.0.0') )
    s_host = spn.Host( env, spn.Mac('bb.bb.bb.bb.bb.bb'),  spn.IP('192.168.1.1') )
    
    # create a Link1 with propagation delay and trasmission delay one
    l1 = spn.Link(env, lambda x,y: 1 , lambda src,trg,l: 1)
    
    #plugs the link to the host server and the host client
    spn.physical.plug( l1 , c_host )
    spn.physical.plug( l1 , s_host )

    # wrap the general HOst in the DHCP client and server
    client=spn.DHCP_client( env , c_host )
    server=spn.DHCP_server( env , s_host )

    # function exeuted by the client to choose the DHVP server
    def choose_ip_server( lista_ip):
        if len(lista_ip) > 0:
            return lista_ip.pop(0)
        else: return None
    
    #function executed by the server whe it must choose an IP address for the client
    def choose_ip_for_client():
        return '123'

    server.add_function_choose( choose_ip_for_client)
    client.add_function_choose( choose_ip_server)

    def funct():
        yield env.timeout(1)
        client.send_DHCP_DISCOVERED()

    env.process( funct())
```

