# -*- coding: utf-8 -*-
"""
This module contain 
"""
import logging
import SimPyNet
class Hub():
    """
    Simulates a Hub at the physical layer.\n
    *environment* is the class which simulates the passing of time provided by
    ``simpy``. \n
    *prg_delay* is the function that implements propagation delay, with
    parameters : source, target, data. Is set to 0 unless specified.
    .
    """
    
    unique_number = 0  # for a unique name of hubs.
    
    def __init__(self, 
                 environment,
                 prg_delay = lambda data , hub: 0.0 ):
        self.unique_number = self.__class__.unique_number
        self.__class__.unique_number = self.__class__.unique_number + 1
        
        self.lgr = logging.getLogger(SimPyNet.__LOGNAME__)
        
        self.prg_delay=prg_delay
        self.total_sent_data=0
        
        self.handlers={}     
        self.env = environment
       
        
        
    def add_handler(self,  name_interface , handler):
        """
        H.add_handler( name_interface , handler) - add handler to hub
        """
        self.handlers[ name_interface] = handler
        return self.get_handler( )
        
        
    def get_handler( self ):
        """
        H.get_handler() - get hub's handler
        """
        def _new_handler(sender_interface, data, trm_delay = 0.0): 
            return self.env.process(self._propagate(sender_interface, data, trm_delay ))
    
        return _new_handler
        
        
    def _propagate( self , sender_interface , data , d_trm_delay ):
        """
        Handler
        """
        self.lgr.log( SimPyNet.__PHYSICAL_LOG_N__ , "   " + str(float(self.env.now)) + "   " + repr(self) + ' : Begin transmission from: ' + str(sender_interface ) )

        self.total_sent_data += len( data )
        self.env.process( self._broadcast( sender_interface , data , d_trm_delay ) )
        yield self.env.timeout( d_trm_delay )        
        

    def _broadcast( self , sender_interface , data , d_trm_delay ):
        """
        Trasmits data from the interface to all the other handlers.
        """
        
        yield self.env.timeout(self.prg_delay( data , repr( self ) ) )
        for trg in self.handlers:
            if trg != sender_interface:
                self.env.process( self._deliver( trg , data, d_trm_delay ) )
                
        
    def _deliver( self , trg_interface , data , d_trm_delay ):
        """
        A single trasmission of a data to a destination handler.
        """
        
        yield self.handlers[ trg_interface ]( repr(self) , data, d_trm_delay )
        self.lgr.log( SimPyNet.__PHYSICAL_LOG_N__ , "   " + str(float(self.env.now)) + "   " + repr(self) + ' : End transmission to: ' + str(trg_interface ) )
                
    def remove_handler( self , name_interface ):
        """
        L.remove_handler( name_interface ) - remove the handler associated with
        name_ interfce.
        """
        if self.handlers.has_key( name_interface):
            del self.handlers[name_interface]
        else:
            raise Exception("Handler not found")
            
            
    def __repr__(self):
        """
        repr( Hub ) - hub's unique name
        """
        return "Hub"+str(self.unique_number)
        
        
    def collector_sentdatabits( self ):
        """
        collector_sentdatabits() - returns total data sent
        """
        return self.total_sent_data
  
        