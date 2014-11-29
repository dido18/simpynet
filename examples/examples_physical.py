# -*- coding: utf-8 -*-
"""
This module contain some examples for the physical layer.

"""
import pandas as pd
import numpy as np
import SimPyNet as spn


def example1( env  ):
    """
    This example simulates the transfer of a packet of size 1000 byte 
    through a link with 
    -distance 2.5 km, 
    -propagation speed 2.5*10^8 m/s 
    -transmission rate 2 Mbps.
    
    A ---link-----B     
     
    Make reference to exercise R18 at page 95 
    (Computer Networking, 6th edition, Kurose-Ross).
    """
    packet_size = 1000*32 # bit
    distance = 2500000 # m
    speed_propagation = 250000#000 # m/s
    transmission_rate = 2000#000 # 2 Mbps


    trm_delay  = lambda  name, data : packet_size / float(transmission_rate)
    prg_delay  = lambda  src , trg , link  : distance / float(speed_propagation)
    
    link=spn.PointToPoint( env, trm_delay , prg_delay  )
      
    
    def h_receiver( name , data, d_trm_delay ): # receiver' s handler
        def _new_handler( name, data , d_trm_delay ):
                yield env.timeout( d_trm_delay )
        return env.process( _new_handler( name , data , d_trm_delay ) )


    f_send=link.add_handler( 'rcv' , h_receiver ) #  handler of Point to Point link

    packet=spn.Databits( packet_size )     
    
    def sender():
        yield f_send('sender', packet, 0.0 )
        
#    env.add_collector_functions('l1 sent data', link.collector_sentdatabits , 4)


    env.process(sender())
    



def example2( env ):
    """
    This example simulates the transfer of a packet of 4 million bytes,
    from A to B.
    
    A /---l1----/-----l2----/----l3----/ B
    
    The path has three link of rates: 
    r1= 500 Kbps, r2 = 2Mbps, r3 = 1 Mbps.
    Make reference to exercise R19 at page 95 
    (Computer Networking, 6th edition, Kurose_Ross)
    """
    packet_size = 40000000 # 40 Mbit
    trm_1 = 2000000.0  #bps
    trm_2 = 500000.0 #bps
    trm_3 = 1000000.0 #bps
    
        
    prg_delay= lambda src,dst,link: 0  # no propagation delay 

    packet=spn.Databits( packet_size ) 
    
    def trm_d( name, data ):
        
        if(  name ==repr(l1)):
            return len(data)/trm_1
            
        if( name==repr(l2)):
            return len(data)/trm_2
            
        if(  name ==repr(l3)):
            return len(data)/trm_3
            
    l1=spn.Link( env, trm_d , prg_delay )
    l2=spn.Link( env, trm_d , prg_delay )    
    l3=spn.Link( env, trm_d , prg_delay )
    
            
    spn.physical.plug(l1,l2) 
    spn.physical.plug(l2,l3)


    
    def h_receiver(name, data, trm_delay):
        def _new_handler(name, data, trm_delay):
                yield env.timeout(trm_delay)
        return env.process(_new_handler(name, data, trm_delay))

    l3.add_handler('receiver',h_receiver)
    
    f_send=l1.get_handler()
 
    def sender():
        yield f_send('sender',packet , trm_delay = 0 )
        
           
    clt_l1=l1.collector_sentdatabits
    clt_l2=l2.collector_sentdatabits
    clt_l3=l3.collector_sentdatabits
    

    env.add_collector_functions( 'l1 sent data' , clt_l1 , 2 ) 
    env.add_collector_functions( 'l2 sent data' , clt_l2 , 2 )
    env.add_collector_functions( 'l3 sent data' , clt_l3 , 2 )
    
    
    env.process(sender())

