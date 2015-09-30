# -*- coding: utf-8 -*-
"""
This module simulates the Network Interface Card at link layer.
"""
import simpynet
from frame import Frame
from mac import Mac
import logging

class NIC():
    """
    Simulates a Network Interface Card at the link layer.\n
    *environment* is the class which simulates the passing of time provided by
    ``simpy``.
    *mac_addr* is the MAC Address associated to the NIC \n
    """
    def __init__(self,
                 environment,
                 mac_addr
                 ):
        self.mac_addr=mac_addr
        self.corrupted_frames = 0
        self.host_handler = None
        self.output_handler = None

        self.env = environment

        self.resource = simpynet.simpy.Resource( self.env , 1 )

        self.lgr = logging.getLogger(simpynet.__LOGNAME__)

        self.discarded_frames = 0
        self.sent_frames = 0
        self.received_frames = 0



    def add_handler(self, name , handler):
        """
        N.add_handler(handler) - add handler to NIC
        """
        self.output_handler=handler # dimensione della coda
        return self.get_handler()


    def get_handler( self ):
        """
        N.get_handler() - get NIC's handler
        """
        def _new_handler( name, data, d_trm_delay = 0.0):
            return self.env.process(self._receive(name, data, d_trm_delay ))

        return _new_handler


    def add_host_handler( self, host_handler ):
        """
        N.add_host_handler(handler) - add host handler to NIC
        """
        def _new_handler( data , mac ):
            return self.env.process(self._send( data , mac ))
        self.host_handler = host_handler

        return _new_handler



    def _receive( self , name , data , d_trm_delay ):
        """
        Handles the frame and sends the processed data to the host.
        """
        yield self.env.timeout ( d_trm_delay )
        self.received_frames += 1

        if (hasattr(data, "dst_mac") and hasattr(data, "datagram")):
            if self.mac_addr == data.dst_mac or data.dst_mac == Mac() :
                self.lgr.log( simpynet.__LINK_LOG_N__ , "   " + str(float(self.env.now)) + "   " + repr(self.mac_addr) + ' :  Received from: ' + repr(data.src_mac) )
                self.host_handler( data.datagram )
            else:
                self.discarded_frames += 1
                self.lgr.log( simpynet.__LINK_LOG_N__ , "   " + str(float(self.env.now)) + "   " + repr(self.mac_addr) + ' :  Discarded from: ' + repr(data.src_mac) )

        else:
            self.corrupted_frames += 1


    def _send( self , data , mac = Mac()):
        """
        Handles the data and sends the processed frame to the host.
        """
        f = Frame( self.mac_addr , mac , data ) #mac in broadcast
        with self.resource.request() as req:
            yield req
            yield self.output_handler( repr(self) , f )
            self.lgr.log( simpynet.__LINK_LOG_N__ , "   " + str(float(self.env.now)) + "   " + repr(self.mac_addr) + ' :  Sent to: ' + repr(mac) )

            self.sent_frames += 1


    def collector_discardedframes( self ):
        """
        collector_discardedframes() - returns number of discarded frames
        """
        return self.discarded_frames


    def collector_sentframes(self ):
        """
        collector_sentframes() - returns number of sent frames
        """
        return self.sent_frames


    def collector_receivedframes( self ):
        """
        collector_receivedframes() - returns number of received frames
        """
        return self.received_frames


    def __repr__(self):
        """
        repr( NIC ) - NIC's unique name identified by its MAC address
        """
        return repr(self.mac_addr)
