# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 16:58:15 2014

@author: ubuntudido
"""

import simpy
import link
import physical


def f(Obj,data):
    
    print ('%f %s ha finito di elaborare %s')%(Obj.env.now, Obj.name,data.name)
    
def start(Obj,data):
    
    print ('%f %s ha inviato il dato %s sul link %s')%(Obj.env.now, Obj.name,data.name,Obj.next_connection.name)
    
def R18():
    
    size_packet=8 # in bits
    num_packets=5
    list_data=[]
    #err_prob=0
    #loss_prob=0.03

    rate_link= 2000000 # bits/s
    delay_prop_link=0.01 # m/s
    #delay_proc_router=0.01
    #queue_router=2

    for i in range(num_packets):
        list_data.append(physical.Databits(i,size_packet))
   
    env=simpy.Environment()
    
    A=link.Host(env,'mac_a')
    B=link.Host(env,'mac_b')
    
    rA=link.Router(env,0.1,3,'mac_rA')
    
    l1=link.Link(env,'l1',rate_link,delay_prop_link)

    A.addHandler(l1.getHandler)
    B.addHandler(l1.getHandler)
    l1.addHandler(rA.getHandler)
    l1.addHandler(A.getHandler)
    l1.addHandler(B.getHandler)
    rA.addHandler(l1.getHandler)
    
    
    A.sendData(list_data, 'mac_rA')
    B.sendData(list_data, 'mac_rA') 
    
    env.run(until=1000)
    

R18()