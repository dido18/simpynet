# -*- coding: utf-8 -*-
"""
Created on Thu May 29 19:01:11 2014

@author: unkown
"""
import SimPyNet as spn



def example1( env ):
    """
    Example at the link level.
    
    h1----l1----| r1 |---l2----h2
    
    """


    h1 = spn.Host(env , spn.Mac("00.00.00.00.00") , spn.IP("192.0.0.0"))
    h2 = spn.Host(env , spn.Mac("00.00.00.00.01") , spn.IP("192.0.0.1"))

    l1 = spn.Link(env, lambda x,y:3, lambda src,trg,l: 1)
    l2 = spn.Link(env, lambda x,y:3, lambda src,trg,l: 1)
    
    def host_handler(data):
        print data

    def forwarding( datagram , src_mac):
        if datagram.dst_ip == spn.IP("192.0.0.0"):
            return spn.Mac("00.00.00.00.00")
        else:
            return spn.Mac("00.00.00.00.01")

    
    r1 = spn.Router (env , spn.Mac("00.00.00.00.02") , forwarding , lambda x,y : 0.1 )
    
    spn.physical.plug(l1,r1)
    spn.physical.plug(l2,r1)
    spn.physical.plug(l1, h1)
    spn.physical.plug(l2,h2)

    send1=h1.add_transport_handler( host_handler )
    send2=h2.add_transport_handler( host_handler )


    def funct():
        yield env.timeout(0)
        send1("Ciao inviato da host 1", spn.IP("192.0.0.1"))
        
    def funct2():
        yield env.timeout(1)
        yield env.timeout(10)
        send2("Ciao inviato da host 2", spn.IP("192.0.0.0"))
    
    r_r = r1.collector_receiveddatagrams
    r_s = r1.collector_sentdatagrams
    r_t = r1.collector_processingtime
    h2_r = h2.collector_receiveddatagrams
    h1_s = h1.collector_sentdatagrams
    
    env.add_collector_functions( 'router received', r_r, 1  )
    env.add_collector_functions( 'router sent', r_s, 2 )
    env.add_collector_functions( 'router proc. time',  r_t,1)
    env.add_collector_functions( 'h2 received' , h2_r , 1)
    env.add_collector_functions( 'h1 sent' , h1_s , 1)
   
    
    env.process(funct())
    env.process(funct2())
    

#e = spn.Environment()
#e.add_network(example1)
#e.run( )


def example2( env ):
    
    
    """"
    example figure 5.17 p. 492 (Computer Networking, 6th edition, Kurose-Ross).
    
    c----l1-----|
                |
    b----l2--- |so|---l4---ro
                |
    a----l3-----|
    """
    
    env=spn.Environment()
    
    host_c=spn.Host( env,spn.Mac('1A:23:F9:CD:06:9B') , spn.IP('222.222.222.220' ) )
    host_b=spn.Host( env,spn.Mac('5C:66:AB:90:75:B1') , spn.IP('222.222.222.221' ) )
    host_a=spn.Host( env,spn.Mac('49:BD:D2:C7:56:2A') , spn.IP('222.222.222.222' ) )
    
    l1=spn.Link( env , trm_delay=lambda name, data : 1  , prg_delay= lambda s,r,l: 1 )
    l2=spn.Link( env , trm_delay=lambda name, data : 1  , prg_delay= lambda s,r,l: 1 )    
    l3=spn.Link( env , trm_delay=lambda name, data : 1  , prg_delay= lambda s,r,l: 1 )
    l4=spn.Link( env , trm_delay=lambda name, data : 1  , prg_delay= lambda s,r,l: 1 )
    
    s0=spn.Switch( env )
   
    def frw( datagram , mac ):
        print mac
        if mac==spn.Mac( '88:B2:2F:54:1A:0F' ):
        
            print 'forwanding'
            return spn.Mac( '5C:66:AB:90:75:B1' )
        else :
            print 'no fornarding'
        

    r0=spn.Router( env,spn.Mac('88:B2:2F:54:1A:0F') , frw )
    
    
    
    spn.physical.plug(host_c,l1)
    
    spn.physical.plug(l1,s0)
    spn.physical.plug(host_b,l2)
    spn.physical.plug(l2,s0)
    spn.physical.plug(host_a,l3)
    spn.physical.plug(l3,s0)
    spn.physical.plug(r0,l4)
    spn.physical.plug(l4,r0)
    
    def tcp_handler( segment ):
        print 'attivato tcp'
        
    def h_receiver(name, data, trm_delay): # receiver' s handler
        def _new_handler(name, data, trm_delay):
                yield env.timeout(trm_delay)
        return env.process(_new_handler(name, data, trm_delay))
    
    f_send = host_c.add_transport_handler(tcp_handler)
    host_b.add_handler('rcv',h_receiver)
    
    def rcv_r():
        pass
    
    host_c.default_gateway=spn.Mac('88:B2:2F:54:1A:0F')
    
    def sender():
        yield env.timeout(0)
        f_send('ciao da host 1', spn.IP('222.222.222.220'))
        

    env.process(sender())
      
 
    
e = spn.Environment()
e.add_network(example2)
e.run( )