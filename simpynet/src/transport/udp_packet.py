# -*- coding: utf-8 -*-
"""
This module contains the UDP Packet at transport layer.
"""

class UDP_Packet():
    """
    UDP Packet
    """
    def __init__( self , src_port , dst_port , message ):
        self.src_port=src_port
        self.dst_port=dst_port
        self.message=message
        self.size=len(message)+64
        self.length = len(message)

    def __str__(self):
        s='Source: '+repr(self.src_port)+' Destination: '+repr(self.dst_port)
        return s

    def __len__(self):
        return self.size

    def __repr__(self):
        s='Source: '+str(self.src_port)+' Destination: '+str(self.dst_port)
        return s
