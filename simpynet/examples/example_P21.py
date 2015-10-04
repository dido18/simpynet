# -*- coding: utf-8 -*-
"""
Created on Sat May 31 06:03:32 2014

@author: dido
"""

import simpynet as spn

def problem21( env ):
    """


    """

    rate0 = 4
    rate1 = 4
    rate2 = 6
    rate3 = 2

    def trm_delay( name, data ):

        if repr(name)==repr(l0):
            return rate0
        if repr(name)==repr(l1):
            return rate1
        if repr(name)==repr(l2):
            return rate2
        if repr(name)==repr(l3):
            return rate3



    l0 = spn.Link( env , trm_delay )
    l1 = spn.Link( env , trm_delay )
    l2 = spn.Link( env , trm_delay )
    l3 = spn.Link( env , trm_delay )

    def h_receiver(name, data, trm_delay): # receiver' s handler
        def _new_handler(name, data, trm_delay):
                print 'Ricevuto'
                yield env.timeout(trm_delay)
        return env.process(_new_handler(name, data, trm_delay ))

    spn.physical.plug( l0 , l1 )
    spn.physical.plug( l1 , l2 )
    spn.physical.plug( l2 , l3 )

    data=spn.Databits(32000000) #32 Mbits

    f_send=l0.get_handler()

    l3.add_handler('rcv',h_receiver)

    def sender ( ):
        yield f_send( 'sender', data  )

    d= l3.collector_sentdatabits


    env.add_collector_functions(' link3 receive', d )

    env.process(sender())

e = spn.Environment()
e.add_network(problem21)
e.run()
