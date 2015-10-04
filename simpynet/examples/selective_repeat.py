# -*- coding: utf-8 -*-
"""
Created on Sat Jun 21 15:30:22 2014

@author: Artem
"""
NUMBER_OF_PACKETS = 50
PROPAGATION_DELAY = 0.1
LOSS_PROBABILITY=0.1
TIMEOUT_TIME = 1.3

import simpynet

class Selective_Repeat_Packet():
    def __init__( self , number , message=simpynet.Databits(0) , ack=False ):
        self.number = number
        self.message=message
        self.ack = ack
        self.size=len(message)+16
        self.length = len(message)

    def __str__(self):
        s="Number: " + str(self.number) + " ack: " + str(self.ack)
        return s

    def __len__(self):
        return self.size

    def __repr__(self):
        s="Number: " + str(self.number) + " ack: " + str(self.ack)
        return s


class Selective_Repeat():
    def __init__(self , environment , window_size ):
        self.host_handler = None
        self.env = environment
        self.window_size = window_size
        self.window = []
        self.current = 0
        self.ip_addr = simpynet.IP()
        self.number_of_packets = 0
        self.timeout_time = TIMEOUT_TIME


    def add_handler( self , handler ):
        self.host_handler=handler
        return self.get_handler()


    def get_handler( self ):
        return self._receive


    def send( self , number_of_packets , ip_addr ):
        self.number_of_packets = number_of_packets
        self.ip_addr = ip_addr
        for i in xrange( self.window_size ):
            if i>=number_of_packets:
                break
            self.window.append({"ack": False, "timeout": self.env.process( self._timeout( i ) )})
            self._send( i )


    def _receive( self , packet ):
        if packet.ack:
            print (str(self.env.now) + ": Ricevuto ack: " + str(packet.number))
            self._ack( packet.number )
        else:
            print (str(self.env.now) + ": Ricevuto pacchetto: " + str(packet.number))
            self._send_ack( packet.number )


    def _send_ack( self , number ):
        p = Selective_Repeat_Packet( number , ack=True )
        self.host_handler(  p , self.ip_addr )


    def _ack( self , number ):
        if number >= self.current:
            if not self.window[number-self.current]["ack"]:
                self._delete_timeout( number-self.current )
            self.window[number-self.current]["ack"] = True
            while( self.window[0]["ack"] ):
                self.current += 1
                del self.window[0]
                if (self.current+self.window_size-1<self.number_of_packets):
                    self.window.append({"ack": False, "timeout": None})
                    self.window[self.window_size-1]["timeout"] = self.env.process( self._timeout( self.window_size+self.current-1 ) )
                    self._send( self.window_size+self.current-1 )
                if self.current == self.number_of_packets:
                    break


    def _timeout( self , number ):
        while( True ):
            try:
                yield self.env.timeout( self.timeout_time )
                self._send( number )
            except simpynet.simpy.Interrupt:
                return

    def _delete_timeout( self , number ):
        self.window[number]["timeout"].interrupt()


    def _send( self , number ):
        p = Selective_Repeat_Packet( number )
        self.host_handler(  p , self.ip_addr )


def sr_network(env):
    h0 = simpynet.Host(env , simpynet.Mac("00.00.00.00.00") , simpynet.IP("192.0.0.0"))
    h1 = simpynet.Host(env , simpynet.Mac("00.00.00.00.01") , simpynet.IP("192.0.0.1"))

    link = simpynet.PointToPoint(env, lambda x,y: PROPAGATION_DELAY, lambda src,trg,l: PROPAGATION_DELAY, lambda src,trg,l: LOSS_PROBABILITY)
    simpynet.physical.plug(link,h0)
    simpynet.physical.plug(link,h1)
    protocol0 = Selective_Repeat( env, 10 )
    protocol1 = Selective_Repeat( env, 10 )
    protocol0.add_handler( h0.add_transport_handler( protocol0.get_handler() ) )
    protocol1.add_handler( h1.add_transport_handler( protocol1.get_handler() ) )
    protocol0.send( NUMBER_OF_PACKETS , simpynet.IP("192.0.0.1") )


def run_example():
    e = simpynet.Environment()
    e.add_network(sr_network)
    e.run( )
