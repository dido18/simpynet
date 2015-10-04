# -*- coding: utf-8 -*-
"""
Created on Mon May 19 18:20:20 2014

@author: unkown
"""

#import simpynet as spn
import spn


def example1(env):

    """
    This example simulates a simple network with three NIC interface connect
    with a switch.
    nic0 (with mac address "00:00:00:00:00:00")
    sends data with destination nic1 (with mac address "00:00:00:00:00:01").
    Switch sends data in broadcast, because its arp table is empty.
    Both nic1 anc nic2 receives data.
    After 10 seconds, nic1 send a packet to nic0
    (with destination mac "00:00:00:00:00:00").
    Switch has the values in its arp table, then sends data only to nic0.

    nic1

    |nic0|----l0----| switch0 |----l1 -----|nic1|
                        |
                        |
                       l2
                        |
                        |
                      |nic2|

    """

    l0 = spn.Link( env, lambda n, x:3, lambda src,trg, l: 1 )
    l1 = spn.Link( env, lambda n, x:3, lambda src,trg, l: 1 )
    l2 = spn.Link( env, lambda n, x:3, lambda src,trg, l: 1 )

    nic0 = spn.NIC(env, spn.Mac("00:00:00:00:00:00"))
    nic1 = spn.NIC(env, spn.Mac("00:00:00:00:00:01"))
    nic2 = spn.NIC(env, spn.Mac("00:00:00:00:00:02"))

    queue_size=10000  # bit
    switch0 = spn.Switch(env, lambda x,s:0.1, queue_size )

    spn.physical.plug( l0 , nic0 )
    spn.physical.plug( l1 , nic1 )
    spn.physical.plug( l2 , nic2 )


    spn.physical.plug( l0 , switch0 )
    spn.physical.plug( l1 , switch0 )
    spn.physical.plug( l2 , switch0 )


    data_host0 = []
    for i in range(10):
        data_host0.append("Hello from host0")

    data_host1 = []
    for i in range(10):
        data_host1.append("Hello from host1")


    def receiver0( data ):
        print data

    def receiver1( data ):
        print data

    def receiver2( data ):
        print data


    nic0_h = nic0.add_host_handler( receiver0 ) # return NIC 's handler to send
    nic1_h = nic1.add_host_handler( receiver1 )
    nic2_h = nic2.add_host_handler( receiver2 )


    def sender0():
        while( len( data_host0 ) >0):
            data=data_host0.pop(0)
            nic0_h( data , spn.Mac("00:00:00:00:00:01") )
            yield env.timeout(6)

    def sender1():
        yield env.timeout(10)
        while( len( data_host1 ) >0):
            data=data_host1.pop(0)
            nic1_h( data , spn.Mac("00:00:00:00:00:00") )
            yield env.timeout(7)

    dcrd_nic2=nic2.collector_discardedframes
    rcv_nic1= nic1.collector_receivedframes
    rcv_nic0= nic0.collector_sentframes

    env.add_collector_functions('discarded nic2',  dcrd_nic2 )
    env.add_collector_functions('received nic1',  rcv_nic1  )
    env.add_collector_functions('received nic0',  rcv_nic0  )

    env.process(sender0())
    env.process(sender1())

e = spn.Environment()
e.add_network(example1)
e.run( 1 , spn.__LINK_LOG_N__ )
