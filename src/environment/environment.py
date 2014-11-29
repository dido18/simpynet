# -*- coding: utf-8 -*-
"""
This module simulates the environment extending the environment provided by 
``simpy``.\n
It also collects the statistics.
"""
import logging
import SimPyNet


class Environment(SimPyNet.simpy.Environment):
    """
    Simulates the Environment and collects the statistics data.
    """
    def __init__( self, initial_time=0 ):
        self.statistical_indexes=[]
        self.collectors_function = {}
        self.collectors_values={}
        self.network = None
        self.lgr = logging.getLogger(SimPyNet.__LOGNAME__)        
        self.frmt = logging.Formatter('%(asctime)s %(message)s ')
        


    def add_network( self , network):
        """
        E.add_network( network )
        When run() is called, builds a network with the given function.
        """
        self.network = network
        
        
    def add_collector_functions( self , cltr_name, collector , interval_collection=1 ):
        """
        E.add_collector_functions(  collector_name , collector , interval_collection=1 )
        Adds a collector function to the environment.
        The function *collector* is called every interval_collection time.
        """
        self.collectors_function[cltr_name] = [ collector, interval_collection ]
        if not self.collectors_values.has_key(cltr_name):
            self.collectors_values[cltr_name]= {} 
            
        return self.collectors_values[cltr_name]
        
    
    def _add_values( self  , cltr_name ):
        """
        Saves the collected values for each collector.
        """
        
        collector = self.collectors_function[cltr_name][0]
        time = float(self.now)
        if not self.collectors_values[cltr_name].has_key(time):
            self.collectors_values[cltr_name][time] = []
            
        self.collectors_values[cltr_name][time].append( collector() ) 

  
    def run_stats_function( self , function ):
        """
        E.run_stats_function( function )
        Returns function( collectors_values )
        """
        return function( self.collectors_values )
  
  
    def _stats_process( self ):
        """
        Main process that manages the statistics collectors and the time the 
        next one is due to be called.
        """
        time_next_collection = { name : 0
                                for name in self.collectors_function }
        min_interval = float("inf")
        while(True):
                for name , time in time_next_collection.iteritems():
                    if time == 0:
                        self._add_values( name )
                        time_next_collection[name] = self.collectors_function[name][1]
                        time = time_next_collection[name]
                    if time < min_interval: min_interval = time
                    
                if self.peek() == float('inf'):
                    break
                
                yield self.timeout( min_interval )
                
                for name in time_next_collection.iterkeys():
                    time_next_collection[name]-=min_interval
                min_interval = float("inf")

                 
    def run( self , number_of_runs = 1 , logging_level =  1 , until=None):
        """
        E.run( number_of_runs = 1 , logging_level =  1 , until=None )
        Builds and simulates a given network *number_of_runs* times.
        *logging_level* is the level of the logger.
        *until* is the maximum time of execution. It's set to None unless 
        specified.
        """
        SimPyNet.simpy.Environment.__init__( self )
        
        fh_log = logging.FileHandler(SimPyNet.__LOGNAME__, mode='a')
        fh_log.setFormatter(self.frmt)
        self.lgr.addHandler(fh_log)
        
        self.network( self )
        
        self.lgr.setLevel(logging_level)        

        self.lgr.log( 9 , '   New run ; Remaining runs :  '+str(number_of_runs))
        
        self.process(self._stats_process()) 
        
            
        number_of_runs -= 1        
        SimPyNet.simpy.Environment.run( self )
        
        self.lgr.removeHandler(fh_log)
        
        if number_of_runs > 0:
            self.run( number_of_runs , logging_level , until )


  

    