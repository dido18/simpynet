# -*- coding: utf-8 -*-
"""
This module contains data at network layer, Datagram.
"""

class Datagram():
    """
    Datagram at network layer
    """
    def __init__( self , src_ip , dst_ip , segment , protocol=None , ttl=float('inf') ):
        self.src_ip=src_ip
        self.dst_ip=dst_ip
        self.segment=segment
        self.protocol = protocol
        self.ttl = ttl
        self.size=len(segment)+160
    
    
    def __str__(self):
        s='Source: '+repr(self.src_ip)+' Destination: '+repr(self.dst_ip)
        return s
        
    def __len__(self):
        return self.size
        
    def __repr__(self):
        s='Source: '+repr(self.src_ip)+' Destination: '+repr(self.dst_ip)
        return s