def example3( env ):
    
    """
    This example simulate a trasfer from a Host A to two hosts B and C, 
    A hub connects three links.
    
    A---l1---Hub ---l2---B
              |
              |
             l3
              |
              |
              C
            
    Statistics are collected from different intervall for every collector.
    """
    packet_size = 12000 #bits
    trm_rate= 2000 # b/s
    
    trm_delay =lambda name, data: len(data) / float(trm_rate) 
  
       
    packet=spn.Databits( packet_size ) 
    
    hub=spn.Hub( env, lambda d,l: 0.0 )
    
    def prg_delay( src_interface, trg_interface , link ):
        if( src_interface=='sender' and trg_interface  ==repr(hub)):
            return 4
        if( src_interface==repr(hub) and trg_interface  =='b'):
            return 8
        if( src_interface==repr(hub) and trg_interface  =='c'):
            return 16
    
    l1=spn.PointToPoint( env, trm_delay , prg_delay )
    l2=spn.PointToPoint( env, trm_delay , prg_delay )    
    l3=spn.PointToPoint( env, trm_delay , prg_delay )
    
    spn.physical.plug(l1,hub)  
    spn.physical.plug(hub,l2)
    spn.physical.plug(hub,l3)
    
    
    f_send=l1.get_handler()
        
    def sender():
        yield f_send('sender',packet , trm_delay=0.0)
        
    def h_receiver(name, data, trm_delay):
        def _new_handler(name, data, trm_delay):
                yield env.timeout(trm_delay)                
        return env.process( _new_handler( name, data, trm_delay) )
        
        
    l1.add_handler( 'b', h_receiver )
    l2.add_handler( 'c', h_receiver )
    
    d=hub.collector_sentdatabits
    c_l1=l1.collector_sentdatabits
    
   
#    env.set_stat_file_name('SPHY.EX3')
  
    env.add_collector_functions('sent hub'    , d     )
    env.add_collector_functions('l1 sent data ', c_l1 )
  
#    def massimo( l ):
#        return max(l) 
#        
#    env.add_statistical_index( np.mean )
#    env.add_statistical_index( massimo )

    
    env.process( sender() )
   


def example4( env ):
    """
    This example simulates the transfer of a list of 100 packets, of 1000 bits
    everyone, through a link with 
    -distance 2.5 km, 
    -propagation speed 2.5*10^8 m/s 
    -transmission rate 2 Mbps.
    -probabilità perdita di pacchetti= 0.3
    -funzione di errore nei pacchetti
    
    A ---link-----B     
     
    """
    packet_size = 1000 # bit
    distance = 2500000 # m
    speed_propagation = 25000000 # m/s
    transmission_rate = 2000 #bps
    
    
    packet=spn.Databits( packet_size ) 
    list_packet=[]
    
    
    
    trm_delay  = lambda  name, data : packet_size / float(transmission_rate) # 0.5 s
    prg_delay  = lambda  src , trg, link  : distance / float(speed_propagation) #0.1 s
    loss_prob  = lambda src , trg, link: 0.2
    f_error    =  lambda  src , trg , data , link :  data.set_error(True)
    
    link=spn.Link( env, trm_delay , prg_delay , loss_prob ,f_error )
    

    def h_receiver(name, data, trm_delay): # receiver' s handler
        def _new_handler(name, data, trm_delay):
                yield env.timeout(trm_delay) 
        return env.process(_new_handler(name, data, trm_delay))

    link.add_handler('rcv',h_receiver) 
    
    f_send=link.get_handler() #  handler of  link
    
    for i in range(10):
        list_packet.append(packet)
        
    def sender():
        while( len( list_packet ) >0):
            packet=list_packet.pop(0)
            yield f_send('sender', packet  )
    
    d=link.collector_sentdatabits
    c=link.collector_lostdatabits
    
    env.add_collector_functions( 'link sent Data' , d , 1 )
    env.add_collector_functions( 'link lost Data' , c , 1)

    def somma( l ):
        return sum(l)
        
    def massimo( l ):
        return max(l)
                
#    env.set_stat_file_name('PHY.EX4')
    
#    env.add_statistical_index( np.mean )
#    env.add_statistical_index( massimo )
#    env.add_statistical_index( somma )
    #env.set_stat_file_name('stat_example4')
    
    env.process(sender())
    
    
    
e=spn.Environment()
e.add_network(example1)
e.run( )



