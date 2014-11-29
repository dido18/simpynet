# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 16:26:11 2014

@author: dido
"""

import SimPyNet as spn
import logging 


class DHCP_client( ):
    
    
    def __init__(self , env , host  ):        
        
        self.env = env
        self.host = host 
        self.client_port = 67
        self.list_ip_server = []
        self.choose_ip_server = None 
        
        self.udp=spn.UDP_Protocol( env )
        send_host=self.host.add_transport_handler( self.udp.get_handler() ) 
        self.udp.add_handler( send_host )
        self.send_udp = self.udp.add_application_handler( self._receive_dhcp , self.client_port ) # handler per ricevere
        
        self.lgr = logging.getLogger(spn.__LOGNAME__)
 
    def _receive_dhcp( self, message ):
        """
        _receive_dhcp( message ) - the client recieves one or more DHCPOFFER 
        messages from one or more servers.
        """
        
        diz_opt =message.values
        option=diz_opt['option_53'] 
        
        if option =='DHCP Offer':    
            self.list_ip_server.append( diz_opt['option_54'] )
            ip_server = self.choose_ip_server( self.list_ip_server )
            self.send_DHCP_REQUEST( diz_opt , ip_server  )
            self.lgr.log(spn.__APPLICATION_LOG_N__,"   " + str(float(self.env.now)) + '   DHCP client sends DHCP REQUEST message to :'+str(ip_server)+' with request IP : '+str(diz_opt['YIADDR']) )
            
        if option == 'DHCP Ack':
            self.host.ip_addr=diz_opt['YIADDR']
            self.lgr.log(spn.__APPLICATION_LOG_N__,"   " + str(float(self.env.now)) + '   DHCP client allocates IP : '+str( diz_opt['YIADDR'] ))
        
    def send_DHCP_DISCOVERED( self  ):
        """
        send_DHCP_DISCOVERED() - send a DHCPdiscovered message in broadcast 
        on its local physical subnet.
        """
               
        dscv_msg = DHCP_DISCOVERED_message( self.host.mac_addr , self.host.ip_addr)  
        self.send_udp( dscv_msg , self.client_port , 68  , spn.IP('255.255.255.255') ) 
        self.lgr.log(spn.__APPLICATION_LOG_N__,"   " + str(float(self.env.now)) + '   DHCP client sends DHCP DISCOVERED message to : 255.255.255.255')
      
    
    def send_DHCP_REQUEST( self , diz_opt , ip_server ):
        """
        send_DHCPREQUEST( diz_option) - In response to the DHCP offer, 
        the client replies with a DHCP request,  broadcast to the server, 
        requesting the offered address.
        """
        ip_offer = diz_opt['YIADDR']
        qst_msg = DHCP_REQUEST_message( self.host.mac_addr ,self.host.ip_addr,
                                       ip_server , 
                                       ip_offer  
                                       )
        
        self.send_udp( qst_msg , self.client_port , 68 ,  spn.IP('255.255.255.255')  )

        
    def add_function_choose( self, func ):
        """
        add_function_choose(func ) - adds  function that choose ip_server. 
         """
        self.choose_ip_server = func 
        
class DHCP_DISCOVERED_message( ):
    
    
    def __init__( self , mac_client , client_ip   ):
        
        self.values={}
        self.values['CIADDR'] = client_ip   # client IP address
        self.values['CHADDR'] = mac_client  # client hardware address (MAC)
        self.values['option_53']='DHCP Discover'
            
        
    def __str__(self):
        s=' option : '+ self.values['option_53']
        return s
        
    def __len__(self):
        return len( self.values)
        
    def __repr__(self):
        s=' option : '+ self.values['option_53']
        return s
    
    
        
class DHCP_REQUEST_message( ):
    
    
    def __init__( self , client_mac , client_ip , ip_server , ip_request ):
        
         self.values={}
        
         self.values['CIADDR'] = client_ip    
         self.values['CHADDR'] = client_mac 
         self.values['YIADDR'] = ip_server       # choosen  ip server 
         self.values['option_50'] = ip_request   # ip request
         self.values['option_53']='DHCP Request'
         
        
    def __str__(self):
        s=' option : '+ self.values['option_53']
        return s
        
    def __len__(self):
        return len( self.values)
        
    def __repr__(self):
        s=' option : '+ self.values['option_53']
        return s
    

    