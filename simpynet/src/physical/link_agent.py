"""
This module simulates the link at the physical layer.
"""

import random
import logging
import simpynet

class Link():
    """
    Simulates a shared link at the physical layer.\n
    *environment* is the class which simulates the passing of time provided by
    ``simpy.Environment``. \n
    *trm_delay* is the function that simulates trasmission delay of link. \n
    *prg_delay* is the funcion that simulates propagation delay of link. It has three
    arguments: source, target, data.\n
    *loss_prob* is the function that simulates loss probability of packets.
    It has two arguments: source, destination. \n
    *f_error* is the function that simulates an error in data.
    It has three arguments: source, target, data, return an corrupt data.\n
    The module ``logging`` is used to creates a log file of esecution, saved
    in the working directory.

    """
    unique_number = 0

    def __init__(self,
                 environment,
                 trm_delay ,
                 prg_delay = lambda src , trg , link: 0.0,
                 loss_prob = lambda src , trg , link: 0.0 ,
                 f_error = lambda  src , trg , data , link: data ,
                 ):
        self.unique_number = self.__class__.unique_number
        self.__class__.unique_number = self.__class__.unique_number + 1

        self.lgr = logging.getLogger(simpynet.__LOGNAME__)

        self.trm_delay=trm_delay
        self.prg_delay=prg_delay
        self.loss_prob=loss_prob
        self.f_error=f_error

        self.lost_data=0
        self.total_sent_data = 0

        self.handlers={}
        self.env = environment

    def add_handler( self, name_interface , handler ):
        """
        L.add_handler( handler ) - add handler to link  \n
        Return link's handler
        """
        self.handlers[name_interface] = handler
        return self.get_handler( )


    def get_handler( self ):
        """
        L.get_handler() - get link's handler
        """
        def _new_handler( sender_interface, data , trm_delay = 0.0 ):
            return self.env.process( self._do_send ( sender_interface , data , trm_delay ) )

        return _new_handler



    def _do_send( self , src_interface , data , d_trm_delay ):
        """
        Link's handler.
        Transmits data from a sender interface to all the other handlers
        (except the sender).
        """
        self.lgr.log( simpynet.__PHYSICAL_LOG_N__ , "   " + str(float(self.env.now)) + "   " + repr(self) + ' :  Begin transmission from: ' + src_interface )
        if d_trm_delay > self.trm_delay( data , repr( self ) ):
            trm_time = d_trm_delay
        else:
            trm_time = self.trm_delay( data , repr( self ) )
        self._broadcast( src_interface , data , trm_time )
        yield self.env.timeout( trm_time )
        self.total_sent_data += len( data )

    def _broadcast( self , src_interface , data , trm_time ):
        """
        Trasmits a data from a interface of the link,
        to all handler (without itself).
        """
        for trg_interface in self.handlers.keys():
            if trg_interface != src_interface:
                self.env.process( self._deliver( src_interface ,
                                                trg_interface ,
                                                data ,
                                                trm_time ) )



    def _deliver( self , src_interface , trg_interface , data , trm_time ):
        """
        A single trasmission of data from a source to a destination handler.

        """
        prg_delay = self.prg_delay( src_interface , trg_interface , repr( self ))
        if prg_delay > 0:
            yield self.env.timeout( prg_delay )
        random_value = random.random()
        if random_value <= self.loss_prob( src_interface , trg_interface , repr( self ) ):
            self.lgr.log( simpynet.__PHYSICAL_LOG_N__ , "   " + str(float(self.env.now)) + "   " + repr(self) + ' :  Lost from: ' + src_interface + " to " + trg_interface )
            self.lost_data+=1
        else:
            yield self.handlers[trg_interface] (  repr( self ) ,self.f_error( src_interface  , trg_interface , data , repr( self ) ) , trm_time )

            self.lgr.log( simpynet.__PHYSICAL_LOG_N__ , "   " + str(float(self.env.now)) + "   " + repr(self) + ' : End transmission to:  ' + trg_interface)

    def remove_handler( self , name_interface ):
        """
        L.remove_handler( name_interface ) - remove handler associates with
        name_interface of link.
        """

        if self.handlers.has_key( name_interface ):
            del self.handlers[name_interface]
        else:
            raise Exception("Handler not found")


    def __repr__(self):
        """
        repr(L) - unique name of link.
        """
        return "Link"+str(self.unique_number)


    def collector_lostdatabits( self ):
        """
        collector_lostdatabits() - returns total lost data
        """
        return self.lost_data


    def collector_sentdatabits( self ):
        """
        collector_sentdatabits() - returns total sent data
        """
        return self.total_sent_data





class PointToPoint(Link):
    """
    Simulates a point to point link at the physical layer.\n
    *environment* is the class which simulates the passing of time provided by
    ``simpy``. \n
    If not specified delay propagation, error probability and loss probability
    are set to ``0``.\n
    The variable *deterministic* defines if the delay is fixed or unpredictable
    .
    """

    unique_number = 0

    def add_handler(self, name_interface, handler):
        """
        L.add_handler(name_interface, handler) - add handler to link associate
        to a name interface.
        """
        if len(self.handlers)>1:
            raise Exception("There are already 2 nodes connected.")
        else:
            return Link.add_handler(self,name_interface,handler)


    def __repr__(self):
        """
        repr(L) - unique name of link.
        """
        return "PointToPoint"+str(self.unique_number)
