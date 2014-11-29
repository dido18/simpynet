# -*- coding: utf-8 -*-
"""
This module simulates the switch at the link layer.
"""
import SimPyNet
import logging

unique_number = 0

class Switch(SimPyNet.physical.hub.Hub):
    """
    Simulates a switch at the link layer.\n
    *environment* is the class which simulates the passing of time provided by
    ``simpy``. \n
    If not specified processing delay is set to ``0`` 
    and queue size is ``inf``.\n
    """
    def __init__(self, 
                 environment, 
                 prcss_delay= lambda x, y : 0.0,
                 queue_size='inf'
                 ):
        self.unique_number = self.__class__.unique_number
        self.__class__.unique_number = self.__class__.unique_number + 1
        
        self.lgr = logging.getLogger(SimPyNet.__LOGNAME__)                    
                     
        self.prcss_delay = prcss_delay
        self.queue_size = queue_size
        self.arp_table = {}
        self.queues = {}
        self.handlers = {}    
        
        self.lost_frames = 0
        self.sent_frames = 0
        self.received_frames = 0
        self.processing_time = 0
        
        self.env = environment
        
        self.switch_resource = SimPyNet.simpy.Resource( self.env , 1 )
        self.output_buffer = {}
        self.prg_delay = lambda x,y:0.0
        
    
    
    def add_handler(self, name , handler):
        """
        S.add_handler(handler) - add handler to switch
        """
        self.queues[name]=[0,0] # first variable input queue, second output
        self.output_buffer[name] = SimPyNet.simpy.Resource( self.env , 1 )
        SimPyNet.physical.hub.Hub.add_handler( self , name , handler)
        return self.get_handler()
        
    
    def get_handler( self ):
        """
        S.get_handler() - get switch's handler
        """
        def _new_handler(name, data, d_trm_delay = 0.0): 
            return self.env.process(self._add_to_queue(name, data, d_trm_delay ))
    
        return _new_handler
        
        
    def _add_to_queue( self , name , data , d_trm_delay ):
        """
        Adds the data to the input-buffer. If full, the frame is lost
        """
        yield self.env.timeout( d_trm_delay )
        self.lgr.log( SimPyNet.__LINK_LOG_N__ , "   " + str(float(self.env.now)) + "   " + repr(self) + ' :  Received from: ' + repr(data.src_mac) )

        self.received_frames += 1
        if (self.queues[name][0] + len( data ) > self.queue_size 
                                        or self.queue_size==0):
            self.lost_frames += 1
            self.lgr.log( SimPyNet.__LINK_LOG_N__ , "   " + str(float(self.env.now)) + "   " + repr(self) + ' :  Lost from: ' + repr(data.src_mac) + " to " + repr(data.dst_mac))

        else:
            self.queues[name][0] +=  len(data)
            self.env.process( self._switch( name, data, d_trm_delay) )
            
            
    def _switch( self , name , data , d_trm_delay ):
        """
        Simulates the switching process. 
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
                self.arp_table[src_mac] = name # si aggiunge all'arp table il riferimento mac-interface
                
                self.queues[name][0] -= len(data)
                
                dst_mac = repr(data.dst_mac)
                if self.arp_table.has_key(dst_mac):
                    self.env.process ( self._deliver( self.arp_table[dst_mac] , data , d_trm_delay ) )
                
                else:
                    self.env.process( self._broadcast( name , data , d_trm_delay ) )
                self.processing_time += float(self.env.now) - temp_time
                
                    
    def _deliver( self , name , data , d_trm_delay):
        """
        Simulates the transmission from the output-buffer on the appropriate port.
        """
        if (self.queues[name][1] + len( data ) > self.queue_size 
                                        or self.queue_size==0):
            self.lost_frames += 1
            self.lgr.log( SimPyNet.__LINK_LOG_N__ , "   " + str(float(self.env.now)) + "   " + repr(self) + ' :  Lost from: ' + repr(data.src_mac) + " to " + repr(data.dst_mac))
        else:
            self.queues[name][1] +=  len(data)
            with self.output_buffer[name].request() as req:
                yield req
                yield self.env.process(SimPyNet
                                    .physical.hub.Hub
                                    ._deliver(self, name, data, d_trm_delay))
                self.lgr.log( SimPyNet.__LINK_LOG_N__ , "   " + str(float(self.env.now)) + "   " + repr(self) + ' :  Sent to: ' + repr(data.dst_mac) )
                self.sent_frames +=1
                self.queues[name][1] -=  len(data)
                
                
    def collector_sentframes( self ):
        """
        collector_sentframes() - returns number of sent frames
        """
        return self.sent_frames
        
    
    def collector_lostframes(self ):
        """
        collector_sentframes() - returns number of lost frames
        """
        return self.lost_frames
        
            
    def collector_receivedframes( self ):
        """
        collector_receivedframes() - returns number of received frames
        """
        return self.received_frames
        
        
    def collector_processingtime( self ):
        """
        collector_processingtime() - returns total processing time
        """
        return self.processing_time
  
  
    def __repr__(self):
        """
        repr( Switch ) - Switch's unique name
        """
        return "Switch"+str(self.unique_number)
        
