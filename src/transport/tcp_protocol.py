# -*- coding: utf-8 -*-
"""
Created on Thu May 29 17:30:41 2014

@author: unkown
"""

import tcp_packet

class TCP_Protocol():
    def __init__(self, 
                 environment
                 ):        
        self.application_handlers = {}
        self.dst = {}
        self.host_handler = None
        self.sent_packets = 0
        self.received_packets = 0
        self.corrupted_packets = 0
        self.data_queue={}
        self.MSS = 11680
        
        
    def add_handler(self, name , handler):
        """
        N.add_handler(handler) - add handler to NIC
        """
        self.host_handler=handler # dimensione della coda
        return self.get_handler()
        
        
    def get_handler( self ):
        """
        N.get_handler() - get NIC's handler
        """
        return self._receive
        
        
    def add_application_handler( self, app_handler , src_port ):
        """
        N.add_host_handler(handler) - add host handler to NIC
        """
        def _new_handler( data , src_port ):
            self._send( data , src_port )
        try:
            if self.application_handlers.has_key(src_port):
                raise Exception("Port already assigned to another process")
            else:
                self.application_handlers[src_port] = ( app_handler )
        except Exception as e:
            print e
        
        return _new_handler
        
        
    def establish_connection( self , src_port , dst_port , ip_addr ):
        self.dst[src_port] = (dst_port , ip_addr)
        self.cwindow_seq_ack[src_port] = self.MSS , 0 , 0
        #syn ecc.
        
        
    def _receive( self , packet ):
        """
        Handles the frame and sends the processed data to the host.
        """
        self.received_packets += 1
        if (hasattr(packet, "port") and hasattr(packet, "message")):
            self.application_handlers[packet.port]( packet.message )
        else:
            self.corrupted_packets += 1
            
            
    def _send( self , data , src_port ):
        """
        Handles the data and sends the processed frame to the host.
        """
        self.data_queue[src_port].append(data)
        
        
        
        
        
        p = tcp_packet.UDP_Packet( src_port , dst_port , data )
        self.host_handler( self , p , ip_addr )
        self.sent_packets += 1