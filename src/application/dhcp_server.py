# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 18:13:15 2014

@author: dido
"""
import SimPyNet as spn
import logging


class DHCP_server(  ):
    
    
    def __init__(self , env , host  ):        
        
        self.env = env
        self.host = host 
        self.my_port = 68 
        self.udp = spn.UDP_Protocol( env )
        self.choose_ip_for_client = None
        
        send_host = self.host.add_transport_handler( self.udp.get_handler() ) 
        rcv_udp = self.udp.add_handler( send_host )
        self.send_udp = self.udp.add_application_handler( self._rcv_server_dhcp , self.my_port ) # handler per ricevere

        self.lgr = logging.getLogger(spn.__LOGNAME__)
         
    def add_function_choose( self , funct ):
        """
        add_function_choose(funct ) _
        """
        self.choose_ip_for_client = funct 
        
        
    def _rcv_server_dhcp( self , message) :
        
        """
        _rcv_server_dhcp( message) - server responds in different ways for
        different received messages from client.
            
        """
       
        diz_opt =  message.values
        option =diz_opt['option_53']
        
        if option =='DHCP Discover':
            
            """
            Each server may respond with a DHCPOFFER message that includes an
            available network address in the 'yiaddr' field
            """
            
            ip_offer = self.choose_ip_for_client()
            self.send_DHCP_OFFER( diz_opt , ip_offer )
            self.lgr.log(spn.__APPLICATION_LOG_N__,"   " + str(float(self.env.now)) + '   DHCP server sends DHCP OFFER message to :'+str(diz_opt['CIADDR'])+' with IP offer : '+str(ip_offer))
           
        elif option =='DHCP Request' :
            
            ip_server = diz_opt['YIADDR']
            
            if str(ip_server) != str(self.host.ip_addr):
                self.lgr.log(spn.__APPLICATION_LOG_N__,"   " + str(float(self.env.now)) + '   DHCP server declined DHCP REQUEST ')
            else:
                self.send_DHCP_ACK( diz_opt )
                self.lgr.log(spn.__APPLICATION_LOG_N__,"   " + str(float(self.env.now)) + '   DHCP server sends DHCP ACK to: '+str(diz_opt['CIADDR']))
        
        
 

        
    def send_DHCP_OFFER( self , diz_opt , ip_offer ):
        
         mac_client = diz_opt['CHADDR']
         ip_client = diz_opt['CIADDR'] 
         offer_msg = DHCP_OFFER_message( self.host.ip_addr , 
                                           mac_client, 
                                           ip_offer , 
                                           ip_client  )
            
         self.host.default_gateway=  mac_client
            
         self.send_udp(offer_msg, self.my_port , 67 , spn.IP() )  #sent in broadcast 
       
       
    def send_DHCP_ACK( self, diz_opt  ):
        
        ip_client = diz_opt['option_50']
        
        dst_ip = diz_opt['CIADDR']
        ack_msg = DHCP_ACK_message( ip_client )
        
        self.send_udp( ack_msg , self.my_port , 67 , dst_ip )
     
     
        
class DHCP_OFFER_message( ):
    
    
    def __init__( self ,server_ip , client_mac ,  ip_offer , client_ip):
        
        self.values={}
        self.values['CIADDR'] = client_ip  
        self.values['YIADDR'] = ip_offer    # your (client) ip
        self.values['CHADDR'] = client_mac  # Client hardware address
        
        self.values['option_53']='DHCP Offer'  #defines the "type" of the DHCP message.
        self.values['option_54']=str(server_ip) 
        
        
        
    def __str__(self):
        s='Option : '+self.values['option_53']
        return s
        
    def __len__(self):
        return len( self.values)
        
    def __repr__(self):
        s='Option : '+self.values['option_53']
        return s
    
        
        

class DHCP_ACK_message( ):
    
    
    def __init__( self , yiaddr ):
    
         self.values={}     
         self.values['YIADDR']= yiaddr    
         self.values['option_53'] ='DHCP Ack'
    
    def __str__(self):
        s='Option : '+self.values['option_53']
        return s
        
    def __len__(self):
        return len( self.values)
        
    def __repr__(self):
        s='Option : '+self.values['option_53']
        return s
    