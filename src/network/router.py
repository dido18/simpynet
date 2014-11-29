# -*- coding: utf-8 -*-
"""
This module simulates the Router at network layer.
"""
import SimPyNet
import logging



class Router(SimPyNet.link.switch.Switch):
    """
    Simulates a Router at the network layer.\n
    *environment* is the class which simulates the passing of time provided by
    ``simpy``.
    *mac* is the MAC Address associated to the Router.
    *forwarding* is the functions that forwards the datagrams (receives as 
    parameters the datagram and the Mac Address and returns the destination Mac
    Address).
    Processing delay (*prcss_delay*) is set to 0 unless specified and queue 
    size (*queue_size*) is infinite unless specified.
        
    \n
    """
    def __init__(self, 
                 environment, 
                 mac,
                 forwarding,
                 prcss_delay=lambda x, y: 0.0,
                 queue_size=float('inf')
                 ):
        
        self.lgr = logging.getLogger(SimPyNet.__LOGNAME__)
   
        self.env = environment
        self.mac = mac
        self.forwarding = forwarding
        self.prcss_delay = prcss_delay
        self.queue_size = queue_size
        self.arp_table = {}
        self.queues = {}
        self.handlers = {}    
        
        self.lost_datagrams = 0
        self.sent_datagrams = 0
        self.received_datagrams = 0
        self.processing_time = 0
        
        self.switch_resource = SimPyNet.simpy.Resource( self.env , 1 )
        self.output_buffer = {}
        self.prg_delay = lambda x,y:0.0
        
        
    def _add_to_queue( self , name , data , d_trm_delay ):
        """
        Adds the data to the input-buffer. If full, the datagram is lost
        """
        yield self.env.timeout( d_trm_delay )
        self.lgr.log( SimPyNet.__NETWORK_LOG_N__ , "   " + str(float(self.env.now)) + "   " + repr(self) + ' :  Received from: ' + repr(data.src_mac) )
        self.received_datagrams += 1
        if (self.queues[name][0] + len( data ) > self.queue_size):
            self.lgr.log( SimPyNet.__NETWORK_LOG_N__ , "   " + str(float(self.env.now)) + "   " + repr(self) + ' :  Lost from: ' + repr(data.src_mac) + " to " + repr(data.dst_mac) )
            self.lost_datagrams += 1
        else:
            self.queues[name][0] +=  len(data)
            self.env.process( self._forwarding( name, data, d_trm_delay) )
        
        
    def _forwarding( self , name , data , d_trm_delay ):
        """
        Simulates the forwarding process. 
        The data is processed and put to the appropriate output buffer.
        """
        with self.switch_resource.request() as req:
                yield req
                temp_time = float(self.env.now)
                yield self.env.timeout( self.prcss_delay( data, repr( self ) ) )                
                src_mac = repr(data.src_mac)
                for mac in self.arp_table:
                    if self.arp_table[mac] == name:
                        del self.arp_table[mac]
                        break
                self.arp_table[repr(src_mac)] = name # si aggiunge all'arp table il riferimento mac-interface
                
                self.queues[name][0] -= len(data)
                if ( (data.dst_mac == self.mac or data.dst_mac == SimPyNet.Mac()) and data.datagram.ttl>0):
                    datagram = data.datagram
                    datagram.ttl -= 1
                    dst_mac = self.forwarding( datagram , repr( self ) ) 
                    data = SimPyNet.Frame( self.mac , dst_mac , datagram )
                    if self.arp_table.has_key(repr(dst_mac)):
                        self.env.process ( self._deliver( self.arp_table[repr(dst_mac)] , data , d_trm_delay ) )
                    else:
                        self.env.process( self._broadcast( name , data , d_trm_delay ) )
                    self.processing_time += float(self.env.now) - temp_time
                    
                    
    def _deliver( self , name , data , d_trm_delay ):
        """
        Simulates the transmission from the output-buffer on the appropriate port.
        """
        if (self.queues[name][1] + len( data ) > self.queue_size):
            self.lost_datagrams += 1
            self.lgr.log( SimPyNet.__NETWORK_LOG_N__ , "   " + str(float(self.env.now)) + "   " + repr(self) + ' :  Lost from: ' + repr(data.src_mac) + " to " + repr(data.dst_mac) )
        else:
            self.queues[name][1] +=  len(data)
            with self.output_buffer[name].request() as req:
                yield req
                yield self.env.process(SimPyNet
                                    .physical.hub.Hub
                                    ._deliver(self, name, data, d_trm_delay))
                self.lgr.log( SimPyNet.__NETWORK_LOG_N__ , "   " + str(float(self.env.now)) + "   " + repr(self) + ' :  Sent to: ' + repr(data.dst_mac) )
                self.sent_datagrams +=1
                self.queues[name][1] -=  len(data)
                
    
    def __repr__(self):
        """
        repr( Router ) - Router's unique name
        """
        return repr( self.mac )
        
        
    def collector_lostdatagrams( self ):
        """
        collector_lostdatagrams() - returns number of lost datagrams
        """
        return  self.lost_datagrams 
        
        
    def collector_sentdatagrams( self ):
        """
        collector_sentdatagrams() - returns number of sent datagrams
        """
        return self.sent_datagrams
        
        
    def collector_receiveddatagrams( self ):
        """
        collector_receiveddatagrams() - returns number of received datagrams
        """
        return self.received_datagrams
        
        
    def collector_processingtime( self ):
        """
        collector_processingtimes() - returns total processing time
        """
        return self.processing_time 
        