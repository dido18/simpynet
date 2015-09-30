# -*- coding: utf-8 -*-
"""
This module simulates the host at network layer.
"""
import simpynet
from ip import IP

class Host(simpynet.link.nic.NIC):
    """
    Simulates a host at the network layer.\n
    *environment* is the class which simulates the passing of time provided by
    ``simpy``.
    *mac_addr* and *ip_addr* are the mac and ip addresses associated to the
    host \n
    """
    def __init__(self,
                 environment,
                 mac_addr,
                 ip_addr
                 ):

        simpynet.link.nic.NIC.__init__( self , environment , mac_addr)


        self.ip_addr = ip_addr
        self.host_handler = self._receive_host
        self.transport_handler = []

        self.discarded_datagrams = 0
        self.sent_datagrams = 0
        self.received_datagrams = 0
        self.corrupted_datagrams = 0

        self.default_gateway = simpynet.Mac()


    def add_transport_handler( self, transport_handler ):
        """
        H.add_transport_handler(handler) - add transport handler
        """
        def _new_handler( data , dst_ip ):
            self._send( data , dst_ip )

        self.transport_handler.append( transport_handler )

        return _new_handler


    def set_default_gateway( self , mac_gateway ):
        """
        H.set_default_gateway( mac_gateway ) - sets the mac to the default gateway
        """
        self.default_gateway = mac_gateway


    def _receive_host( self , datagram ):
        """
        Handles the frame and sends the processed data to the host.
        """
        self.received_datagrams += 1
        if (hasattr(datagram, "dst_ip") and hasattr(datagram, "segment")):
            if self.ip_addr == datagram.dst_ip or datagram.dst_ip== IP(): # or in broadcast
                self.lgr.log( simpynet.__NETWORK_LOG_N__ , "   " + str(float(self.env.now)) + "   " + repr(self.ip_addr) + ' :  Received from: ' + repr(datagram.src_ip) )
                for h in self.transport_handler:
                    h( datagram.segment )
            else:
                self.lgr.log( simpynet.__NETWORK_LOG_N__ , "   " + str(float(self.env.now)) + "   " + repr(self.ip_addr) + ' :  Discarded from: ' + repr(datagram.src_ip) )
                self.discarded_datagrams += 1
        else:
            self.corrupted_datagrams += 1




    def _send( self , message , dst_ip ):
        """
        Handles the data and sends the processed frame to the host.
        """
        d = simpynet.Datagram( self.ip_addr , dst_ip , message )
        self.env.process(simpynet.link.nic.NIC._send( self , d , self.default_gateway ))
        self.sent_datagrams += 1
        self.lgr.log( simpynet.__NETWORK_LOG_N__ , "   " + str(float(self.env.now)) + "   " + repr(self.ip_addr) + ' :  Sent to: ' + repr(dst_ip) )



    def __repr__(self):
        """
        repr( Host ) - Host's unique name identified by its IP address
        """
        return repr(self.ip_addr)


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


    def collector_discarded_datagrams( self ):
        """
        collector_discarded_datagrams() - returns number of discarded datagrams
        """
        return self.discarded_datagrams


    def collector_corrupted_datagrams( self ):
        """
        collector_corrupted_datagrams() - returns number of corrupted datagrams
        """
        return self.corrupted_datagrams
