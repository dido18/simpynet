# -*- coding: utf-8 -*-
"""
This module contains the frame at link layer
"""

class Frame():
    """
    Frame at link layer
    """
    def __init__(self,src_mac,dst_mac,datagram, CRC=None, tpe=None):
        self.src_mac=src_mac
        self.dst_mac=dst_mac
        self.datagram=datagram
        self.size=len(datagram)+26


    def __str__(self):
        s='Source: '+repr(self.src_mac)+' Destination: '+repr(self.dst_mac)
        return s

    def __len__(self):
        return self.size

    def __repr__(self):
        s='Source: '+repr(self.src_mac)+' Destination: '+repr(self.dst_mac)
        return s
