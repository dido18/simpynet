# -*- coding: utf-8 -*-
"""
Created on Sat May 31 19:19:31 2014

@author: dido
"""

   def average( lnumber ):
        l=len(lnumber)
        somma=0
        for n in lnumber:
            somma+=n
            
        return  somma/float(l)   
        
        
    
    def c_variance( lnumber ):
        
        """ variaza campionaria"
        """
        l=len(lnumber)
        a_somma=0
        for n in lnumber:
            a_somma+=n
            
        average= a_somma/float(l)    
        
        v_somma=0
        for n in lnumber:
            v_somma+=(n-average)**2
            
        return v_somma/float(l-1)
        
    def standard_deviation( lnumber ):
        l=len(lnumber)
        a_somma=0
        for n in lnumber:
            a_somma+=n
            
        average= a_somma/float(l)    
        
        v_somma=0
        for n in lnumber:
            v_somma+=(n-average)**2
            
        variance=v_somma/float(l-1)
        return variance**(0.5)  # Radice della varianza
    

                
     
    def sum_value( lnumber ):
        d=defaultdict(int)
        for n in lnumber:
            d[n]+=1
            
        l=len(lnumber)
        for v , num in d.items():
            d[v]=d[v]/float(l)      
        return d
        