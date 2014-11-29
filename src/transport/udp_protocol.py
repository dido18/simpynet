# -*- coding: utf-8 -*-
"""
This module simulates the UDP Protocol at transport layer.

"""
import udp_packet
import SimPyNet
import logging

class UDP_Protocol():
    """
    Simulates a Network Interface Card at the link layer.\n
    *environment* is the class which simulates the passing of time provided by
    ``simpy``.
    """
    def __init__(self , environment ):        
        self.application_handlers = {}
        self.host_handler = None
        self.sent_packets = 0
        self.received_packets = 0
        self.corrupted_packets = 0
        self.env = environment 
        
        self.lgr = logging.getLogger(SimPyNet.__LOGNAME__)
        
        
    def add_handler( self , handler ):
        """
        UDP.add_handler(handler) 
        """
        self.host_handler=handler  
        return self.get_handler()
        
        
    def get_handler( self ):
        """
        UDP.get_handler() - get UDP_Protocol's handler
        """
        return self._receive
        
        
    def add_application_handler( self, app_handler , port ):
        """
        UDP.add_application_handler(handler) - add application handler to UDP_Protocol
        """
        def _new_handler( data , src_port , dst_port , ip_addr ):
            self._send( data , src_port , dst_port , ip_addr)
            
        try:
            if self.application_handlers.has_key(port):
                raise Exception("Port already assigned to another process")
            else:
                self.application_handlers[port] = ( app_handler )
        except Exception as e:
            print e
        
        return _new_handler
        
        
    def _receive( self , packet ):
        """
        Handles the frame and sends the processed data to the application.
        """
        self.received_packets += 1
        if (hasattr(packet, "dst_port") and hasattr(packet, "message")):
            self.lgr.log( SimPyNet.__TRANSPORT_LOG_N__, "   " + str(float(self.env.now)) + "   Receive, Source port : " + str(packet.src_port )+ ' : Destinantion port : ' +str( packet.dst_port))
            self.application_handlers[packet.dst_port]( packet.message )
        else:
            self.lgr.log( SimPyNet.__TRANSPORT_LOG_N__, "   " + str(float(self.env.now)) + "   Discarded From : " + str(packet.src_port) + ' To : ' + str(packet.dst_port))
            self.corrupted_packets += 1
            
            
    def _send( self , message  , src_port , dst_port , ip_addr ):
        """
        Handles the data and sends the processed frame to the host.
        """

        p = udp_packet.UDP_Packet( src_port , dst_port , message )
        self.host_handler(  p , ip_addr )
        self.lgr.log( SimPyNet.__TRANSPORT_LOG_N__, "   " + str(float(self.env.now)) + "   Send, Source port : " + str(p.src_port) + ': Destination port  : ' +str( p.dst_port)+ ' To  : '+str(ip_addr)  )
        self.sent_packets += 1