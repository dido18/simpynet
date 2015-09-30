# -*- coding: utf-8 -*-
"""
Created on Thu May 29 17:11:08 2014

@author: unkown
"""

class TCP_Packet():

    def __init__( self , src_port , dst_port , message , seq_number , ack_number , windows_size , ack=0 ):
        self.src_port=src_port
        self.dst_port=dst_port
        self.message=message
        self.seq_number=seq_number
        self.ack_number=ack_number
        self.windows_size=windows_size
        self.ack=ack
        self.size=len(message)+160

    def __str__(self):
        s='Source: '+repr(self.src_port)+' Destination: '+repr(self.dst_port)
        return s

    def __len__(self):
        return self.size

    def __repr__(self):
        s='Source: '+repr(self.src_port)+' Destination: '+repr(self.dst_port)
        return s
