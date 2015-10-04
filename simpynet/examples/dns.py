# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 10:29:00 2014

@author: Artem
"""
import simpynet

SERVER_PORT = 150
CLIENT_PORT = 110
PROPAGATION_DELAY = 0.1
PROCESSING_DELAY = 0.2

class dns_packet():
    def __init__( self , src_ip , server_name , ip_addr = None ):
        self.src_ip = src_ip
        self.server_name = server_name
        self.ip_addr = ip_addr

    def __len__(self):
        return 64+len(self.server_name)


class packet():
    def __init__( self , src_ip , src_port , data ):
        self.src_ip = src_ip
        self.src_port = src_port
        self.data = data

    def __len__(self):
        return 40+len(self.data)


class Client( ):


    def __init__( self , env , host , dns_ip ):

        self.env = env
        self.host = host
        self.port = CLIENT_PORT
        self.ip_adresses = {}
        self.send_queue = {}
        self.dns_ip = dns_ip

        self.udp=simpynet.UDP_Protocol( env )

        self.udp.add_handler( self.host.add_transport_handler( self.udp.get_handler() )  )
        self.udp_handler = self.udp.add_application_handler( self._receive , self.port )


    def _receive( self , data ):
        if isinstance(data , dns_packet):
            if data.ip_addr is not None:
                self.ip_adresses[data.server_name] = data.ip_addr
                print str(self.env.now)+": Received answer from dns. "+ data.server_name + ": " + str(data.ip_addr)
                if self.send_queue.has_key( data.server_name ):
                    while len(self.send_queue[data.server_name])>0:
                        self.send( self.send_queue[data.server_name].pop(0) , data.server_name )
            else:
                print str(self.env.now) + ": Not found for: " + data.server_name

        else:
            print str(self.env.now) + ": "+ data.data


    def send( self , message , dst_server ):
        if self.ip_adresses.has_key(dst_server):
            self.udp_handler( packet( self.host.ip_addr , self.port , message ) , self.port , SERVER_PORT , self.ip_adresses[dst_server] )
        else:
            self._request_ip_address( dst_server )
            if not( self.send_queue.has_key( dst_server ) ):
                self.send_queue[dst_server] = []
            self.send_queue[dst_server].append( message )

    def _request_ip_address( self , server ):
        self.udp_handler( dns_packet( self.host.ip_addr , server ) , self.port , 53 , self.dns_ip )



class DNS_Server( ):


    def __init__( self , env , host , dns_function ):

        self.env = env
        self.host = host
        self.port = 53
        self.dns_function = dns_function

        self.udp=simpynet.UDP_Protocol( env )

        self.udp.add_handler( self.host.add_transport_handler( self.udp.get_handler() )  )
        self.udp_handler = self.udp.add_application_handler( self._receive , self.port )


    def _receive( self , data ):
        if isinstance(data , dns_packet):
            self.udp_handler( dns_packet( self.host.ip_addr , data.server_name , self.dns_function( data.server_name ) ) , self.port , CLIENT_PORT , data.src_ip )



class Server( ):


    def __init__( self , env , host , name ):

        self.env = env
        self.host = host
        self.port = SERVER_PORT
        self.name = name

        self.udp=simpynet.UDP_Protocol( env )

        self.udp.add_handler( self.host.add_transport_handler( self.udp.get_handler() )  )
        self.udp_handler = self.udp.add_application_handler( self._receive , self.port )


    def _receive( self , data ):
        self.udp_handler( packet(self.host.ip_addr , self.port,  "This is a reply from "+self.name+" to the message: "+data.data) , self.port , data.src_port , data.src_ip )

def network(env):

    domains = {"moogle.com": simpynet.IP("192.0.0.50"), "mybank.com": simpynet.IP("192.0.0.80")}

    def dns_function( name ):
        if domains.has_key(name):
            return domains[name]
        else:
            return None

    def sender(env):
        client.send( "Hello" , "moogle.com" )
        yield env.timeout(5)
        client.send( "Hello" , "mybank.com" )
        yield env.timeout(5)
        client.send( "Hello" , "random.com" )
        client.send( "Hello again" , "moogle.com" )

    def forwarding( datagram , router ):
        if datagram.dst_ip == simpynet.IP("192.0.0.0"): return simpynet.Mac("00.00.00.00.00")
        if datagram.dst_ip == simpynet.IP("192.0.0.1"): return simpynet.Mac("00.00.00.00.01")
        if datagram.dst_ip == simpynet.IP("192.0.0.50"): return simpynet.Mac("00.00.00.00.02")
        if datagram.dst_ip == simpynet.IP("192.0.0.80"): return simpynet.Mac("00.00.00.00.03")
        else: return None


    router = simpynet.Router( env, simpynet.Mac("00.00.00.00.10") , forwarding , lambda x, y : PROCESSING_DELAY )
    host = simpynet.Host(env , simpynet.Mac("00.00.00.00.00") , simpynet.IP("192.0.0.0"))
    dns_host = simpynet.Host(env , simpynet.Mac("00.00.00.00.01") , simpynet.IP("192.0.0.1"))
    server_host0 = simpynet.Host(env , simpynet.Mac("00.00.00.00.02") , simpynet.IP("192.0.0.50"))
    server_host1 = simpynet.Host(env , simpynet.Mac("00.00.00.00.03") , simpynet.IP("192.0.0.80"))

    host.set_default_gateway(simpynet.Mac("00.00.00.00.10"))
    dns_host.set_default_gateway(simpynet.Mac("00.00.00.00.10"))
    server_host0.set_default_gateway(simpynet.Mac("00.00.00.00.10"))
    server_host1.set_default_gateway(simpynet.Mac("00.00.00.00.10"))

    client = Client( env , host , dns_host.ip_addr )
    dns = DNS_Server( env , dns_host , dns_function )
    moogle = Server( env , server_host0 , "moogle.com" )
    mybank = Server( env , server_host1 , "mybank.com" )

    link0 = simpynet.PointToPoint(env, lambda x,y: PROPAGATION_DELAY, lambda src,trg,l: PROPAGATION_DELAY )
    link1 = simpynet.PointToPoint(env, lambda x,y: PROPAGATION_DELAY, lambda src,trg,l: PROPAGATION_DELAY )
    link2 = simpynet.PointToPoint(env, lambda x,y: PROPAGATION_DELAY, lambda src,trg,l: PROPAGATION_DELAY )
    link3 = simpynet.PointToPoint(env, lambda x,y: PROPAGATION_DELAY, lambda src,trg,l: PROPAGATION_DELAY )



    simpynet.physical.plug(link0,host)
    simpynet.physical.plug(link0,router)
    simpynet.physical.plug(link1,dns_host)
    simpynet.physical.plug(link1,router)
    simpynet.physical.plug(link2,server_host0)
    simpynet.physical.plug(link2,router)
    simpynet.physical.plug(link3,server_host1)
    simpynet.physical.plug(link3,router)

    env.process(sender(env))

def run_example():
    e = simpynet.Environment()
    e.add_network(network)
    e.run( )
