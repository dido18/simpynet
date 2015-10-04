# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 13:41:53 2014

@author: Artem
"""
import selective_repeat
import simpynet
import numpy

NUMBER_OF_PACKETS = 100
PROPAGATION_DELAY = 0.1
TRANSMISSION_DELAY = 0.1
PROCESSING_DELAY = 0.2
TIME_INCREMENT = 0.01


class TimeCollector():
    def __init__(self,
                 environment,
                 ):
        self.data = {}
        self.env = environment


    def _get_handler( self , Object2 , handler ):
        def _new_handler( sender_interface, data , trm_delay = 0.0 ):
            return self.env.process( self._collect ( sender_interface , data , trm_delay , Object2 , handler) )

        return _new_handler


    def add_handlers( self , Object1 , Object2 ):
        Object1.add_handler(repr(Object2), self._get_handler(  Object2 , Object2.get_handler( ) ) )
        Object2.add_handler(repr(Object1), self._get_handler(  Object1 , Object1.get_handler( ) ) )
        self.data[repr(Object1)+repr(Object2)] = []
        self.data[repr(Object2)+repr(Object1)] = []


    def _collect( self , sender_interface , data , trm_delay , Object2 , handler ):
        yield handler( sender_interface , data , trm_delay )
        self.data[sender_interface+repr(Object2)].append( self.env.now )


    def collector( self ):
        return self.data


    def reset( self ):
        self.data = {}


def network(env):
    simpynet.PointToPoint.unique_number=0
    simpynet.Switch.unique_number=0
    h0 = simpynet.Host(env , simpynet.Mac("00.00.00.00.00") , simpynet.IP("192.0.0.0"))
    h1 = simpynet.Host(env , simpynet.Mac("00.00.00.00.01") , simpynet.IP("192.0.0.1"))

    link0 = simpynet.PointToPoint(env, lambda x,y:PROPAGATION_DELAY, lambda src,trg,l: TRANSMISSION_DELAY)
    link1 = simpynet.PointToPoint(env, lambda x,y:PROPAGATION_DELAY, lambda src,trg,l: TRANSMISSION_DELAY)

    switch = simpynet.Switch( env, lambda x, y : PROCESSING_DELAY )

    tc = TimeCollector(env)
    tc.reset()
    simpynet.physical.plug(link0,h0)
    tc.add_handlers( switch , link0 )
    tc.add_handlers( switch , link1 )
    simpynet.physical.plug(link1,h1)

    env.add_collector_functions( 'data', tc.collector , float('inf')  )

    protocol0 = selective_repeat.Selective_Repeat( env, 10 )
    protocol0.timeout_time = 30
    protocol1 = selective_repeat.Selective_Repeat( env, 10 )
    protocol1.timeout_time = 30
    protocol0.add_handler( h0.add_transport_handler( protocol0.get_handler() ) )
    protocol1.add_handler( h1.add_transport_handler( protocol1.get_handler() ) )
    protocol0.send( NUMBER_OF_PACKETS , simpynet.IP("192.0.0.1") )


def run_example():
    e = simpynet.Environment()
    e.add_network(network)
    e.run( )
    time_spent = (numpy.sum(e.collectors_values['data'][0][-1]['Switch0PointToPoint1']) - numpy.sum(e.collectors_values['data'][0][0]['PointToPoint0Switch0']) + numpy.sum(e.collectors_values['data'][0][-1]['Switch0PointToPoint0']) - numpy.sum(e.collectors_values['data'][0][0]['PointToPoint1Switch0']))/NUMBER_OF_PACKETS
    print "Each packet sent has spent an average time of " + str(time_spent) + " inside the switch."


def network_alt(env):
    simpynet.PointToPoint.unique_number=0
    simpynet.Switch.unique_number=0
    h0 = simpynet.Host(env , simpynet.Mac("00.00.00.00.00") , simpynet.IP("192.0.0.0"))
    h1 = simpynet.Host(env , simpynet.Mac("00.00.00.00.01") , simpynet.IP("192.0.0.1"))

    link0 = simpynet.PointToPoint(env, lambda x,y:PROPAGATION_DELAY, lambda src,trg,l: TRANSMISSION_DELAY)
    link1 = simpynet.PointToPoint(env, lambda x,y:PROPAGATION_DELAY, lambda src,trg,l: TRANSMISSION_DELAY)

    switch = simpynet.Switch( env, lambda x, y : PROCESSING_DELAY )

    simpynet.physical.plug(link0,h0)
    simpynet.physical.plug(link0,switch)
    simpynet.physical.plug(link1,switch)
    simpynet.physical.plug(link1,h1)

    env.add_collector_functions( 'received_frames', switch.collector_receivedframes , TIME_INCREMENT )
    env.add_collector_functions( 'sent_frames', switch.collector_sentframes , TIME_INCREMENT )

    protocol0 = selective_repeat.Selective_Repeat( env, 10 )
    protocol0.timeout_time = 30
    protocol1 = selective_repeat.Selective_Repeat( env, 10 )
    protocol1.timeout_time = 30
    protocol0.add_handler( h0.add_transport_handler( protocol0.get_handler() ) )
    protocol1.add_handler( h1.add_transport_handler( protocol1.get_handler() ) )
    protocol0.send( NUMBER_OF_PACKETS , simpynet.IP("192.0.0.1") )


def run_example_alt():
    e = simpynet.Environment()
    e.add_network(network_alt)
    e.run( )
    received_frames = e.collectors_values['received_frames']
    sent_frames = e.collectors_values['sent_frames']

    time_spent = 0

    for k in received_frames:
        time_spent += (received_frames[k][-1]-sent_frames[k][-1])*TIME_INCREMENT
    time_spent =  time_spent/NUMBER_OF_PACKETS
    print "Each packet sent has spent an average time of " + str(time_spent) + " inside the switch."
