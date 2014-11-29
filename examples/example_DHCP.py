# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 17:40:55 2014

@author: dido
"""


import SimPyNet as spn


def example( env ):
    
    """
    
    dhcp_client------l1------dhcp_server
    
    """
    # --------------------------------------------------------

    c_host = spn.Host( env, spn.Mac('aa.aa.aa.aa.aa.aa'),  spn.IP('0.0.0.0') )
    s_host = spn.Host( env, spn.Mac('bb.bb.bb.bb.bb.bb'),  spn.IP('192.168.1.1') )
    

    client=spn.DHCP_client( env , c_host )
    server=spn.DHCP_server( env , s_host )
    
    def choose_ip_server( lista_ip):
        if len(lista_ip) > 0:          
            return lista_ip.pop(0)
            
        else: return None
        
        
    def choose_ip_for_client():
        return '123'
        
    server.add_function_choose( choose_ip_for_client)
    
    client.add_function_choose( choose_ip_server)
    
    l1 = spn.Link(env, lambda x,y: 1 , lambda src,trg,l: 1)
    
    spn.physical.plug( l1 , c_host )
    spn.physical.plug( l1 , s_host )
    
    
    def funct():
        yield env.timeout(1)
        client.send_DHCP_DISCOVERED()
        
    env.process( funct())
     
    
    
    
e=spn.Environment()
e.add_network(example)
e.run( 1, spn.__TRANSPORT_LOG_N__)
    